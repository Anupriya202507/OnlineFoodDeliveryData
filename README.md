🍔 Online Food Delivery Data Analysis
📌 Project Overview

This project analyzes an online food delivery dataset to understand customer behavior, delivery performance, sales trends, and business insights using Python (Pandas, Matplotlib, Plotly),SQL and Power BI.

The project includes:

Data Cleaning & Preprocessing
Feature Engineering
Exploratory Data Analysis (EDA)
KPI Dashboard
Business Insights
🛠️ Technologies Used
Python
Pandas
NumPy
Matplotlib
Plotly
SQL
Power BI
📂 Data Cleaning & Preprocessing

The following preprocessing steps were performed before analysis.

Date Conversion
Converted Order_Date to datetime datatype.
Missing Value Handling
Cancellation Reason
Missing values were replaced with "No Cancellation Reason".
Customer Age
Missing values were filled using proportion-based imputation because the data was uniformly distributed.
Final Amount
Negative values were replaced with 0.
Missing values were calculated using:
Final_Amount = Order_Value - Discount_Applied

If Discount_Applied = 0, then:

Final_Amount = Order_Value
Numeric Columns

Missing values were filled using the median for:

Delivery_Time_Min
Distance_km
Order_Value
Profit_Margin
Ratings

Delivery Rating

Filled using grouped averages wherever possible.
Cancelled orders have no delivery rating, so remaining missing values were filled with the median.

Restaurant Rating

Filled using grouped restaurant averages.
Categorical Columns

Filled missing values using the mode for:

Customer_Gender
City
Area
Cuisine_Type
Payment_Mode
Order_Status
Order_Time
Feature Formatting
Removed extra spaces using strip()
Standardized text using str.title()
Restaurant Rating Validation

Restaurant ratings were clipped between 1 and 5.

clip(1,5)
Outlier Detection
Checked all numeric columns.
No significant outliers were found.
⚙️ Feature Engineering

The following analytical columns were created.

1. Order Day Type

Created a new column:

Weekday
Weekend

using Order_Date.

2. Order Hour

Extracted hour from Order_Time.

Note: The Peak Hour indicator currently needs correction because all values are becoming 0.

3. Profit Margin Percentage

Calculated as:

(Profit_Margin / Order_Value) × 100
4. Delivery Performance Category

Created using:

pd.cut(
Delivery_Rating,
bins=[0,3,4,5],
labels=["Low","Medium","High"]
)
5. Customer Age Group

Customer ages were categorized into different age groups for analysis.

📊 Power BI Dashboard
KPI Cards

The dashboard includes:

Total Orders
Total Revenue
Average Order Value
Average Delivery Time
Total Profit
Average Customer Rating
Cancellation Rate
📈 Visualizations & Insights
1. Distribution of Order Value

Chart Used: Histogram / Bar Chart

Insight

Shows how order values are distributed across customers.
2. Distribution of Delivery Time

Chart Used: Histogram / Bar Chart

Insight

Helps understand delivery time distribution.
3. City-wise Order Analysis

Chart Used: Bar Chart

Insight

Hyderabad recorded the highest number of orders.
4. Cuisine-wise Order Analysis

Chart Used: Bar Chart

Insight

Indian cuisine was ordered the most.
5. Weekend vs Weekday Orders

Chart Used: Column Chart

Insight

Weekday orders are higher than weekend orders.
6. Distance vs Delivery Time

Chart Used: Scatter Plot

Insight

Distance does not show a strong relationship with delivery delay.
Delivery time is likely influenced by traffic, weather, and other operational factors.
7. Cancellation Reason Analysis

Chart Used: Bar Chart

Insight

"No Cancellation Reason" is the most common category.
8. Correlation Analysis

Chart Used: Correlation Heatmap

Insight

Shows positive and negative relationships among numeric features.
📌 Key Business Insights
Hyderabad generates the highest number of food orders.
Indian cuisine is the most popular.
Most orders are placed on weekdays.
Delivery delay is not strongly dependent on travel distance.
Most records have no cancellation reason.
No significant outliers were detected.
Customer age was uniformly distributed, making proportion-based imputation appropriate.
