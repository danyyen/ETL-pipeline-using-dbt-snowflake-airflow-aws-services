# Analytics ELT Pipeline  
### dbt, Snowflake, Airflow & AWS

## Overview

Many analytics teams struggle with unreliable data, tightly coupled transformations, and fragile pipelines that break silently. These issues slow down analysis, reduce trust in metrics, and make it difficult to scale data usage across teams.

This project demonstrates how to build an **analytics-focused ELT pipeline** that transforms raw data into **trusted, analytics-ready datasets**, using modern data engineering and analytics engineering practices. The emphasis is on **data reliability, clarity, and decision readiness**, rather than infrastructure complexity.

---

## Problem Context

Analytics initiatives commonly fail due to:
- Raw or poorly validated data reaching dashboards and models  
- Transformation logic tightly coupled to reporting layers  
- Limited visibility into pipeline health and failures  

The goal of this project is to show how these challenges can be addressed using a modular ELT design that supports **iteration, testing, and observability**.

---

## What This Pipeline Delivers

- Clear separation between raw, transformed, and analytics-ready data  
- Reproducible and testable transformations using dbt  
- Automated orchestration with dependency management  
- Basic observability through alerts and retries  
- Datasets ready for BI tools and ad-hoc analytics  

This mirrors the needs of real analytics teams where **trust and consistency matter as much as speed**.

---

## High-Level Architecture

1. **Data Landing**  
   Raw CSV data is stored in Amazon S3.

2. **Ingestion**  
   Python logic loads raw data into Snowflake staging schemas.

3. **Transformation**  
   dbt models transform data from staging → intermediate → analytics marts.

4. **Orchestration**  
   Apache Airflow manages dependencies and execution order.

5. **Monitoring & Alerts**  
   Failures trigger notifications via AWS SNS and Slack.

6. **Analytics Consumption**  
   Final datasets are exposed for Power BI, QuickSight, and SQL analysis.

---

## Key Design Decisions

### ELT over ETL
Raw data is loaded into Snowflake first, allowing transformations to leverage the warehouse’s scalability and keeping ingestion logic simple and flexible.

### dbt for Transformations
dbt enables modular SQL models, built-in testing, and lineage tracking, making transformations easier to reason about and maintain over time.

### Orchestration with Airflow
Airflow coordinates ingestion and transformation steps, ensuring downstream tasks only run when prerequisites are met.

### Observability by Default
Basic alerting provides visibility into pipeline failures, helping teams respond quickly and maintain trust in the data.

---

## Transformations (dbt)

The dbt project follows a layered analytics-engineering structure:

- **Staging models**  
  Basic cleaning, type casting, and standardization

- **Intermediate models**  
  Business logic, joins, and derived fields

- **Marts**  
  Analytics-ready fact and dimension tables designed for reporting and analysis

Data quality checks include:
- `not_null`
- `unique`
- referential integrity tests  

Only validated data is promoted to analytics consumers.

---

## Orchestration (Apache Airflow)

The pipeline is orchestrated using Apache Airflow with an emphasis on reliability and clarity:

- Sensors wait for source data availability in S3  
- Tasks are retried automatically with backoff  
- Slack notifications provide visibility into task success or failure  

This setup reflects how analytics pipelines are commonly managed in production environments without unnecessary complexity.

---

## Resulting Analytics Use Cases

The final datasets enable analyses such as:

- **Content Strategy**  
  Distribution of content by genre or production type

- **Temporal Trends**  
  Understanding how content production evolves over time

- **Data Quality Monitoring**  
  Visibility into test coverage and validation success rates

The focus is on enabling **consistent, repeatable analytics**, not one-off analysis.

---

## Tools & Technologies

- **Languages:** Python, SQL  
- **Transformations:** dbt  
- **Warehouse:** Snowflake  
- **Orchestration:** Apache Airflow  
- **Cloud Services:** AWS (S3, SNS, IAM), Slack 
- **Analytics:** Power BI, AWS QuickSight  

---

## Project Structure

```bash
.
├── airflow-code/
│   ├── DAGS/
│   │   ├── Netflix_Data_Analytics.py
│   │   ├── alerting/
│   │   ├── source_load/
│   └── config/
│
├── dbt_etl_code/
│   ├── models/
│   │   └── netflix/
│   ├── tests/
│   ├── macros/
│   └── datasets/
│
├── Result_Deliverables_images/
└── README.md
```

## What I Would Improve Next

If this pipeline were extended further, the next iterations would focus on:

- **CI/CD for Data Quality**  
  Add automated dbt model and test execution using CI/CD (e.g., GitHub Actions) to enforce quality gates before changes are promoted.

- **Deeper Data Validation**  
  Expand validation using statistical profiling and anomaly detection to catch subtle data issues beyond schema-level checks.

- **Containerized Development**  
  Introduce Docker and Docker Compose to standardize local development and improve reproducibility across environments.

- **Incremental & Scalable Models**  
  Explore incremental dbt models to improve performance and scalability as data volumes grow.

---


## Why This Project Matters

This project reflects how analytics pipelines are built and used in practice — emphasizing **clarity, reliability, and trust** over technical novelty. It highlights how thoughtful data engineering and analytics engineering choices directly influence the quality, usability, and credibility of downstream analytics.

---

## About Me

I’m a data professional interested in building analytics systems that make data easier to trust and easier to use.  
Feel free to explore the code or reach out if you’d like to discuss the design decisions or trade-offs behind this project.
