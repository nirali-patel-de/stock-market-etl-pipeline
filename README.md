# Stock Market ETL Pipeline

An end-to-end stock market data engineering pipeline built using **Python, Docker, Hadoop HDFS, PySpark, Parquet, and DuckDB**.

## Project Goal

The objective of this project is to build and understand a complete data engineering pipeline using real stock market data.

The pipeline covers:

* Data extraction
* Raw data storage
* Distributed data processing
* Data cleaning and transformation
* Columnar data storage using Parquet
* Analytical querying using DuckDB

The project demonstrates a practical ETL workflow using the Hadoop and Spark ecosystem.

---

## Architecture

```text
Yahoo Finance
      │
      ▼
Python / yfinance
      │
      ▼
Raw CSV Files
      │
      ▼
HDFS Raw Layer
/stock-market/raw
      │
      ▼
PySpark ETL
      │
      ├── Schema inference
      ├── Data cleaning
      ├── Duplicate removal
      ├── Date conversion
      ├── Ticker extraction
      └── Source file tracking
      │
      ▼
Parquet
      │
      ▼
HDFS Processed Layer
/stock-market/processed
      │
      │ Local analytical copy
      ▼
data/processed/stock_market.parquet
      │
      ▼
DuckDB
      │
      ▼
SQL Analytics
```

---

## Technologies

* **Python** — Data extraction and project scripting
* **yfinance** — Stock market data extraction from Yahoo Finance
* **Hadoop HDFS** — Distributed raw and processed data storage
* **PySpark** — Data transformation and ETL processing
* **Parquet** — Columnar storage format for processed data
* **DuckDB** — Analytical SQL query engine
* **Docker** — Containerized Hadoop and Spark environment
* **Ubuntu / WSL** — Development environment
* **Git / GitHub** — Version control and project portfolio

---

## Data Flow

### 1. Data Extraction

Stock market data is downloaded using Python and `yfinance`.

Currently, the pipeline processes:

* RELIANCE.NS
* TCS.NS
* INFY.NS

The extracted data is stored as CSV files in the local raw data directory.

```text
data/raw/

├── INFY_NS.csv
├── RELIANCE_NS.csv
└── TCS_NS.csv
```

---

### 2. HDFS Raw Layer

The raw CSV files are uploaded into the HDFS raw layer:

```text
/stock-market/raw/
```

HDFS provides the distributed storage layer for the pipeline.

The original CSV files are preserved in the raw layer before transformation.

---

### 3. PySpark ETL

PySpark reads the raw CSV files from HDFS and performs the ETL transformation process.

The transformation includes:

* Schema inference
* Date conversion
* Ticker extraction from source filenames
* Source file tracking
* Duplicate removal
* Null value removal

The result is a cleaned and standardized dataset ready for analytical processing.

---

### 4. Processed Parquet Layer

The transformed dataset is written to HDFS in **Parquet** format:

```text
/stock-market/processed/
```

Parquet is used because it is a columnar storage format that is well suited for analytical workloads and efficient data processing.

---

### 5. DuckDB Analytics

A local copy of the processed Parquet dataset is maintained for analytical querying:

```text
data/processed/stock_market.parquet
```

DuckDB is used as the analytical SQL engine to query the processed Parquet dataset and perform SQL-based analysis.

Current analytics include:

* Dataset overview
* Records per stock
* Basic price statistics
* Daily returns
* Price performance
* Trading volume analysis

---

## Project Status

### Completed

* [x] Repository created
* [x] Project structure created
* [x] Docker environment configured
* [x] Hadoop NameNode configured
* [x] Hadoop DataNode configured
* [x] HDFS connectivity verified
* [x] Yahoo Finance data extraction
* [x] Raw CSV data created
* [x] Raw data uploaded to HDFS
* [x] PySpark ETL pipeline developed
* [x] Data cleaning and transformation implemented
* [x] Parquet output generated
* [x] Processed data stored in HDFS
* [x] HDFS → local Parquet analytical copy created
* [x] DuckDB installed and configured
* [x] DuckDB successfully reading Parquet
* [x] Basic SQL analytics implemented
* [x] Calculate daily returns
* [x] Analyze price performance
* [x] Analyze trading volume

---

## Running the Pipeline

### Prerequisites

Make sure Docker and the project environment are available before running the pipeline.

### 1. Extract Stock Data

From the project root:

```bash
python -m scripts.extract_stock_data
```

This downloads the stock market data and stores the raw CSV files locally.

### 2. Upload Raw Data to HDFS

```bash
python -m scripts.upload_to_hdfs
```

This uploads the raw CSV files into the HDFS raw layer.

### 3. Run PySpark Transformation

The transformation runs inside the Spark Docker container:

```bash
docker exec spark bash -c \
'cd /app && PYTHONPATH=/app /opt/spark/bin/spark-submit scripts/transform_stock_data.py'
```

This reads the raw data from HDFS, applies the transformations, and writes the processed dataset as Parquet to HDFS.

### 4. Copy Processed Parquet for Local Analytics

The processed Parquet dataset generated in HDFS is copied to the local processed-data directory for DuckDB analysis:

```text
data/processed/stock_market.parquet
```

### 5. Run DuckDB Analysis

```bash
python analysis/stock_analysis.py
```

DuckDB reads the local Parquet dataset and executes the analytical SQL queries.

---

## HDFS Data Layers

### Raw Layer

```text
/stock-market/raw/
```

Contains the original extracted CSV files.

### Processed Layer

```text
/stock-market/processed/
```

Contains the transformed Parquet dataset generated by PySpark.

This separation provides a simple **raw → processed** data lake structure.

---

## Current Pipeline

```text
Python / yfinance
        ↓
      CSV
        ↓
      HDFS
        ↓
    PySpark
        ↓
    Parquet
        ↓
      HDFS
        ↓
Local Parquet Copy
        ↓
    DuckDB
        ↓
  SQL Analytics
```

---

## Future Improvements

Potential improvements include:

* Increase dataset volume
* Add more stocks and market instruments
* Add partitioning to the Parquet dataset

---

## Key Learning Outcomes

Through this project, the following data engineering concepts are demonstrated:

* Building an end-to-end ETL pipeline
* Working with Hadoop HDFS
* Separating raw and processed data layers
* Processing data using PySpark
* Performing data cleaning and transformation
* Working with Parquet columnar storage
* Querying Parquet data using SQL
* Using Docker for distributed-data infrastructure
* Working with Linux/WSL development environments
