import os

from dagster import ConfigurableIOManager
from duckdb.experimental.spark.sql import SparkSession

# from dagster_duckdb_pyspark import DuckDBPySparkIOManager

# class PySparkParquetIOManager(ConfigurableIOManager):
#     def _get_path(self, context):
#         return os.path.join(*context.asset_key.path)

#     def handle_output(self, context, obj):
#         obj.write.saveAsTable(self._get_path(context))

#     def load_input(self, context):
#         spark = SparkSession.builder.getOrCreate()
#         return spark.read.parquet(self._get_path(context.upstream_output))


class DuckSparkParquetIOManager(ConfigurableIOManager):
    def _get_path(self, context):
        return os.path.join(*context.asset_key.path)

    def handle_output(self, context, obj):
        obj.relation.to_parquet(self._get_path(context))

    def load_input(self, context):
        spark = SparkSession.builder.getOrCreate()
        return spark.read.parquet(self._get_path(context.upstream_output))
