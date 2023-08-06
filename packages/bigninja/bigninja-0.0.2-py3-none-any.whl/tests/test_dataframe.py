from pyspark.sql import SparkSession
from bigninja import *

spark = SparkSession.builder.config("spark.driver.host", "127.0.0.1").getOrCreate()

df1 = spark.createDataFrame([
    {
        "id": 1,
        "name": "Ivan"
    },
    {
        "id": 2,
        "name": "Unknown"
    }
])

df2 = spark.createDataFrame([
    {
        "id": 1,
        "city": "London"
    }
])


def test_union_anyway():
    df: DataFrame = df1.union_anyway(df2)
    assert ["id", "name", "city"] == df.columns
    assert 3 == df.count()
    assert df.head_as_dict() == {
        "id": 1,
        "name": "Ivan",
        "city": None
    }

