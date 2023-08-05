"""cogeo-mosaic AWS DynamoDB backend."""

import itertools
import json
import os
import re
import sys
import warnings
from decimal import Decimal
from typing import Any, Dict, List, Sequence
from urllib.parse import urlparse

import attr
import boto3
import click
import mercantile
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from cachetools import TTLCache, cached
from cachetools.keys import hashkey

from cogeo_mosaic.backends.base import BaseBackend
from cogeo_mosaic.backends.utils import find_quadkeys
from cogeo_mosaic.cache import cache_config
from cogeo_mosaic.errors import (
    _HTTP_EXCEPTIONS,
    MosaicError,
    MosaicExistsError,
    MosaicNotFoundError,
)
from cogeo_mosaic.logger import logger
from cogeo_mosaic.mosaic import MosaicJSON
from cogeo_mosaic.utils import bbox_union


@attr.s
class DynamoDBBackend(BaseBackend):
    """DynamoDB Backend Adapter."""

    client: Any = attr.ib(default=None)
    region: str = attr.ib(default=os.getenv("AWS_REGION", "us-east-1"))
    table_name: str = attr.ib(init=False)
    mosaic_name: str = attr.ib(init=False)
    table: Any = attr.ib(init=False)

    _backend_name = "AWS DynamoDB"
    _metadata_quadkey: str = "-1"

    def __attrs_post_init__(self):
        """Post Init: parse path, create client and connect to Table.

        A path looks like

        dynamodb://{region}/{table_name}:{mosaic_name}
        dynamodb:///{table_name}:{mosaic_name}

        """
        logger.debug(f"Using DynamoDB backend: {self.path}")

        if not re.match(
            r"^dynamodb://([a-z]{2}\-[a-z]+\-[0-9])?\/[a-zA-Z0-9\_\-\.]+\:[a-zA-Z0-9\_\-\.]+$",
            self.path,
        ):
            raise ValueError(f"Invalid DynamoDB path: {self.path}")

        parsed = urlparse(self.path)

        mosaic_info = parsed.path.lstrip("/").split(":")
        self.table_name = mosaic_info[0]
        self.mosaic_name = mosaic_info[1]

        logger.debug(f"Table: {self.table_name}")
        logger.debug(f"Mosaic: {self.mosaic_name}")

        self.region = parsed.netloc or self.region
        self.client = self.client or boto3.resource("dynamodb", region_name=self.region)
        self.table = self.client.Table(self.table_name)
        super().__attrs_post_init__()

    @property
    def _quadkeys(self) -> List[str]:
        """Return the list of quadkey tiles."""
        resp = self.table.query(
            KeyConditionExpression=Key("mosaicId").eq(self.mosaic_name),
            ProjectionExpression="quadkey",
        )
        return [
            item["quadkey"]
            for item in resp["Items"]
            if item["quadkey"] != self._metadata_quadkey
        ]

    def write(self, overwrite: bool = False, **kwargs: Any):
        """Write mosaicjson document to AWS DynamoDB.

        Args:
            overwrite (bool): delete old mosaic items inthe Table.
            **kwargs (any): Options forwarded to `dynamodb.create_table`

        Returns:
            dict: dictionary with metadata constructed from the sceneid.

        Raises:
            MosaicExistsError: If mosaic already exists in the Table.

        """
        if not self._table_exists():
            self._create_table(**kwargs)

        if self._mosaic_exists():
            if not overwrite:
                raise MosaicExistsError(
                    f"Mosaic already exists in {self.table_name}, use `overwrite=True`."
                )
            self.delete()

        items = self._create_items()
        self._write_items(items)

    def _update_quadkey(self, quadkey: str, dataset: List[str]):
        """Update single quadkey in DynamoDB."""
        self.table.put_item(
            Item={"mosaicId": self.mosaic_name, "quadkey": quadkey, "assets": dataset}
        )

    def _update_metadata(self):
        """Update bounds and center.

        Note: `parse_float=Decimal` is required because DynamoDB requires all numbers to be in Decimal type

        """
        meta = json.loads(self.metadata.json(), parse_float=Decimal)
        meta["quadkey"] = self._metadata_quadkey
        meta["mosaicId"] = self.mosaic_name
        self.table.put_item(Item=meta)

    def update(
        self,
        features: Sequence[Dict],
        add_first: bool = True,
        quiet: bool = False,
        **kwargs,
    ):
        """Update existing MosaicJSON on backend."""
        logger.debug(f"Updating {self.mosaic_name}...")

        new_mosaic = self.mosaic_def.from_features(
            features,
            self.mosaic_def.minzoom,
            self.mosaic_def.maxzoom,
            quadkey_zoom=self.quadkey_zoom,
            quiet=quiet,
            **kwargs,
        )

        fout = os.devnull if quiet else sys.stderr
        with click.progressbar(  # type: ignore
            new_mosaic.tiles.items(),
            file=fout,
            show_percent=True,
            label=f"Updating mosaic {self.table_name}:{self.mosaic_name}",
        ) as items:
            for quadkey, new_assets in items:
                tile = mercantile.quadkey_to_tile(quadkey)
                assets = self.assets_for_tile(*tile)
                assets = [*new_assets, *assets] if add_first else [*assets, *new_assets]

                # add custom sorting algorithm (e.g based on path name)
                self._update_quadkey(quadkey, assets)

        bounds = bbox_union(new_mosaic.bounds, self.mosaic_def.bounds)

        self.mosaic_def._increase_version()
        self.mosaic_def.bounds = bounds
        self.mosaic_def.center = (
            (bounds[0] + bounds[2]) / 2,
            (bounds[1] + bounds[3]) / 2,
            self.mosaic_def.minzoom,
        )

        self._update_metadata()

    def _create_table(self, billing_mode: str = "PAY_PER_REQUEST", **kwargs: Any):
        """Create DynamoDB Table.

        Args:
            billing_mode (str): DynamoDB billing mode (default set to PER_REQUEST).
            **kwargs (any): Options forwarded to `dynamodb.create_table`

        """
        logger.debug(f"Creating {self.table_name} Table.")

        # Define schema for primary key
        # Non-keys don't need a schema
        attr_defs = [
            {"AttributeName": "mosaicId", "AttributeType": "S"},
            {"AttributeName": "quadkey", "AttributeType": "S"},
        ]
        key_schema = [
            {"AttributeName": "mosaicId", "KeyType": "HASH"},
            {"AttributeName": "quadkey", "KeyType": "RANGE"},
        ]

        # Note: errors if table already exists
        try:
            self.client.create_table(
                AttributeDefinitions=attr_defs,
                TableName=self.table.table_name,
                KeySchema=key_schema,
                BillingMode=billing_mode,
                **kwargs,
            )

            # If outside try/except block, could wait forever if unable to
            # create table
            self.table.wait_until_exists()
        except self.table.meta.client.exceptions.ResourceNotFoundException:
            warnings.warn("Unable to create table.")
            return

    def _create_items(self) -> List[Dict]:
        """Create DynamoDB items from Mosaic defintion.

        Note: `parse_float=Decimal` is required because DynamoDB requires all numbers to be
            in Decimal type (ref: https://blog.ruanbekker.com/blog/2019/02/05/convert-float-to-decimal-data-types-for-boto3-dynamodb-using-python/)

        """
        items = []
        meta = json.loads(self.metadata.json(), parse_float=Decimal)
        meta = {"quadkey": self._metadata_quadkey, "mosaicId": self.mosaic_name, **meta}
        items.append(meta)

        for quadkey, assets in self.mosaic_def.tiles.items():
            item = {"mosaicId": self.mosaic_name, "quadkey": quadkey, "assets": assets}
            items.append(item)

        return items

    def _write_items(self, items: List[Dict]):
        with self.table.batch_writer() as batch:
            with click.progressbar(
                items,
                length=len(items),
                show_percent=True,
                label=f"Uploading mosaic {self.table_name}:{self.mosaic_name} to DynamoDB",
            ) as progitems:
                for item in progitems:
                    batch.put_item(item)

    @cached(
        TTLCache(maxsize=cache_config.maxsize, ttl=cache_config.ttl),
        key=lambda self: hashkey(self.path),
    )
    def _read(self) -> MosaicJSON:  # type: ignore
        """Get Mosaic definition info."""
        meta = self._fetch_dynamodb(self._metadata_quadkey)
        if not meta:
            raise MosaicNotFoundError(
                f"Mosaic {self.mosaic_name} not found in table {self.table_name}"
            )

        # Numeric values are loaded from DynamoDB as Decimal types
        # Convert maxzoom, minzoom, quadkey_zoom to int
        for key in ["minzoom", "maxzoom", "quadkey_zoom"]:
            if meta.get(key):
                meta[key] = int(meta[key])

        # Convert bounds, center to float
        for key in ["bounds", "center"]:
            if meta.get(key):
                meta[key] = list(map(float, meta[key]))

        # Create pydantic class
        # For now, a tiles key must exist
        meta["tiles"] = {}
        return MosaicJSON(**meta)

    @cached(
        TTLCache(maxsize=cache_config.maxsize, ttl=cache_config.ttl),
        key=lambda self, x, y, z: hashkey(self.path, x, y, z),
    )
    def get_assets(self, x: int, y: int, z: int) -> List[str]:
        """Find assets."""
        mercator_tile = mercantile.Tile(x=x, y=y, z=z)
        quadkeys = find_quadkeys(mercator_tile, self.quadkey_zoom)
        return list(
            itertools.chain.from_iterable(
                [self._fetch_dynamodb(qk).get("assets", []) for qk in quadkeys]
            )
        )

    def _fetch_dynamodb(self, quadkey: str) -> Dict:
        try:
            return self.table.get_item(
                Key={"mosaicId": self.mosaic_name, "quadkey": quadkey}
            ).get("Item", {})
        except ClientError as e:
            status_code = e.response["ResponseMetadata"]["HTTPStatusCode"]
            exc = _HTTP_EXCEPTIONS.get(status_code, MosaicError)
            raise exc(e.response["Error"]["Message"]) from e

    def _table_exists(self) -> bool:
        """Check if the Table already exists."""
        try:
            _ = self.table.table_status
            return True
        except self.table.meta.client.exceptions.ResourceNotFoundException:
            return False

    def _mosaic_exists(self) -> bool:
        """Check if the mosaic already exists in the Table."""
        item = self.table.get_item(
            Key={"mosaicId": self.mosaic_name, "quadkey": self._metadata_quadkey}
        ).get("Item", {})
        return bool(item)

    def delete(self):
        """Delete all items for a specific mosaic in the dynamoDB Table."""
        logger.debug(f"Deleting all items for mosaic {self.mosaic_name}...")

        quadkey_list = self._quadkeys + [self._metadata_quadkey]
        with self.table.batch_writer() as batch_writer:
            for item in quadkey_list:
                batch_writer.delete_item(
                    Key={"mosaicId": self.mosaic_name, "quadkey": item}
                )
