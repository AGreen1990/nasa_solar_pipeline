# CACTus Solar Weather Pipeline ☀️🛰️

## 1. Objective
Build an ELT pipeline to ingest NASA solar data, correlate Solar Flares with Geomagnetic Storms, and visualize the "Lag Time" to predict grid impact.

## 2. The Stack
* **Infrastructure:** Google BigQuery (Data Warehouse)
* **Language:** SQL (Standard SQL)
* **Visualization:** Looker Studio
* **Data Source:** CACTus (Computer Aided CME Tracking) database developed by Solar Influences Data Center at the Royal observatory of Belgium. 


## 3. Key Technical Challenges
* **Non-Equi Joins:** Linked two disparate datasets (Flares and Storms) based on a sliding time window (Event B happens 2-5 days after Event A) rather than a common ID.
* **Data Cleaning:** Handled messy timestamps using `COALESCE` and `SAFE.PARSE_TIMESTAMP` to prevent pipeline failures.

## 4. The Insights
My analysis disproved the hypothesis that stronger (X-Class) flares travel significantly faster than weaker ones.
* **Average Travel Time:** ~62 hours regardless of intensity.
* **Safest Buffer:** 45% of storms take 70+ hours to arrive, giving grid operators a 3-day warning.

## 5. The Dashboard
*(Screenshot of finished product to come!)*


