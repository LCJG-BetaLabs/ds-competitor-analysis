"""
Functions for reading and writing to Feature Store.
Copied and modified from ds-mix-and-match
https://github.com/LCJG-BetaLabs/ds-mix-and-match/blob/master/mix_and_match/connection.py
"""
import os
import pandas as pd
from typing import List, Optional, Union
from functools import lru_cache

CA_DATABASE = os.environ.get("CA_DATABASE", "competitor_analysis")
LC_DATABASE = os.environ.get("LC_DATABASE", "lanecrawford")
FEATURE_STORE_ATTRIBUTE_TABLE = os.environ.get(
    "FEATURE_STORE_ATTRIBUTE_TABLE", "attribute"
)

# programmatically detect if running on databricks
IS_DATABRICKS = "DATABRICKS_RUNTIME_VERSION" in os.environ
if IS_DATABRICKS:
    try:
        from databricks.feature_store import FeatureStoreClient
        from pyspark.sql import SparkSession
    except ImportError as e:
        raise ValueError(f"Running on Databricks but failed to import modules") from e


def feature_store_table_exists(database: str, table: str) -> bool:
    fs = FeatureStoreClient()
    try:
        fs.get_table(name=f"{database}.{table}")
    except Exception:  # can be either ValueError or just Exception
        return False
    return True


def read_feature_store(
    database: str,
    table: str,
    columns: Optional[List[str]] = None,
) -> pd.DataFrame:
    """
    Attempts to read table from Feature Store.
    """
    df = _cached_read_fs(database, table)
    if columns:
        df = df[columns]
    return df


@lru_cache(maxsize=16)
def _cached_read_fs(database: str, table: str) -> pd.DataFrame:
    # reading from fs is slow, cache it
    fs = FeatureStoreClient()
    return fs.read_table(name=f"{database}.{table}").toPandas()


def write_feature_store(
    database: str,
    table: str,
    df: pd.DataFrame,
    mode: str = "merge",
    primary_keys: Optional[Union[str, List[str]]] = None,
    **kwargs,
):
    _write_feature_store_table(database, table, df, mode, primary_keys, **kwargs)


def _write_feature_store_table(
    database: str,
    table: str,
    df: Union[pd.DataFrame, "pyspark.sql.dataframe.DataFrame"],
    mode: str = "merge",
    primary_keys: Optional[Union[str, List[str]]] = None,
    **kwargs,
):
    if not IS_DATABRICKS:
        raise ValueError("Cannot write to Feature Store when not running on Databricks")

    spark = SparkSession.getActiveSession()  # should be sufficient if on databricks
    fs = FeatureStoreClient()
    if isinstance(df, pd.DataFrame):
        df = spark.createDataFrame(df)
    if feature_store_table_exists(database, table):
        fs.write_table(
            name=f"{database}.{table}",
            df=df,
            mode=mode,
            **kwargs,
        )
    else:
        fs.create_table(
            name=f"{database}.{table}",
            primary_keys=primary_keys,
            df=df,
            **kwargs,
        )
