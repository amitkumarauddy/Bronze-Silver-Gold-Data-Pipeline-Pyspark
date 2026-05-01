# PySpark Medallion Architecture Data Pipeline

## 📖 Project Overview
This project is an end-to-end batch processing data pipeline built with Apache Spark (PySpark) and Python. It processes over 11.2 million records of NYC Yellow Taxi transportation data, transforming raw data into business-ready analytical tables. 

The pipeline strictly adheres to the **Medallion Architecture (Bronze, Silver, Gold)** to guarantee data immutability, enforce data quality, and optimize storage using Snappy-compressed Parquet formats. The final reporting layer is modeled into a **Kimball Star Schema**, optimizing the data for high-performance Business Intelligence (BI) querying.

## 🏗️ Architecture Layering

*   **🥉 Bronze Layer (Raw Ingestion):** 
    *   Ingests raw `.parquet` files from the NYC Taxi dataset.
    *   Appends a programmatic `ingestion_timestamp` for data governance and lineage tracking.
    *   Stored in columnar Parquet format to optimize downstream I/O.
*   **🥈 Silver Layer (Cleansing & Conforming):**
    *   Reads from the Bronze layer and enforces Data Quality constraints.
    *   Removes exact duplicates.
    *   Filters out business anomalies (e.g., ghost passengers, negative trip distances, negative fare amounts). 
    *   *Result:* Successfully filtered out over 2.6 million corrupt/anomalous records.
*   **🥇 Gold Layer (Dimensional Modeling):**
    *   Transforms the denormalized Silver data into a Kimball Star Schema.
    *   Extracts time-based attributes into a dedicated Date Dimension table (`dim_date`).
    *   Centralizes quantifiable metrics and foreign keys into a core Fact table (`fact_trips`).
    *   Optimized for aggregation and dashboarding tools (PowerBI, Tableau).

## 🛠️ Tech Stack
*   **Language:** Python 3.x
*   **Data Processing:** Apache Spark (PySpark), Spark SQL DataFrame API
*   **Storage Format:** Apache Parquet (Columnar Storage)
*   **Architecture:** Medallion Data Lake, Dimensional Modeling (Star Schema)
*   **Environment Management:** `venv`, `pip`

## 📂 Project Structure
```text
nyc_taxi_pipeline/
│
├── data/                  # Git-ignored: Local data lake storage
│   ├── raw/               # Downloaded NYC TLC Trip Records
│   ├── bronze/            # Output of Bronze layer
│   ├── silver/            # Output of Silver layer
│   └── gold/              # Output of Gold layer (dim_date, fact_trips)
│
├── src/
│   ├── __init__.py        
│   ├── config.py          # Centralized configuration and absolute file paths
│   ├── spark_session.py   # Spark cluster initialization & memory management
│   ├── bronze.py          # Raw data ingestion logic
│   ├── silver.py          # Data cleansing and quality checks
│   └── gold.py            # Dimensional modeling transformations
│
├── main.py                # Master orchestrator script
├── requirements.txt       # Project dependencies
└── README.md

🚀 Setup and Execution
1. Prerequisites
Python 3.8+

Java 8 or 11 (Required for Apache Spark)

(Windows Users Only): Requires winutils.exe and hadoop.dll configured in the system PATH or injected dynamically at runtime.

2. Installation
Clone the repository and set up a virtual environment:

git clone [https://github.com/yourusername/nyc_taxi_pipeline.git](https://github.com/yourusername/nyc_taxi_pipeline.git)
cd nyc_taxi_pipeline
python -m venv venv

# Activate virtual environment
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

pip install -r requirements.txt

3. Data Acquisition
Download 2-3 months of Yellow Taxi Trip Records (.parquet format) from the NYC TLC Trip Record Data Website.

Place the raw files inside the data/raw/ directory.

4. Run the Pipeline
Execute the master orchestrator to run the full pipeline from end-to-end:

python main.py

📊 Performance Metrics
Running locally with custom Spark memory configurations (4GB Driver/Executor limit), the pipeline processes the data with the following benchmarks:

Input Data: 11,198,026 rows

Data Quality Removals: 2,617,962 anomalous rows dropped

Output Data: 8,580,064 highly conformed rows

End-to-End Execution Time: ~1.26 minutes

***

### CRITICAL: Before you push to GitHub!
You must create a `.gitignore` file. If you upload 150MB of raw Parquet files to GitHub, it will reject your push and mess up your repository history. 

Create a file named **`.gitignore`** in the root of your project and paste this inside:

```text
# Ignore local data lake
data/

# Ignore virtual environments
venv/
env/
.env

# Ignore compiled python files
__pycache__/
*.pyc

# Ignore Windows Hadoop binaries
hadoop/

