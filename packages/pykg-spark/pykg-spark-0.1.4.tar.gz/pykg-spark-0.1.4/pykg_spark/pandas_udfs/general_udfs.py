import pandas as pd
from uuid import uuid4
from pyspark.sql.functions import pandas_udf, PandasUDFType, udf
from pyspark.sql.types import DoubleType, StringType
from .general_udfs_base import clean_string, empty_string_to_null


@pandas_udf(StringType(), PandasUDFType.SCALAR)
def pd_clean_string(target_col):
    """ Apply `clean_string` over Spark Column.
    Args:
        target_col (Spark Column): containing strings to clean.
    Returns:
        Spark Column (StringType): cleaned version of input strings.
    """
    return pd.Series(target_col.apply(lambda x: clean_string(x)))

@pandas_udf(StringType(), PandasUDFType.SCALAR)
def pd_empty_string_to_null(target_col):
    """ Apply `empty_string_to_null` to Spark Column.
    Args:
        target_col (Spark Column): containing strings to convert empties --> nulls
    Returns:
        Spark Column: where empty strings replaced with nulls.
    """
    return pd.Series(target_col.apply(lambda x: empty_string_to_null(x)))

def pd_map_string(broadcast_map):
    """ Apply `map dict` to Spark Column, and return prior value if not containe 
        in map.

    Usage example:
        df.withColumn("new_col", pd_map_string(broadcast_variable)(F.col("old_col"))).show()

    Args:
        target_col (Spark Column): containing strings to convert with map
    Returns:
        Spark Column: where strings replaced with map.
    """
    def f(x):
        if x in broadcast_map.value:
            return broadcast_map.value.get(x)
        else:
            return x
    return udf(f)