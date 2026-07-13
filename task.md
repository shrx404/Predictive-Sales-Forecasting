📋 **Internship Project — Week 3 & Week 4**  
 **Project Title:** End-to-End Sales Forecasting & Demand Intelligence System  
 **Assigned Date:** \[03/07/2026\] **Submission Date:** \[13/07/2026\]

---

🎯 **Problem Statement**  
 Every retail and e-commerce company — from Walmart and Amazon to D-Mart and Flipkart — lives and dies by one question: *"How much of each product will we sell next month, and will we have enough stock to meet that demand?"* Getting this wrong in either direction costs crores — overstock wastes storage and capital, understock loses sales and customers.

This is not a beginner classification problem. This is a **multi-layered, real industry problem** that requires you to work with time-series data (data ordered by date, not rows of independent customers), build and compare multiple forecasting models, detect anomalies in sales patterns, segment products by demand behavior, and deliver a working interactive dashboard that a business manager could open on Monday morning and make stocking decisions from.

You will touch **Time Series Analysis, Machine Learning, Forecasting, Anomaly Detection, Customer/Product Segmentation, and Deployment** — all in one project. This is the kind of system that data science teams at mid-to-large companies actually build and maintain.

**Your task:** Build an intelligent sales forecasting system that predicts future product demand, detects unusual sales spikes or drops, segments products by demand pattern, and presents everything through a deployed interactive dashboard.

---

📦 **Dataset — Where to Get It**  
 Go to this link and download the dataset:  
 🔗 [https://www.kaggle.com/datasets/rohitsahoo/sales-forecasting](https://www.kaggle.com/datasets/rohitsahoo/sales-forecasting)

Steps to download:

* Create a free account on [www.kaggle.com](http://www.kaggle.com) (if you don't have one)  
* Search for **"Superstore Sales Dataset"**  
* Download the file — it will be a .csv file named **train.csv**  
* Use the full dataset — it covers 4 years of daily sales data across multiple product categories and regions

**Supplementary Dataset (Required for Anomaly Detection Task):**  
 🔗 [https://www.kaggle.com/datasets/gregorut/videogamesales](https://www.kaggle.com/datasets/gregorut/videogamesales)  
 *(You will use this as a secondary dataset to practice merging and multi-source analysis — a real-world skill since no company keeps all its data in one file)*

---

✅ **Tasks to Complete**  
 Complete all the following tasks in a Jupyter Notebook (.ipynb):

---

**Task 1 — Data Loading, Merging & Deep Exploration**

* Load the Superstore Sales CSV using Pandas  
* Parse the **Order Date** and **Ship Date** columns as proper datetime objects  
* Extract time features: Year, Month, Week Number, Day of Week, Quarter, Season  
* Check for missing values, duplicates, and data type issues  
* Aggregate daily sales into **weekly and monthly totals** (you will need both granularities for different models)  
* Answer these questions in your notebook with data to back each one:  
  * Which product category generates the highest total revenue?  
  * Which region has the most consistent sales growth over 4 years?  
  * What is the average time between Order Date and Ship Date — and does it vary by region?  
  * Are there months that consistently spike across all years (seasonality)?

---

**Task 2 — Time Series Analysis & Decomposition**

* Plot the overall monthly sales trend across all 4 years  
* Apply **Time Series Decomposition** (using `statsmodels`) to break the sales signal into:  
  * Trend component  
  * Seasonal component  
  * Residual/noise component  
* Plot all 4 components clearly on one figure  
* Write 3–4 observations: what does the trend tell you? Is seasonality strong or weak? What months show the highest residual noise?  
* Check for **stationarity** using the **Augmented Dickey-Fuller (ADF) Test** — explain in plain English what stationarity means and what your test result tells you  
* Apply differencing if the series is non-stationary and re-test

---

**Task 3 — Sales Forecasting using 3 Different Models**

This is the core technical task. Build, train, and compare 3 fundamentally different forecasting approaches:

**Model 1 — SARIMA (Statistical Model)**

* Install statsmodels (`pip install statsmodels`)  
* Fit a SARIMA model on monthly sales  
* Choose appropriate (p, d, q) and seasonal (P, D, Q, m) parameters — document why you chose them  
* Generate a 3-month future forecast with confidence intervals  
* Plot actual vs forecasted sales

**Model 2 — Facebook Prophet (Industry-standard Forecasting Tool)**

* Install Prophet (`pip install prophet`)  
* Prepare data in Prophet's required format (ds, y columns)  
* Fit the model and generate a 3-month forecast  
* Plot the forecast with Prophet's built-in trend and seasonality breakdown  
* Extract and interpret the weekly and yearly seasonality components

**Model 3 — XGBoost for Time Series (ML-based Approach)**

* Convert the time series into a supervised ML problem using lag features:  
  * Lag 1 (sales from 1 month ago)  
  * Lag 2 (sales from 2 months ago)  
  * Lag 3 (sales from 3 months ago)  
  * Rolling mean (3-month moving average)  
  * Month, Quarter, Season as features  
* Train XGBoost Regressor on these features  
* Predict the next 3 months  
* Plot actual vs predicted

**Model Comparison Table (Required)**  
 Create a clear comparison table in your notebook:

| Model | MAE | RMSE | MAPE | Forecast for Month 1 | Forecast for Month 2 | Forecast for Month 3 |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| SARIMA |  |  |  |  |  |  |
| Prophet |  |  |  |  |  |  |
| XGBoost |  |  |  |  |  |  |

State clearly which model you would recommend for production use and why — based on numbers, not preference.

---

**Task 4 — Product Category & Region Level Forecasting**

* Repeat the best performing model (from Task 3\) separately for each of the following segments:  
  * Furniture category sales  
  * Technology category sales  
  * Office Supplies category sales  
  * West region sales  
  * East region sales  
* Plot all 5 forecasts together on one comparison chart  
* Write: which category/region is showing the strongest upcoming growth according to your model?

---

**Task 5 — Anomaly Detection in Sales Data**

* Use **Isolation Forest** (from scikit-learn) to detect anomalous sales weeks — weeks where sales were unusually high or unusually low compared to the expected pattern  
* Mark the anomalies on a time series plot (use a different color/marker for anomaly points)  
* For each detected anomaly, write a possible real-world explanation (e.g., "spike in November likely corresponds to a festive sale period")  
* Apply a second anomaly detection method: **Z-Score based detection** — flag any week where sales deviate more than 2 standard deviations from the rolling mean  
* Compare: do both methods flag the same anomalies, or do they disagree? What does this tell you?

---

**Task 6 — Product Demand Segmentation using Clustering**

* Aggregate data at the **product sub-category level** with features like:  
  * Total sales volume  
  * Sales growth rate (year-over-year)  
  * Sales volatility (standard deviation of monthly sales)  
  * Average order value  
* Apply **K-Means Clustering** to segment products into demand groups  
* Use the **Elbow Method** to find the optimal number of clusters  
* Label each cluster meaningfully, for example:  
  * High Volume, Stable Demand  
  * Low Volume, High Volatility  
  * Growing Demand  
  * Declining Demand  
* Plot clusters using a 2D scatter plot (use PCA to reduce to 2 dimensions if needed)  
* Write: what stocking strategy would you recommend for each cluster?

---

**Task 7 — Deployment: Interactive Dashboard using Streamlit**  
 Build a working Streamlit web app with the following features:

**Page 1 — Sales Overview Dashboard**

* Total sales by year (bar chart)  
* Monthly sales trend line chart  
* Sales by region and category (interactive filters)

**Page 2 — Forecast Explorer**

* Dropdown to select: Category or Region  
* Date range slider to select forecast horizon (1, 2, or 3 months ahead)  
* Display the forecast output from your best model for the selected inputs  
* Show MAE and RMSE of the model below the chart

**Page 3 — Anomaly Report**

* Display the anomaly chart from Task 5  
* List detected anomaly dates in a table with their sales values

**Page 4 — Product Demand Segments**

* Display the cluster chart from Task 6  
* Show which sub-categories belong to which demand cluster in a table

Deploy the app on **Streamlit Community Cloud** (free) and submit the live link.

---

**Task 8 — Executive Business Report**  
 Write a structured 2-page business report (in summary.pdf or summary.docx) as if you are presenting to the **Head of Supply Chain and the CFO** of a retail company. The report must include:

* A one-paragraph executive summary (no jargon)  
* Key findings from EDA and forecasting  
* The 3-month sales forecast with confidence ranges in plain language  
* Top 3 anomalies detected and their likely cause  
* Product demand segmentation findings and recommended stocking strategy per segment  
* 3 concrete business recommendations with data backing each one  
* One risk/limitation of this system that the business should be aware of

**This report must be readable by someone who has never opened Python.**

---

🛠️ **Tools & Libraries to Use**

| Tool | Purpose |
| ----- | ----- |
| Python 3.x | Main programming language |
| Jupyter Notebook / Google Colab | To write and run your code |
| Pandas & NumPy | Data loading, cleaning, feature engineering |
| Statsmodels | SARIMA model and time series decomposition |
| Prophet | Facebook's production-grade forecasting library |
| XGBoost | ML-based time series forecasting |
| Scikit-learn | Isolation Forest, K-Means, PCA, evaluation metrics |
| Matplotlib / Seaborn / Plotly | Static and interactive charts |
| Streamlit | Interactive dashboard deployment |
| Git & GitHub | Version control and code submission |

---

📁 **What to Submit**  
 Create a folder named: **SalesForecasting\_\[YourName\]**  
 Inside the folder, include:  
 ✅ analysis.ipynb — Complete Jupyter Notebook with all 8 tasks, with markdown explanations throughout  
 ✅ train.csv — The Superstore sales dataset used  
 ✅ app.py — Your Streamlit dashboard code as a separate Python file  
 ✅ requirements.txt — All Python libraries used (so the app can be re-deployed by anyone)  
 ✅ summary.pdf or summary.docx — 2-page executive business report  
 ✅ charts/ — All chart images saved as .png

Submit the entire folder as a ZIP file \+ paste your Google Colab link \+ paste your live Streamlit app link  
 Via: https://docs.google.com/forms/d/e/1FAIpQLSf7t2YhRzjpQi0CL4TtG6gjqGWZ168Rk047SmuPTAXlUB7Flw/viewform?usp=dialog

---

📊 **Evaluation Criteria**

| Criteria | Weightage |
| ----- | ----- |
| Time Series Analysis & Decomposition | 10% |
| Correct implementation of all 3 forecasting models | 20% |
| Model comparison with correct metrics & justified recommendation | 15% |
| Anomaly Detection (both methods) | 10% |
| Product Segmentation & Clustering quality | 10% |
| Streamlit Dashboard — functionality & usability | 15% |
| Executive Business Report — clarity & business relevance | 10% |
| Code quality, comments, notebook structure | 5% |
| GitHub repository & requirements.txt | 5% |

**Total: 100%**

---

⚠️ **Important Note for the Intern:**  
 This project is intentionally designed to be uncomfortable. You will encounter concepts you have not seen before — SARIMA parameters, Prophet's data format, converting time series into supervised ML features, PCA for visualization. That discomfort is the point. A real data science role at any company will hand you a problem you have never solved before on your first week. How you handle not knowing something — how you research, attempt, fail, adjust, and document — is what this final project is actually evaluating.

A working project with honest documentation of what you could not fully solve is worth far more than a perfect-looking notebook that was copied without understanding.

