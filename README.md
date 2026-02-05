# NASA Solar Weather Pipeline ☀️🛰️

## 1. Objective
Build an ELT pipeline to ingest NASA solar data, correlate Solar Flares with Geomagnetic Storms, and visualize the "Lag Time" to predict grid impact.

## 2. The Stack
* **Infrastructure:** Google BigQuery (Data Warehouse)
* **Language:** SQL (Standard SQL)
* **Visualization:** Looker Studio
* **Data Source:** NASA DONKI API (Coronal Mass Ejection & Geomagnetic Storm logs)

## 3. Key Technical Challenges
* **Non-Equi Joins:** Linked two disparate datasets (Flares and Storms) based on a sliding time window (Event B happens 2-5 days after Event A) rather than a common ID.
* **Data Cleaning:** Handled messy timestamps using `COALESCE` and `SAFE.PARSE_TIMESTAMP` to prevent pipeline failures.

## 4. The Insights
My analysis disproved the hypothesis that stronger (X-Class) flares travel significantly faster than weaker ones.
* **Average Travel Time:** ~62 hours regardless of intensity.
* **Safest Buffer:** 45% of storms take 70+ hours to arrive, giving grid operators a 3-day warning.

## 5. The Dashboard
*(Screenshot of finished product to come!)*

<img width="1283" height="951" alt="1a1bae0f-9e41-4573-998d-8dce0cd8c344" src="https://github.com/user-attachments/assets/95f02054-d3f2-4d5e-b26e-84818c9097ac" />
<img width="1070" height="716" alt="13debbf7-7489-41b1-a1de-9b83ce9e043d" src="https://github.com/user-attachments/assets/8a6eb498-9460-4489-bbee-73438753591c" />
<img width="1070" height="716" alt="b31f92f5-50d3-41eb-bb2d-1767aae0d9cb" src="https://github.com/user-attachments/assets/7b8d2921-6366-4f17-afa4-147731b8d428" />
