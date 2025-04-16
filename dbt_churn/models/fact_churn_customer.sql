{{ config(materialized='table') }}
SELECT 
  md5(cast("CustomerID" as text)) as customer_key,
  CASE WHEN "Gender" = 'Male' THEN 'M' ELSE 'F' END as gender,
  "Age",
  "Tenure",
  "MonthlyCharges",
  "TotalCharges",
  "ContractType",
  "InternetService",
  "TechSupport",
  "Churn"
FROM staging.churn_raw