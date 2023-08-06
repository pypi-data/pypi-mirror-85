from pyspark.sql import DataFrame
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


DataFrame.wc_select = wc_select
DataFrame.display = display_with_json
