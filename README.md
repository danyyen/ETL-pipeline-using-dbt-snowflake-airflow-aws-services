# ETL Pipeline - dbt, Snowflake, Airflow & AWS Services

A production-style **ELT data platform** that transforms raw data into **trusted analytics-ready datasets** using industry-standard tooling.

This project demonstrates how to build a robust, scalable ELT pipeline using modern data engineering best practices, including orchestration, data quality testing, observability, and reliability.

---
## 📌 Project Overview

###  Objective

Analytics initiatives often fail due to:
- Unvalidated/raw data leading to unreliable analyses  
- Tight coupling between transformation logic and reporting layers  
- Lack of observability, alerts, and automated failure handling

**Goal:** Implement a scalable, testable ELT pipeline that delivers consistent, production-level reliability and trusted analytics outputs.
---
##  Architecture & Workflow

**High-Level Flow:**

1. **Storage:** Raw data lands in Amazon S3  
2. **Ingestion:** Python scripts load data into Snowflake (Raw → Staging)  
3. **Transformation:** dbt builds modular models (Staging → Intermediate → Marts)  
4. **Orchestration:** Apache Airflow DAG manages task dependencies  
5. **Monitoring:** Alerts via AWS SNS & Slack on failure  
6. **Analytics:** Final datasets are ready for BI tools (Power BI, QuickSight)

**Architecture Diagram:**  
![architecture](https://github.com/user-attachments/assets/9a4828ec-83a0-4c32-aa4c-4a1f834cd970)

## Key Design Decisions

- **ELT over ETL:**  
  Raw data is loaded into Snowflake first, allowing transformations to leverage the warehouse’s scalability and simplifying ingestion logic.

- **dbt for Transformations:**  
  dbt enforces modular, testable SQL models with built-in lineage, documentation, and data quality checks.

- **Event-Driven Orchestration:**  
  Airflow sensors ensure downstream processing only begins when source data is available, improving reliability and cost efficiency.

- **Observability by Default:**  
  Slack and SNS alerts provide immediate feedback on pipeline health, enabling faster incident response.


**Goal:**  
Implement a **scalable, testable ELT pipeline** that delivers consistent, production-level reliability and trusted analytics outputs.

---


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
| **Cloud Infrastructure** | AWS (S3, SNS, IAM, SSM), Slack |
| **Data Warehouse** | Snowflake |
| **Transformations** | dbt (models, tests, docs, lineage) |
| **Orchestration** | Apache Airflow |
| **Languages** | Python, SQL (Snowflake Dialect) |
| **Analytics** | Power BI |

---
## Getting Started

### 🔧 Prerequisites

Before running this project locally or in cloud:

- AWS account with S3 + SNS permissions  
- Snowflake account with proper roles + warehouses  
- Python ≥ 3.8  
- dbt installed (`pip install dbt-snowflake`)  
- Airflow installed and configured

### 📦 Setup

1. Clone the repository:  
   ```bash
   git clone https://github.com/danyyen/ETL-pipeline-using-dbt-snowflake-airflow-aws-services.git
   cd ETL-pipeline-using-dbt-snowflake-airflow-aws-services
Configure environment variables (Snowflake & AWS credentials)

Install requirements:
pip install -r requirements.txt

Initialize Airflow: airflow db init

   
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

##  Transformations/Pipeline component (dbt)

Data transformation is handled using **dbt**, following modern **Analytics Engineering** principles:

- **Modular Architecture**
  - `Staging`: Data cleaning and type casting
  - `Intermediate`: Business logic and joins
  - `Marts`: Analytics-ready fact and dimension tables

- **Data Quality Gates**
  - dbt tests for `not_null`, `unique`, and `referential integrity.`
  - Ensures only trusted data reaches analytics consumers

- **Visual Lineage**
  - Auto-generated dependency graphs enable impact analysis and easier debugging

---
## Result and Impact

This pipeline produces **trusted analytics datasets** that enable:

- **Content Strategy**  
  Content distribution by production type/genre

- **Temporal Trends**  
  Tracking production trends over time

- **Data Health Scoring**  
 Automated metrics coverage and dbt test pass rates
---

## Future Repository Roadmap

Planned enhancements to further mature the platform include:

- **CI/CD Integration**  
  Automate dbt testing and documentation deployment using **GitHub Actions** to enforce quality gates before production releases.

- **Advanced Validation**  
  Integrate **Great Expectations** for deeper statistical data profiling, anomaly detection, and data drift monitoring.

- **Containerization**  
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
 
