# Enterprise E-Commerce ETL Pipeline — Medallion Architecture

End-to-end data engineering pipeline correlating regional weather conditions 
with food delivery volumes and applying dynamic surge pricing. Processes 
100,000+ transactional records through a Bronze → Silver → Gold medallion 
architecture using PySpark for distributed processing and dbt Core + DuckDB 
for the analytics layer.

---

## What this solves

Food delivery platforms lose revenue by applying flat pricing regardless of 
weather conditions. This pipeline enriches transactional data with live 
weather signals and applies vectorised surge pricing at scale — without 
iterative loops.

---

## Architecture
Bronze (raw ingestion)
└── PySpark reads raw CSV → writes Parquet
Silver (enrichment + business logic)
└── PySpark joins orders × weather on city + date
└── Vectorised surge pricing engine (NumPy-style, Spark DataFrame API)
Rainy  → +25% revenue multiplier
Cloudy → +5%  revenue multiplier
Sunny  → standard pricing
Gold (aggregations)
└── dbt Core + DuckDB SQL models
└── Metrics: revenue by city, weather condition, surge uplift %
└── Schema tests via dbt (not_null, accepted_values)

---

## Tech stack

| Layer | Tool |
|---|---|
| Distributed processing | PySpark 3.5 |
| Analytics / Gold layer | dbt Core + DuckDB |
| Cloud migration | AWS S3 via boto3 |
| Serialisation | PyArrow (Parquet) |
| CI/CD | GitHub Actions + flake8 |
| Orchestration | Prefect-compatible subprocess runner |

---

## Repository structure
Enterprise_Weather_ETL/
├── src/
│   ├── data_generator.py       # Generates synthetic food delivery data
│   ├── transform_silver.py     # PySpark: join + surge pricing engine
│   ├── transform_gold.py       # Triggers dbt run
│   └── main.py                 # Pipeline orchestrator with checkpoints
├── ecom_gold_dbt/
│   ├── models/
│   │   └── gold_revenue_by_city.sql   # Final metrics model
│   ├── tests/                         # dbt schema tests
│   ├── dbt_project.yml
│   └── profiles.yml                   # DuckDB target
├── data/
│   ├── raw/                    # Bronze layer (Parquet)
│   ├── silver/                 # Enriched records with surge multipliers
│   └── gold/                   # metrics.duckdb
├── logs/
├── aws_migration.py            # Pushes Gold metrics to S3 Data Lake
├── requirements.txt
└── .github/
└── workflows/
└── ci.yml              # Lint + dbt parse on every push

---

## Performance

- **Volume:** 100,000+ transactional records
- **Runtime:** ~21 seconds end-to-end (Bronze → Gold)
- **Scalability:** PySpark runs distributed — scales horizontally 
  across nodes, not limited to single-machine memory

---

## Running locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run full pipeline
python src/main.py

# Run dbt Gold layer independently
cd ecom_gold_dbt
dbt run
dbt test
```

---

## CI/CD

GitHub Actions runs on every push:
- `flake8` lints all source files
- `dbt parse` validates all SQL models compile correctly

No broken code reaches main.
