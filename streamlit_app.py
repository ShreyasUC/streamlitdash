import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from pathlib import Path

# Set page config
st.set_page_config(page_title="Uppercase Business Dashboard", page_icon = "uppercase-logo.png", layout="wide")

# Load the dataset
DATA_FILENAME = Path(__file__).parent / 'data/base.csv'
df = pd.read_csv(DATA_FILENAME)

# Convert 'order-date' to datetime format (in case it's not already in datetime format)
df['order-date'] = pd.to_datetime(df['order-date'], errors='coerce')  # 'coerce' will turn invalid dates into NaT
df['revenue'] = pd.to_numeric(df['revenue'],errors='coerce')

# Streamlit app layout
st.title('Revenue Dashboard')

st.sidebar.image("uppercase-logo.png", use_column_width=True)
st.sidebar.markdown("""
    <style>
        .header-title {
            font-size: 40px;
            font-weight: bold;
            color: #2C3E50;
            text-align: center;
        }
    </style>
    <div class="header-title">Business Summary</div>
""", unsafe_allow_html=True)
#st.sidebar.header("⚙️ Settings")


# # Sidebar for selecting filters
# st.sidebar.header('Filter Data')

# Add date range filter
st.sidebar.subheader("Select Date Range")
start_date = st.sidebar.date_input("Start Date", df['order-date'].min())
end_date = st.sidebar.date_input("End Date", df['order-date'].max())

# Add an "All" option for filters in the sidebar
category_filter = st.sidebar.selectbox('Select Category', ['All'] + list(df['category'].unique()))
zone_filter = st.sidebar.selectbox('Select Customer Zone', ['All'] + list(df['cust-zone'].unique()))
platform_filter = st.sidebar.selectbox('Select Platform', ['All'] + list(df['platform'].unique()))

# Apply filters to the DataFrame based on selected options
filtered_df = df.copy()  # Start with the full dataset

# Filter by Category
if category_filter != 'All':
    filtered_df = filtered_df[filtered_df['category'] == category_filter]

# Filter by Customer Zone
if zone_filter != 'All':
    filtered_df = filtered_df[filtered_df['cust-zone'] == zone_filter]

# Filter by Platform
if platform_filter != 'All':
    filtered_df = filtered_df[filtered_df['platform'] == platform_filter]

# Filter by Date Range
filtered_df = filtered_df[(filtered_df['order-date'] >= pd.to_datetime(start_date)) & 
                          (filtered_df['order-date'] <= pd.to_datetime(end_date))]

# Show the filtered data
st.subheader(f'Selected Data: Category - {category_filter}, Zone - {zone_filter}, Platform - {platform_filter}')
st.write(filtered_df)

# --- Display Total Revenue and Units (Card Style) ---

total_revenue = filtered_df['revenue'].sum()
tr = total_revenue/100000
total_units = filtered_df['qty'].sum()
asp = round(total_revenue/total_units)
distinct_order_dates = df['order-date'].nunique()
distinct_orders = df['order-no'].nunique()
drr_gmv = total_revenue / distinct_order_dates if distinct_order_dates > 0 else 0
drr_units = total_units / distinct_order_dates if distinct_order_dates > 0 else 0
aov = total_revenue / distinct_orders if distinct_orders > 0 else 0

# Displaying the data in a card-like format using st.markdown
st.markdown(f"""
    <div style="padding: 10px; background-color: #f1f1f1; border-radius: 8px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);">
        <h3>GMV : {tr:,.0f} lakhs</h3>
        <h3>Units: {total_units:,.0f}</h3>
        <h3>ASP : {asp:,}</h3>
        <h3> DRR (GMV) : {drr_gmv:,.0f}</h3>
        <h3> DRR (Units) : {drr_units:,.0f}</h3>
        <h3> AOV : {aov:,.0f}</h3>
    </div>
    """, unsafe_allow_html=True)

# # --- Revenue by Category (Bar Chart) ---
# st.subheader('Revenue by Category')
# category_revenue = filtered_df.groupby('category')['revenue'].sum().reset_index()

# # Bar chart using Matplotlib
# fig, ax = plt.subplots(figsize=(10, 6))
# ax.bar(category_revenue['category'], category_revenue['revenue'], color='skyblue')
# ax.set_title('Total Revenue by Category')
# ax.set_xlabel('Category')
# ax.set_ylabel('Revenue')
# plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability

# st.pyplot(fig)

# --- Revenue Split by Category (Pie Chart) ---
st.subheader('Revenue Split by Category (Pie Chart)')
category_revenue_pie = filtered_df.groupby('category')['revenue'].sum().reset_index()

# Pie chart using Plotly
fig = px.pie(category_revenue_pie, names='category', values='revenue', title='Revenue Split by Category')
st.plotly_chart(fig)

# --- Revenue Over Time (Line Chart) ---
st.subheader('Revenue Over Time (Order Date)')
time_revenue = filtered_df.groupby('order-date')['revenue'].sum().reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(time_revenue['order-date'], time_revenue['revenue'], marker='o', color='green')
ax.set_title('Revenue Over Time')
ax.set_xlabel('Order Date')
ax.set_ylabel('Revenue')
plt.xticks(rotation=45)

st.pyplot(fig)

# --- Revenue Distribution by Customer Zone (Boxplot) ---
st.subheader('Revenue Distribution by Customer Zone')
plt.figure(figsize=(10, 6))
sns.boxplot(x='cust-zone', y='revenue', data=filtered_df, palette='Set2')
plt.title('Revenue Distribution by Customer Zone')
plt.xlabel('Customer Zone')
plt.ylabel('Revenue')
plt.xticks(rotation=45)

st.pyplot(plt)

# --- Revenue by Platform (Interactive Bar Chart) ---
st.subheader('Revenue by Platform (Interactive)')
platform_revenue = filtered_df.groupby('platform')['revenue'].sum().reset_index()

fig = px.bar(platform_revenue, x='platform', y='revenue', title='Revenue by Platform', color='platform')
st.plotly_chart(fig)

# Optionally, you can add more graphs based on user input, such as:
# Create Revenue by SKU, Quantity Sold, or more visualizations.
