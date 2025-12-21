# ETL-pipeline-using-dbt-snowflake-airflow-aws-services
This repository contains a production-style ELT data platform built to transform raw data into trusted, analytics-ready datasets using modern data engineering best practices
# Data Engineering ELT Platform

[![Airflow](https://img.shields.io/badge/Orchestration-Apache_Airflow-017CEE?style=flat&logo=apache-airflow)](https://airflow.apache.org/)
[![dbt](https://img.shields.io/badge/Transformation-dbt-FF694B?style=flat&logo=dbt)](https://www.getdbt.com/)
[![Snowflake](https://img.shields.io/badge/Warehouse-Snowflake-29B5E8?style=flat&logo=snowflake)](https://www.snowflake.com/)
[![AWS](https://img.shields.io/badge/Cloud-AWS-232F3E?style=flat&logo=amazon-aws)](https://aws.amazon.com/)

## Overview
This repository contains a **production-style ELT data platform** built to transform raw Netflix data into trusted, analytics-ready datasets. The project mirrors real-world enterprise data team workflows — emphasizing orchestration, testing, and observability over ad-hoc scripts.

## Problem Statement
Analytics initiatives often fail due to:
* **Unreliable raw data** (no validation).
* **Coupling** between transformations and reporting.
* **Lack of observability** (no alerts).

**Goal:** Implement a scalable, testable ELT pipeline that delivers consistent, production-level reliability.

---

## Architecture
The pipeline follows a modern cloud-native architecture:
![architecture](https://github.com/user-attachments/assets/9a4828ec-83a0-4c32-aa4c-4a1f834cd970)


1.  **Storage:** Raw data landing in **Amazon S3**.
2.  **Ingestion:** Python logic moving data into **Snowflake** (Raw/Staging schemas).
3.  **Transformation:** **dbt** modular modeling (Staging → Intermediate → Marts).
4.  **Orchestration:** **Apache Airflow** managing task dependencies and sensors.
5.  **Monitoring:** **AWS SNS** & **Slack** notifications on task failure.
6.  **Analytics:** Final datasets exposed for **AWS QuickSIght** or **Power BI** and SQL analytics.



---

## Tech Stack

| Layer | Tools |
| :--- | :--- |
| **Cloud Infrastructure** | AWS (S3, SNS, IAM, SSM) |
| **Data Warehouse** | Snowflake |
| **Transformations** | dbt (models, tests, docs, lineage) |
| **Orchestration** | Apache Airflow |
| **Languages** | Python, SQL (Snowflake Dialect) |
| **Analytics** | Power BI |

---

## Orchestration (Apache Airflow)
The end-to-end workflow is managed by **Apache Airflow**, ensuring the pipeline is reliable, idempotent, and observable.

* S3 Event Sensors: Optimized for efficiency using `reschedule` mode, the pipeline dynamically waits for the arrival of `credits.csv` and `titles.csv` in the S3 landing zone before triggering.
* Resilient Error Handling: Tasks are configured with automated retries and a 5-minute exponential backoff to handle transient network or warehouse connection issues.
* Proactive Alerting: Integrated Slack callbacks provide real-time visibility into the pipeline health, sending instant notifications for task successes or failures.



---

##  Transformations (dbt)
Data transformation is handled by dbt, adhering to modern **Analytics Engineering** design patterns:

* **Modular Architecture:** The project follows a strictly tiered structure: 
    * `Staging`: Data cleaning and type casting.
    * `Intermediate`: Complex business logic and joins.
    * `Marts`: Final analytics-ready Fact and Dimension tables.
* Data Quality Gates: Automated schema and data validation are built directly into the CI/CD flow, utilizing dbt tests for `non-null`, `uniqueness`, and `referential integrity`.
* Visual Lineage: Auto-generated dependency graphs provide clear impact analysis, allowing for easier maintenance and debugging.



---

## Business Insights Demonstrated
This ELT framework delivers high-fidelity data that empowers stakeholders to uncover:

* Content Strategy: Distribution analysis of content volume segmented by production type and genre.
* Temporal Trends: Deep dives into Netflix production trends over time to identify market shifts.
* Data Health Scoring: Monitoring data quality coverage and test pass rates to ensure "Trusted Data" status.

---

## Future Roadmap
- CI/CD Integration: Automate dbt testing and documentation deployment via GitHub Actions.
- Advanced Validation: Integrate **Great Expectations** for deeper statistical data profiling and anomaly detection.
- Containerization: Migrate the Airflow environment to **Docker** (using Docker Compose) for better portability and local development consistency.
