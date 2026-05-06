# ⚡ Enterprise E-Commerce & Weather ETL Pipeline (Medallion Architecture)

## 📌 Executive Summary
This project is an end-to-end Data Engineering pipeline designed to solve a critical business problem: **Correlating regional weather conditions with food delivery volumes, revenue, and logistical delays.** By merging mock transactional data (100,000+ records) with external weather data, the pipeline generates actionable business metrics for the executive dashboard.

## 🏗️ Architecture Design (Medallion Approach)
The system is built on a robust Medallion architecture to ensure data quality, scalability, and FinOps optimization:

* 🥉 **Bronze Layer (Ingestion):** Raw transaction data (`food_delivery_data.csv`) and weather logs (`weather_data.csv`) are ingested into the landing zone. 
* 🥈 **Silver Layer (Enrichment & Cleansing):** * Standardizes unstructured timestamps into ISO formats.
    * Performs an enterprise-grade Left Join on `City` and `Date` to merge transactions with weather conditions.
    * Executes feature engineering to calculate `delivery_duration` in minutes.
    * **FinOps Optimization:** Drops redundant columns and saves the enriched data in **Parquet format**, drastically reducing storage footprint and improving I/O read speeds.
* 🥇 **Gold Layer (Business Aggregations):** Aggregates the Silver data to generate final metrics grouped by `restaurant_city` and `weather_condition`. Calculates `total_orders`, `avg_delivery_duration`, and `total_revenue`.

## ⚙️ Tech Stack & Tooling
* **Data Processing:** Python, Pandas, Numpy
* **Storage Optimization:** PyArrow, Fastparquet (Parquet formatting)
* **Orchestration:** Custom Python Subprocess Orchestrator (`main.py`)
* **Environment:** Fully isolated via `venv` to prevent dependency conflicts (PEP 668 compliance).

## 🚀 Performance Metrics
* **Volume Processed:** 100,000 transactional records.
* **Total Execution Time:** ~21.26 seconds (from raw extraction to Gold metrics generation).
* **Automation:** The entire pipeline is automated via a master switch (`src/main.py`) with built-in failure checkpoints to prevent data corruption.

## 📂 Repository Structure
```text
Enterprise_Weather_ETL/
├── data/
│   ├── raw/          # Bronze Layer (CSVs)
│   ├── silver/       # Silver Layer (Enriched Parquet)
│   └── gold/         # Gold Layer (Aggregated Parquet)
├── src/
│   ├── data_generator.py     # Simulates transaction flow
│   ├── transform_silver.py   # Cleans and merges data
│   ├── transform_gold.py     # Aggregates business metrics
│   └── main.py               # Pipeline Orchestrator
└── README.md