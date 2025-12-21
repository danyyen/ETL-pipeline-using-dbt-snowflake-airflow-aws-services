# ETL Pipeline Using dbt, Snowflake, Airflow & AWS Services

This repository contains a **production-style ELT data platform** built to transform raw data into **trusted, analytics-ready datasets** using modern data engineering best practices.

---

## Data Engineering ELT Platform

[![Airflow](https://img.shields.io/badge/Orchestration-Apache_Airflow-017CEE?style=flat&logo=apache-airflow)](https://airflow.apache.org/)
[![dbt](https://img.shields.io/badge/Transformation-dbt-FF694B?style=flat&logo=dbt)](https://www.getdbt.com/)
[![Snowflake](https://img.shields.io/badge/Warehouse-Snowflake-29B5E8?style=flat&logo=snowflake)](https://www.snowflake.com/)
[![AWS](https://img.shields.io/badge/Cloud-AWS-232F3E?style=flat&logo=amazon-aws)](https://aws.amazon.com/)

---

## Overview

This repository contains a **production-style ELT data platform** built to transform raw Netflix data into **trusted, analytics-ready datasets**.  
The project mirrors real-world enterprise data team workflows, emphasizing **orchestration, testing, observability, and reliability** over ad-hoc scripts.

---

## Problem Statement

Analytics initiatives often fail due to:

- **Unreliable raw data** with no validation
- **Tight coupling** between transformations and reporting
- **Lack of observability**, alerts, and failure handling

**Goal:**  
Implement a **scalable, testable ELT pipeline** that delivers consistent, production-level reliability and trusted analytics outputs.

---

## Architecture

The pipeline follows a **modern cloud-native ELT architecture**:

![architecture](https://github.com/user-attachments/assets/9a4828ec-83a0-4c32-aa4c-4a1f834cd970)

### High-Level Flow

1. **Storage:** Raw data lands in **Amazon S3**
2. **Ingestion:** Python logic loads data into **Snowflake** (Raw / Staging schemas)
3. **Transformation:** **dbt** modular modeling (Staging → Intermediate → Marts)
4. **Orchestration:** **Apache Airflow** manages task dependencies and sensors
5. **Monitoring:** **AWS SNS** & **Slack** notifications on task failure
6. **Analytics:** Final datasets exposed for **Power BI**, **AWS QuickSight**, and SQL analytics

---

## Tech Stack

| Layer | Tools |
|------|------|
| **Cloud Infrastructure** | AWS (S3, SNS, IAM, SSM) |
| **Data Warehouse** | Snowflake |
| **Transformations** | dbt (models, tests, docs, lineage) |
| **Orchestration** | Apache Airflow |
| **Languages** | Python, SQL (Snowflake Dialect) |
| **Analytics** | Power BI |

---

## Orchestration (Apache Airflow)

The end-to-end workflow is managed by **Apache Airflow**, ensuring the pipeline is **reliable, idempotent, and observable**.

- **S3 Event Sensors:**  
  Uses `reschedule` mode to efficiently wait for `credits.csv` and `titles.csv` in the S3 landing zone before triggering downstream tasks.

- **Resilient Error Handling:**  
  Tasks are configured with automated retries and a **5-minute exponential backoff** to handle transient failures.

- **Proactive Alerting:**  
  Integrated Slack callbacks provide real-time visibility into pipeline health, sending instant notifications for task successes or failures.

---

## 🔧 Transformations (dbt)

Data transformation is handled using **dbt**, following modern **Analytics Engineering** principles:

- **Modular Architecture**
  - `Staging`: Data cleaning and type casting
  - `Intermediate`: Business logic and joins
  - `Marts`: Analytics-ready fact and dimension tables

- **Data Quality Gates**
  - dbt tests for `not_null`, `unique`, and `referential integrity`
  - Ensures only trusted data reaches analytics consumers

- **Visual Lineage**
  - Auto-generated dependency graphs enable impact analysis and easier debugging

---
## Business Insights Demonstrated

This ELT framework delivers **high-fidelity, analytics-ready data** that empowers stakeholders to uncover actionable insights, including:

- **Content Strategy**  
  Distribution analysis of content volume segmented by production type and genre.

- **Temporal Trends**  
  Deep dives into Netflix production trends over time to identify shifts in content strategy and market demand.

- **Data Health Scoring**  
  Monitoring data quality coverage and dbt test pass rates to ensure *Trusted Data* status across analytics models.

---

## Future Repository Roadmap

Planned enhancements to further mature the platform include:

- **CI/CD Integration**  
  Automate dbt testing and documentation deployment using **GitHub Actions** to enforce quality gates before production releases.

- **Advanced Validation**  
  Integrate **Great Expectations** for deeper statistical data profiling, anomaly detection, and data drift monitoring.

- **Containerization**  
  Migrate the Airflow environment to **Docker** (using Docker Compose) to improve portability, reproducibility, and local development consistency.

- **Containerization:**  
  Migrate the Airflow environment to **Docker** (using Docker Compose) to improve portability, reproducibility, and local development consistency.


## Repository Structure (As Deployed)

```bash
.
├── airflow-code/
│   ├── DAGS/
│   │   ├── Netflix_Data_Analytics.py   # Main Airflow DAG
│   │   ├── alerting/                   # Failure notification logic
│   │   ├── source_load/                # Ingestion helpers
│   │   └── readme.md
│   ├── config/
│   ├── plugins/
│   └── README.md
│
├── dbt_etl_code/
│   ├── dbt_project.yml
│   ├── models/
│   │   ├── example/
│   │   └── netflix/                    # Analytics-ready models
│   ├── macros/
│   ├── snapshots/
│   ├── seeds/
│   ├── tests/
│   │   └── SHOW_DETAILS_NOT_NULL.sql
│   ├── analyses/
│   ├── datasets/                       # Public Netflix CSVs
│   └── README.md
│
├── Result_Deliverables_images/
├── .gitignore
└── README.md


---
 
