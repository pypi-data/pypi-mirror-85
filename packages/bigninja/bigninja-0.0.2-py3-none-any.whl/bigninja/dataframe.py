from typing import Dict, List, Any

from pyspark.sql import DataFrame, Row
import re

from pyspark.sql.types import *
import pyspark.sql.functions as f


def wc_select(self: DataFrame, pattern: str = "*") -> DataFrame:
    expr = pattern.replace("*", ".+")
    cols = [c for c in self.columns if re.search(expr, c)]
    return self.select(*cols)


def display_with_json(self: DataFrame) -> None:
    for column in self.schema:
        t = type(column.dataType)
        if t == StructType or t == ArrayType or t == MapType:
            self = self.withColumn(column.name, f.to_json(column.name))
    self.show(truncate=False)


def union_anyway(self: DataFrame, df2: DataFrame) -> DataFrame:
    # take first df and add missing columns, filling them with nulls
    df1u = self
    for df2c in df2.columns:
        if df2c not in self.columns:
            df1u = (df1u.withColumn(df2c, f.lit(None)))

    # take df2 and make it idential in order and columns to df1u
    cols2 = []
    for df1c in df1u.columns:
        if df1c in df2.columns:
            # add own column
            cols2.append(f.col(df1c))
        else:
            # add a dummy
            cols2.append(f.lit(None).alias(df1c))
    df2u = df2.select(*cols2)
    df = df1u.union(df2u)

    return df


def as_list_of_dict(self: DataFrame) -> List[Dict[str, Any]]:
    row_list: List[Row] = self.collect()
    return [r.asDict(True) for r in row_list]


def head_as_dict(self: DataFrame) -> Dict[str, Any]:
    r: Row = self.head()
    return r.asDict(True)


def col_as_list(self: DataFrame, col_name: str = None) -> List[Any]:
    df = self
    if col_name:
        df = df.select(col_name)
    rows = df.collect()
    return [x[0] for x in rows]


DataFrame.wc_select = wc_select
DataFrame.display = display_with_json
DataFrame.union_anyway = union_anyway
DataFrame.as_list_of_dict = as_list_of_dict
DataFrame.head_as_dict = head_as_dict
DataFrame.col_as_list = col_as_list
