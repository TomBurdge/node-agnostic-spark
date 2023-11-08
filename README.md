# PySpark: The Industry Standard DataFrame API for Data Engineering

PySpark is recognized as the go-to DataFrame API for data engineering. 

Traditional PySpark is particularly well suited for scaling to massive datasets. However, PySpark not as efficient for smaller datasets. Here's why:

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

Advocates for Spark and Polars argue they're faster and leaner than Spark. But in scenarios where data sizes unpredictably double, vertical scaling (e.g., more RAM) may not be viable.

Allowing for horizontal scaling with Spark, requiring minimal code adjustments, is prudent. It prevents the need for extensive refactoring for the occasional pipelines that do need Spark.

### DuckDB as a Spark Accelerator:

MotherDuck has discussed using DuckDB to enhance Spark's speed:
[Making PySpark Code Faster with DuckDB](https://motherduck.com/blog/making-pyspark-code-faster-with-duckdb/)

Their demonstration showcases the potential in toy scenarios. But how about more complex, realistic ETL pipelines that are indifferent to running on single machines with DuckDB or distributed through Spark?

### Objectives of This Repository:

This repo seeks to demonstrate that:
- Identical codebases can be deployed to either a single-node container or a Spark cluster.
- Application-specific environment variables, which can be set through a Terraform file, dictate the initiation of a DuckDB spark session or a genuine Spark session.
- This dual compatibility facilitates the use of both DuckDB and PySpark in real-world scenarios with zero code changes.

> **Warning**: The DuckDB Spark API is currently experimental and not recommended for production use.
