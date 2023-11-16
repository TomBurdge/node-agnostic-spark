# PySpark: The Industry Standard DataFrame API for Data Engineering

PySpark is recognized as the go-to DataFrame API for data engineering. 

Traditional PySpark is particularly well suited for scaling to massive datasets. However, PySpark is a poor choice for smaller datasets. Here's why:

- Spark operates on a Java Virtual Machine, which introduces a significant overhead.
- Multi-node operations in Spark involve either complex infrastructure or relatively high costs for serverless environments (e.g., DataBricks, DataProc).
- Performance on single-node computing is suboptimal with Spark.
- For low latency requirements and medium-sized data, single machine alternatives can outperform Spark. One example for time series data is `functime`,
- The carbon emissions of computing are very high. Serverless spark almost always provisions with at least two nodes - in cases where this is greater than the use case needs, this is needless carbon emissions that contribute to the climate crisis.

Despite these drawbacks, many companies stick with Spark even for small data tasks due to familiarity with its well-crafted API.

## Scalable Alternatives to Spark for Single Machines:

For single-machine data engineering, the following stand out and are well integrated with PyArrow :
- **Polars**: Offers (experimental) streaming features to scale beyond memory datasets, uses lazy execution like Spark does, and has an API with a similar syntax to Spark.
- **DuckDB**: Has an experimental Spark API.

I've had a positive experience using Polars in my `tipitaka` repository and professionally, but this project focuses on DuckDB.

As DuckDB's Spark API matures and expands, it could become an ideal substitute for those accustomed to PySpark, especially where Spark isn't the most suitable tool.

Advocates for Spark and Polars argue they're faster and leaner than Spark. But in scenarios where data sizes unpredictably double, vertical scaling (e.g., more RAM) may not be viable or desirable.

Allowing for horizontal scaling with Spark, requiring minimal code adjustments, is prudent. It prevents the need for extensive refactoring for the occasional pipelines that do need distributed Spark.

### DuckDB as a Spark Accelerator:

MotherDuck has discussed using DuckDB to enhance Spark's speed:
[Making PySpark Code Faster with DuckDB](https://motherduck.com/blog/making-pyspark-code-faster-with-duckdb/)

Their demonstration showcases the potential in a toy scenario. 

MotherDuck point out that a DuckDB spark client can save costs by provisioning tests on just a single node.

But how about more complex, realistic ETL pipelines that are indifferent to running on single machines with DuckDB or distributed through Spark?

### DuckDB PySpark with an Orchestrator:

ETL pipelines (almost) always use an orchestrator in some form.

There are plenty of options for orchestrators. One great choice of orchestrator is [Dagster](https://github.com/dagster-io/dagster). 

Dagster is a particularly good choice because it [separates the IO code from the pipeline code](https://docs.dagster.io/concepts/io-management/io-managers). This is particularly useful, because you could switch between duckdb spark and true pyspark without changing the etl pyspark code.

In this repo there are three options for the pipeline io (this is still a WIP, not everything is quite finished):
* [Spark PySpark which saves to parquet for between each step](https://docs.dagster.io/integrations/spark) in the pipeline.
* [Spark PySpark, which saves to a duckdb file at each step](https://dagster.io/integrations/dagster-duckdb-pyspark) in the pipeline (WIP).
* DuckDB PySpark, which saves to a parquet between each step in the pipeline. 

Dagster typically pickles its objects between each asset, but you can't pickle a DuckDB spark or regular PySpark session. As a result, dagster loads the files as parquets at each step (ELTL data pipelines). Both Spark and DuckDB write to parquet very efficiently, although it is a little cumbersome (though not the end of the world) to initiate a spark session at each step with true PySpark. This also makes testing a bit less like "unit" tests, i.e. testing the most basic units of code, but this is no worse than any other orchestrator with Spark.

By default, the pyspark IO code is commented. I will refactor this soon to make it more accessible.

### Objectives of This Repository:

This repo seeks to demonstrate that:
- Near identical codebases can be deployed to either a single-node container or a Spark cluster.
- It is possible to begin developing pipelines without distributed spark by default and then scale up to true spark with only infrastructure changes, i.e. without changes to transformation logic.
- This dual compatibility facilitates the use of both DuckDB and PySpark in real-world scenarios with low and decoupled code changes.

> **Warning**: The DuckDB Spark API is currently experimental and not recommended for production use.
