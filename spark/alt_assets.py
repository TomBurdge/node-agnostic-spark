from dagster import asset

# from dagster_duckdb_pyspark import DuckDBPySparkIOManager
from duckdb.experimental.spark.sql import DataFrame, SparkSession
from duckdb.experimental.spark.sql.functions import (
    avg,
    col,
    count,
    regexp_replace,
)

# from pyspark.sql import DataFrame, SparkSession
# from pyspark.sql.functions import avg, col, count


@asset
def read() -> DataFrame:
    spark = SparkSession.builder.getOrCreate()  # type: ignore

    return (
        spark.read.parquet("data/hacker_news_2021_2022.parquet")
        .withColumn("cleaned_title", regexp_replace(col("title"), "[^a-zA-Z0-9 ]", ""))
        .filter((col("type") == "story") & (col("by") != "NULL"))
    )


@asset
def aggregate(read: DataFrame) -> DataFrame:
    return (
        (
            read.groupBy(col("by"))
            .agg(
                avg(col("score")).alias("average_score"),
                sum(col("score")).alias("total_score"),
                count(col("id")).alias("number_of_stories"),
            )
            .filter(col("number_of_stories") > 1)
        )
        .orderBy(col("number_of_stories").desc(), col("average_score").desc())
        .limit(10)
    )


@asset
def show(aggregate: DataFrame) -> None:
    aggregate.show()
