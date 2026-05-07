# ⚡ Enterprise E-Commerce & Weather ETL Pipeline (Medallion Architecture)

## 📌 Executive Summary
This project is an end-to-end Data Engineering pipeline designed to solve a critical business problem: **Correlating regional weather conditions with food delivery volumes and implementing real-time revenue optimization.** By merging mock transactional data (100,000+ records) with external weather logs, the system calculates logistics delays and applies dynamic pricing.

## 🏗️ Architecture Design (Medallion Approach)
The system is built on a robust Medallion architecture to ensure data quality and FinOps optimization:

* 🥉 **Bronze Layer (Ingestion):** Raw transaction data and weather logs ingested into the landing zone.
* 🥈 **Silver Layer (Enrichment & Business Logic):** * Standardizes timestamps and performs an Enterprise Left Join on `City` and `Date`.
    * **Dynamic Surge Pricing Engine:** Implemented a vectorized pricing logic using NumPy to adjust revenue based on weather:
        * 🌧️ **Rainy:** +25% Surge (High Demand/Risk)
        * ☁️ **Cloudy:** +5% Surge
        * ☀️ **Sunny:** Standard Pricing
* 🥇 **Gold Layer (Business Aggregations):** Aggregates Silver data to generate final metrics for CEO Dashboards, focusing on `total_revenue` after surge adjustments.

## ⚙️ Tech Stack & Tooling
* **Data Processing:** Python, Pandas, NumPy (Vectorized Operations)
* **Storage Optimization:** PyArrow, Fastparquet (Parquet formatting)
* **Orchestration:** Custom Python Subprocess Orchestrator (`main.py`)
* **Environment:** Fully isolated via `venv` (PEP 668 compliance).

## 🚀 Performance Metrics
* **Volume Processed:** 100,000 transactional records.
* **Total Execution Time:** ~21.26 seconds (from extraction to Gold metrics).
* **Automation:** Full-cycle automation with built-in failure checkpoints.

## 📂 Repository Structure
```text
Enterprise_Weather_ETL/
├── data/
│   ├── raw/          # Bronze Layer
│   ├── silver/       # Silver Layer (Enriched with Surge Pricing)
│   └── gold/         # Gold Layer (Aggregated Metrics)
├── src/
│   ├── data_generator.py     
│   ├── transform_silver.py   # Now with Surge Logic
│   ├── transform_gold.py     
│   └── main.py               
└── README.md