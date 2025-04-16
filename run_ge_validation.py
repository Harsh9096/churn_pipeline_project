import great_expectations as ge
from sqlalchemy import create_engine
import os

# Connect to Postgres
engine = create_engine("postgresql://airflow:airflow@postgres:5432/churn_dw")

# Load data into Pandas
df = ge.read_sql("SELECT * FROM staging.churn_raw", engine)

# Create expectations
df.expect_column_values_to_not_be_null("customerid")
df.expect_column_values_to_be_between("age", 18, 100)
df.expect_column_values_to_be_in_set("churn", ["Yes", "No"])

# Validate
results = df.validate()

# Print summary
print(results)
