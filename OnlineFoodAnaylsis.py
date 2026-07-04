import pandas as pd
from pandas.core import groupby
import numpy as np
from numpy._core.defchararray import strip
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import sqlalchemy as sqlalchemy
from sqlalchemy import create_engine


#-------------------------------------------------
#Dataset consists of 100,000 online food delivery orders
#-------------------------------------------------
df = pd.read_csv('C:\\Users\\ANUPRIYA\\Desktop\\DataScience\\DSProject\\OnlineFoodAnalysisProject\\ONINE_FOOD_DELIVERY_ANALYSIS.csv')

# Display basic summary stats
#print(df.describe())

#-------------------------------------------------
#Handling missing values using mean, median, or mode
#Removing or capping outliers (delivery time, order value)
#Correcting invalid values (ratings > 5, negative profit margin)
#Standardizing categorical values
#Ensuring logical consistency (e.g., cancelled orders vs ratings)
#-------------------------------------------------

#print(df.dtypes)
print(f'Duplicates in customer_id:{df.duplicated(subset=["Customer_ID"]).sum()}')
df.drop_duplicates(subset=["Customer_ID"],inplace=True)

df['Order_Date']=pd.to_datetime(df['Order_Date'],errors='coerce')
#print(df['Order_Date'].dtypes)

df.isnull().sum()

df['Cancellation_Reason'] = df['Cancellation_Reason'].fillna('No_cancellation_Reason')

Null_index=df[df['Customer_Age'].isnull()].index
Proportion=df['Customer_Age'].value_counts(normalize=True)
df.loc[Null_index,['Customer_Age']]=np.random.choice(Proportion.index,size=len(Null_index),p=Proportion.values)

numeric_columns = ["Delivery_Time_Min","Distance_km","Order_Value","Profit_Margin"]

for column in numeric_columns:

    if column in df.columns:

        df[column] = df[column].fillna(df[column].median())

if 'order_status' in df.columns:

    mask = df['order_status'].str.lower() == 'cancelled'

    df.loc[mask,'restaurant_rating'] = np.nan
    df.loc[mask,'delivery_rating'] = np.nan

df['Discount_Applied'] = df['Discount_Applied'].fillna(0)

df["Final_Amount"] = df["Final_Amount"].clip(lower=0)
df.loc[(df['Discount_Applied']== 0) & (df['Final_Amount'].isna()),"Final_Amount" ]=df['Order_Value']
df.loc[df['Final_Amount'].isna(),'Final_Amount']=(df['Order_Value'] -df['Discount_Applied'])

df['Delivery_Rating']=df.groupby('Delivery_Partner_ID')['Delivery_Rating'].transform(lambda x: x.fillna(round(x.mean(),1)))
df['Restaurant_Rating']=df.groupby('Restaurant_ID')['Restaurant_Rating'].transform(lambda x: x.fillna(round(x.mean(),1)))

df.dropna(subset=["Order_Date"], inplace=True)

categorical_columns = ["Customer_Gender","City","Area","Cuisine_Type","Payment_Mode","Order_Status"]

for column in categorical_columns:

    if column in df.columns:

        df[column] = df[column].fillna(df[column].mode()[0])

df["Order_Time"] = df["Order_Time"].fillna(df["Order_Time"].mode()[0])


peak_hourcounts = df['Peak_Hour'].value_counts()
Null_indexp=df[df['Peak_Hour'].isnull()].index
Proportionp=df['Peak_Hour'].value_counts(normalize=True)
df.loc[Null_indexp,['Peak_Hour']]=np.random.choice(Proportionp.index,size=len(Null_indexp),p=Proportionp.values)

for column in df.select_dtypes(include=['object', 'string']).columns:
   if column in df.columns:
      df[column]=df[column].astype(str).str.title().str.strip()


#for col in df.select_dtypes(include='object').columns:
 #   print('Column Name: ',col)
 #   print(sorted(df[col].unique()))
 #   print('----'*10)


df["Restaurant_Rating"] = df["Restaurant_Rating"].clip(1, 5)
df["Profit_Margin"] = df["Profit_Margin"].abs()


columns_to_check =  ["Delivery_Time_Min","Distance_km","Order_Value","Final_Amount","Profit_Margin"]

for col in columns_to_check:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)

    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    # Select outliers for the current column
    outliers = df[(df[col] < lower) | (df[col] > upper)]

    print(f"Column: {col}, Lower Limit: {lower:.2f}, Upper Limit: {upper:.2f}, Number of Outliers: {len(outliers)}")

#---------------------------------------------------------------------------------------
#Distribution of order values and delivery time
#City-wise and cuisine-wise order analysis
#Weekend vs weekday demand
#Distance vs delivery delay relationship
#Cancellation reasons analysis
#Correlation analysis among numeric features
#----------------------------------------------------------------------------------------

plt.figure(figsize=(8,5))
plt.hist(df["Order_Value"], bins=30)
plt.title("Distribution of Order Value")
plt.xlabel("Order Value")
plt.ylabel("Frequency")
plt.savefig("order_value_distribution.png")
plt.close()
#-----------------------------------------------------------------
plt.figure(figsize=(8,5))
plt.hist(df["Delivery_Time_Min"], bins=40)
plt.title("Distribution of Delivery_Time_Min")
plt.xlabel("Delivery_Time_Min")
plt.ylabel("Frequency")
plt.savefig("delivery_time_distribution.png")
plt.close()
#-------------------------------------------------------------
city_order_counts = df["City"].value_counts()
cuisine_order_counts = df["Cuisine_Type"].value_counts()

Order_counts=df[['City','Cuisine_Type']]
for col in Order_counts.columns:
    Count=df[col].value_counts()
    print(Count)
    plt.figure(figsize=(8,5))
    Count.plot(kind="bar")

    plt.title(f"{col} Wise Order Analysis")
    plt.xlabel(col)
    plt.ylabel("Number of Orders")
    plt.xticks(rotation=45)

    plt.savefig(f"{col}_wise_order_analysis.png")
    plt.close()

#-------------------------------------------------------
Order_demand = df['Order_Day'].value_counts()
Order_demand.plot(kind="bar", figsize=(6,4))

plt.title("Weekend vs Weekday Order Demand")
plt.xlabel("Order Day")
plt.ylabel("Number of Orders")

plt.savefig("weekend_vs_weekday_order_demand.png")
plt.close()
#--------------------------------------
plt.figure(figsize=(8,5))

plt.scatter(
    df["Distance_km"],
    df["Delivery_Time_Min"]
)

plt.xlabel("Distance (km)")

plt.ylabel("Delivery Time (Minutes)")

plt.title("Distance vs Delivery Time")

plt.savefig("distance_vs_delivery_time.png")
plt.close()

#-----------------------------------------------------------
cancel_reason = df["Cancellation_Reason"].value_counts()
cancel_reason.plot(
    kind="bar",
    figsize=(8,5)
)

plt.title("Cancellation Reasons")

plt.ylabel("Orders")

plt.xticks(rotation=45)

plt.savefig("cancellation_reasons.png")
plt.close()

#-----------------------------------------------------------
numeric_df = df.select_dtypes(include=["int64", "float64"])
numeric_corr = numeric_df.corr()
plt.figure(figsize=(10,8))

plt.imshow(numeric_corr)

plt.colorbar()

plt.xticks(
    range(len(numeric_corr.columns)),
    numeric_corr.columns,
    rotation=90
)

plt.yticks(
    range(len(numeric_corr.columns)),
    numeric_corr.columns
)

plt.title("Correlation Matrix")
plt.savefig("correlation_matrix.png")
plt.close()

#------------------------------------------------------------------------------------
#Feature Engineering Derived analytical columns: Order day type (Weekday / Weekend)
#Peak hour indicator
#Profit margin percentage
#Delivery performance categories
#Customer age groups
#------------------------------------------------------------------------------------
df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce')
df['Order_day_type']=np.where(df['Order_Date'].dt.day_of_week < 5,'Weekday','Weekend')


#-----------------------------------------------------------
df['Order_Time'] = pd.to_datetime(
    df['Order_Time'],
    format='%H:%M',
    errors='coerce'
)

df['Order_hour'] = df['Order_Time'].dt.hour

df['Profit_Margin_Percentage'] = (df['Profit_Margin'] / df['Order_Value']) * 100
df['Delivery_Performance'] = pd.cut(df['Delivery_Rating'], bins=[0, 3, 4, 5], labels=['Low', 'Medium', 'High'])


bins = [0, 18, 30, 45, 60, float('inf')]
labels = ['Teen', 'Young Adult', 'Adult', 'Middle Age', 'Senior']
df['Age_Group'] = pd.cut(df['Customer_Age'], bins=bins, labels=labels, right=False)
#df['Age_Group']

#-----------------------------------------------------------------------------------------
#Store Data in MySQL
#---------------------------------------------------------------------------------------------
username='postgres'
password='Dhashwin05'
port=5432
database_name='OnlineFoodDeliveryDB'
host_name='localhost'
engine=create_engine(f'postgresql+psycopg2://{username}:{password}@{host_name}:{port}/{database_name}')

print("Connection created successfully")

df.columns = df.columns.str.lower()

# write the file to postgressql
df.to_sql("onlinefooddeliverydata",con=engine,if_exists="replace",index=False)
print(f'Cleaned Online Food Delivery data has been inserted into OnlineFoodDeliveryDB and count of :{len(df)}')