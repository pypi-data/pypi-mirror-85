from pyspark.sql import DataFrame
import re


def wc_select(self: DataFrame, pattern: str = "*") -> DataFrame:
    expr = pattern.replace("*", ".+")
    cols = [c for c in self.columns if re.search(expr, c)]
    return self.select(*cols)


DataFrame.wc_select = wc_select
