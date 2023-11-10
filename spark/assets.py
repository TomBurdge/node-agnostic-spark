from dagster import asset

# from dagster_duckdb_pyspark import DuckDBPySparkIOManager
from duckdb.experimental.spark.sql import DataFrame, SparkSession
from duckdb.experimental.spark.sql.functions import avg, col, count

# from pyspark.sql import DataFrame, SparkSession
# from pyspark.sql.functions import avg, col, count


@asset
def read() -> DataFrame:
    spark = SparkSession.builder.getOrCreate()  # type: ignore
    # need to process completly, for no out of memory.
    # write my own transformation(s) and maybe a visualisation (streamlit?) tomorrow.
    return (
        spark.read.parquet("data/hacker_news_2021_2022.parquet")
        .filter((col("type") == "story") & (col("by") != "NULL"))
        .groupBy(col("by"))
        .agg(
            avg(col("score")).alias("average_score"),
            count(col("id")).alias("number_of_stories"),
        )
        .filter(col("number_of_stories") > 1)  # Filter users with more than one story
        .orderBy(
            col("number_of_stories").desc(), col("average_score").desc()
        )  # Order by the number of stories first, then by average score
        .limit(10)
    )


@asset
def analyse(read: DataFrame) -> DataFrame:
    return read
