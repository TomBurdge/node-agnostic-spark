from dagster import Definitions, load_assets_from_modules

import spark.alt_assets as assets_module

# from .assets import analyse, read
from .io import DuckSparkParquetIOManager

assets = load_assets_from_modules([assets_module])
defs = Definitions(
    assets=assets,
    # can have dictionary with if else logic here
    resources={"io_manager": DuckSparkParquetIOManager()},
)

# from .io import PySparkParquetIOManager

# assets = load_assets_from_modules([assets_module])
# defs = Definitions(
#     assets=assets,
#     resources={"io_manager": PySparkParquetIOManager()},
# )
