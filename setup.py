from setuptools import find_packages, setup

setup(
    name="spark",
    packages=find_packages(exclude=["spark_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "dagster-spark",
        "dagster-pyspark",
        "duckdb",
        "pandas",
        "dagster-duckdb-pyspark",
        "dagster-duckdb",
    ],
    extras_require={"dev": ["dagster-webserver", "pytest", "pre-commit"]},
)
