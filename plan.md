# Project Plan: End-to-End Sales Forecasting & Demand Intelligence System

## 📋 Main Tasks

- [x] **Task 1 — Data Loading, Merging & Deep Exploration**
  - [x] Load the Superstore Sales CSV
  - [x] Parse dates and extract time features
  - [x] Check for missing values, duplicates, and data type issues
  - [x] Aggregate daily sales into weekly and monthly totals
  - [x] Answer exploratory questions

- [x] **Task 2 — Time Series Analysis & Decomposition**
  - [x] Plot the overall monthly sales trend
  - [x] Apply Time Series Decomposition (trend, seasonality, residuals)
  - [x] Check for stationarity using the Augmented Dickey-Fuller (ADF) Test
  - [x] Apply differencing if needed

- [x] **Task 3 — Sales Forecasting using 3 Different Models**
  - [x] Model 1: SARIMA (Statistical Model)
  - [x] Model 2: Facebook Prophet (Industry-standard Forecasting Tool)
  - [x] Model 3: XGBoost for Time Series (ML-based Approach)
  - [x] Model Comparison Table and Recommendation

- [x] **Task 4 — Product Category & Region Level Forecasting**
  - [x] Run forecasts separately for specific categories (Furniture, Technology, Office Supplies) and regions (West, East)
  - [x] Plot all 5 forecasts together on one comparison chart
  - [x] Identify category/region with the strongest upcoming growth

- [x] **Task 5 — Anomaly Detection in Sales Data**
  - [x] Use Isolation Forest to detect anomalous sales weeks
  - [x] Apply Z-Score based detection
  - [x] Compare results from both anomaly detection methods

- [x] **Task 6 — Product Demand Segmentation using Clustering**
  - [x] Aggregate data at the product sub-category level
  - [x] Use K-Means Clustering and the Elbow Method to segment products
  - [x] Visualize clusters using a 2D scatter plot (PCA)
  - [x] Recommend stocking strategies per cluster

- [x] **Task 7 — Deployment: Interactive Dashboard using Streamlit**
  - [x] Build Page 1 — Sales Overview Dashboard
  - [x] Build Page 2 — Forecast Explorer
  - [x] Build Page 3 — Anomaly Report
  - [x] Build Page 4 — Product Demand Segments
  - [x] Deploy the app on Streamlit Community Cloud and submit the live link

- [x] **Task 8 — Executive Business Report**
  - [x] Produce a jargon-free 2-page executive summary (summary.docx)
  - [x] Include key findings, forecasts, anomalies, segmentation, and recommendations
