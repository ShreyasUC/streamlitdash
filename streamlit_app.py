import streamlit as st
import pandas as pd
import math
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


DATA_FILENAME = Path(__file__).parent/'data/base.csv'
df = pd.read_csv(DATA_FILENAME)

# Streamlit app layout
st.title('Streamlit Dashboard: Revenue Analysis')

# Sidebar for selecting filters
st.sidebar.header('Filter Data')
category_filter = st.sidebar.selectbox('Select Category', df['category'].unique())
zone_filter = st.sidebar.selectbox('Select Customer Zone', df['cust-zone'].unique())
platform_filter = st.sidebar.selectbox('Select Platform', df['platform'].unique())

# Apply filters to the DataFrame
filtered_df = df[
    (df['category'] == category_filter) &
    (df['cust-zone'] == zone_filter) &
    (df['platform'] == platform_filter)
]

# Show the filtered data
st.subheader(f'Selected Data: Category - {category_filter}, Zone - {zone_filter}, Platform - {platform_filter}')
st.write(filtered_df)

# Create a Revenue Plot by Category
st.subheader('Revenue by Category')
category_revenue = df.groupby('category')['revenue'].sum().reset_index()

# Bar chart using Matplotlib
fig, ax = plt.subplots()
ax.bar(category_revenue['category'], category_revenue['revenue'], color='skyblue')
ax.set_title('Total Revenue by Category')
ax.set_xlabel('Category')
ax.set_ylabel('Revenue')

st.pyplot(fig)

# Create a Time Series Plot of Revenue over Order Dates
st.subheader('Revenue Over Time (Order Date)')
df['order-date'] = pd.to_datetime(df['order-date'])  # Make sure order-date is in datetime format
time_revenue = df.groupby('order-date')['revenue'].sum().reset_index()

fig, ax = plt.subplots()
ax.plot(time_revenue['order-date'], time_revenue['revenue'], marker='o', color='green')
ax.set_title('Revenue Over Time')
ax.set_xlabel('Order Date')
ax.set_ylabel('Revenue')

st.pyplot(fig)

# Create a Boxplot of Revenue by Customer Zone
st.subheader('Revenue Distribution by Customer Zone')
plt.figure(figsize=(8, 6))
sns.boxplot(x='cust-zone', y='revenue', data=df, palette='Set2')
plt.title('Revenue Distribution by Customer Zone')
plt.xlabel('Customer Zone')
plt.ylabel('Revenue')

st.pyplot(plt)

# Interactive Plot using Plotly (Revenue by Platform)
st.subheader('Revenue by Platform (Interactive)')
platform_revenue = df.groupby('platform')['revenue'].sum().reset_index()

fig = px.bar(platform_revenue, x='platform', y='revenue', title='Revenue by Platform', color='platform')
st.plotly_chart(fig)

# Optionally, you can also add more graphs based on user input, for example:
# Create Revenue by SKU, Quantity Sold, or more visualizations.
