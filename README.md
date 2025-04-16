# 📊 ELT Customer Churn Pipeline

An end-to-end ELT pipeline to ingest customer churn CSV data, transform, validate, and visualize using open-source tools.

---

[ELT Pipeline]

---

## 🛠 Tech Stack

- **Language**: Python 3.10
- **Orchestration**: Apache Airflow
- **Data Warehouse**: PostgreSQL
- **Transformations**: DBT (Data Build Tool)
- **Validation**: Great Expectations
- **Visualization**: Metabase
- **Containerization**: Docker + Docker Compose

---

## 📁 Project Structure

```
.
├── airflow/                 # DAGs and scripts
├── data/                   # Input CSV
├── dbt_churn/              # DBT models and project config
├── scripts/                # SQL schema creation
├── data_validation/        # GE scripts and expectations
├── Dockerfile              # Image setup
├── docker-compose.yaml     # Service definitions
├── .env                    # Environment variables
├── README.md               # Project documentation
└── run_ge_validation.py    # Script to validate staging
```

---

## 🚀 How to Run the Project

### ✅ Prerequisites

- Docker Desktop
- Visual Studio Code
- pgAdmin / DBeaver (optional for PostgreSQL GUI)

---

### 🧰 Setup & Start

```bash
# Clone or extract project
cd churn_pipeline_project

# Make sure .env is configured
cp .env.example .env

# Place the CSV file
mv customer_churn_data.csv data/

# Build and launch containers
docker compose up --build
```

---

## ✅ Using the Tools

### 1. **Airflow**
- URL: http://localhost:8080
- First time? Create user via:
```bash
docker exec -it <airflow_container> airflow users create ...
```
- Trigger `churn_pipeline_dag`

### 2. **DBT**
```bash
docker exec -it <airflow_container> bash
cd dbt_churn
dbt run
```

### 3. **Great Expectations**
```bash
docker exec -it <airflow_container> python run_ge_validation.py
```

### 4. **PostgreSQL Validation**
```bash
docker exec -it <postgres_container> psql -U airflow -d churn_dw

-- Check staging
SELECT * FROM staging.churn_raw LIMIT 5;
-- Check production
SELECT * FROM production.fact_churn_customer LIMIT 5;
```

### 5. **Metabase**
- URL: http://localhost:3000
- Connect to DB:
  - Host: `postgres`
  - DB: `churn_dw`
  - User: `airflow` / Password: `airflow`

---

## ✅ Data Validations (GE)

| Column       | Expectation                     |
|--------------|----------------------------------|
| `customerid` | Not null                         |
| `age`        | Between 18 and 100               |
| `churn`      | One of ['Yes', 'No']             |

---

## 📈 Sample Dashboards

Use Metabase to create:
- Churn rate by gender
- MonthlyCharges distribution
- Tenure & Churn relationship
- ContractType vs Churn

---

## ✅ Deployment Notes

- To reset Postgres:
```bash
docker compose down -v
```
- To rebuild from scratch:
```bash
docker compose up --build
```

---

## 🧪 Tests and Improvements

- Add `dbt test` assertions
- Schedule `dbt run` after Airflow DAG
- Create Metabase templates for quick dashboarding