import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from pathlib import Path
from datetime import datetime, timedelta

# Set page config
st.set_page_config(page_title="Uppercase Business Dashboard", page_icon = "uppercase-logo.png", layout="wide")

# Load the dataset
DATA_FILENAME = Path(__file__).parent / 'data/base.csv'
df = pd.read_csv(DATA_FILENAME)

# Convert 'order-date' to datetime format (in case it's not already in datetime format)
df['order-date'] = pd.to_datetime(df['order-date'], format='%d-%m-%Y', errors='coerce')
#df['order-date'] = df['order-date'].dt.date  # This will convert to just the date part

df['revenue'] = pd.to_numeric(df['revenue'],errors='coerce')
df['revenue'] = df['revenue'].round(0)

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

st.markdown("""
    <style>
        /* Dropdown options' text color */
        .stMultiSelect .st-bx div {
            color: #008080;              /* Teal color for the dropdown items */
        }

        /* Hover effect for dropdown items */
        .stMultiSelect .st-bx > div:hover {
            background-color: #007f7f;   /* Slightly lighter teal on hover */
            color: white;                /* White text color on hover */
        }
    </style>
""", unsafe_allow_html=True)


# # Sidebar for selecting filters
# st.sidebar.header('Filter Data')

# Add date range filter
st.sidebar.subheader("Select Date Range")
start_date = st.sidebar.date_input("Start Date", df['order-date'].min())
end_date = st.sidebar.date_input("End Date", df['order-date'].max())

# Add an "All" option for filters in the sidebar
#category_filter = st.sidebar.selectbox('Select Category', ['All'] + list(df['category'].unique()))
category_filter = st.sidebar.multiselect('Select Category', ['All'] + list(df['category'].unique()), default=['All'])
zone_filter = st.sidebar.multiselect('Select Customer Zone', ['All'] + list(df['cust-zone'].unique()), default=['All'])
platform_filter = st.sidebar.multiselect('Select Platform', ['All'] + list(df['platform'].unique()), default=['All'])

# Apply filters to the DataFrame based on selected options
filtered_df = df.copy()  # Start with the full dataset

#Filter by Category
if 'All' in category_filter:
    filtered_df = filtered_df  # Show all data if 'All' is selected
else:
    filtered_df = filtered_df[filtered_df['category'].isin(category_filter)]


# Filter by Customer Zone
if 'All' in zone_filter:
    filtered_df = filtered_df  # Show all data if 'All' is selected
else:
    filtered_df = filtered_df[filtered_df['cust-zone'].isin(zone_filter)]


# if zone_filter != 'All':
#     filtered_df = filtered_df[filtered_df['cust-zone'] == zone_filter]

# Filter by Platform
if 'All' in platform_filter:
    filtered_df = filtered_df  # Show all data if 'All' is selected
else:
    filtered_df = filtered_df[filtered_df['platform'].isin(platform_filter)]

# if platform_filter != 'All':
#     filtered_df = filtered_df[filtered_df['platform'] == platform_filter]

# Filter by Date Range
filtered_df = filtered_df[(filtered_df['order-date'] >= pd.to_datetime(start_date)) & 
                          (filtered_df['order-date'] <= pd.to_datetime(end_date))]

# Show the filtered data
st.subheader(f"KPI's")
st.write(f'Selected Data: Category - {category_filter}, Zone - {zone_filter}, Platform - {platform_filter}')

# --- Display Total Revenue and Units (Card Style) ---


total_revenue = filtered_df['revenue'].sum()
tr = total_revenue/100000
total_units = filtered_df['qty'].sum()
asp = round(total_revenue/total_units if total_units > 0 else 0)
distinct_order_dates = filtered_df['order-date'].nunique()
distinct_orders = filtered_df['order-no'].nunique()
drr_gmv = tr / distinct_order_dates if distinct_order_dates > 0 else 0
drr_units = total_units / distinct_order_dates if distinct_order_dates > 0 else 0
aov = total_revenue / distinct_orders if distinct_orders > 0 else 0



#Calculating data for trend

min_order_date = filtered_df['order-date'].min() 
first_day_current_month = min_order_date.replace(day=1)
last_day_last_month = first_day_current_month - timedelta(days=1)
first_day_last_month = last_day_last_month.replace(day=1)

fdf = df.copy()

if 'All' in category_filter:
    fdf = fdf  # Show all data if 'All' is selected
else:
    fdf = fdf[fdf['category'].isin(category_filter)]

# # Filter by Customer Zone
# if zone_filter != 'All':
#     fdf = fdf[fdf['cust-zone'] == zone_filter]

# # Filter by Platform
# if platform_filter != 'All':
#     fdf = fdf[fdf['platform'] == platform_filter]


# Filter by Customer Zone
if 'All' in zone_filter:
    fdf = fdf  # Show all data if 'All' is selected
else:
    fdf = fdf[fdf['cust-zone'].isin(zone_filter)]


# Filter by Platform
if 'All' in platform_filter:
    fdf = fdf  # Show all data if 'All' is selected
else:
    fdf = fdf[fdf['platform'].isin(platform_filter)]



last_month_df = fdf[(fdf['order-date'] >= first_day_last_month) & 
                             (fdf['order-date'] <= last_day_last_month)]
lm_orders = last_month_df['order-no'].nunique()
last_month_revenue = last_month_df['revenue'].sum()
lmr_lakhs = last_month_revenue/100000
last_month_units = last_month_df['qty'].sum()
last_month_asp = round(last_month_revenue/last_month_units if last_month_units > 0 else 0)
last_month_aov = round(last_month_revenue/lm_orders if lm_orders > 0 else 0)
divisor = last_day_last_month.day
lm_rev_drr = last_month_revenue/divisor/100000
lm_units_drr = round(last_month_units/divisor if divisor > 0 else 0)
revenue_trend = drr_gmv - lm_rev_drr
rt = revenue_trend/lm_rev_drr*100
ut = ((drr_units-lm_units_drr)/lm_units_drr if lm_units_drr > 0 else 0)*100
aovt = ((aov-last_month_aov)/lm_units_drr if lm_units_drr > 0 else 0)*100

# Displaying the data in a card-like format using st.markdown

col1, col2, col3 = st.columns(3)

# Card 1 (GMV)
with col1:
    st.markdown(f"""
        <div style="padding: 15px; background-color: #f1f1f1; border-radius: 8px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);">
            <h3 style="text-align: center; font-size: 18px;"> Sales: ₹{tr:,.1f} Lakhs</h3>
        </div>
    """, unsafe_allow_html=True)

# Card 2 (Units)
with col2:
    st.markdown(f"""
        <div style="padding: 15px; background-color: #f1f1f1; border-radius: 8px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);">
            <h3 style="text-align: center; font-size: 18px;">Units: {total_units:,.0f}</h3>
        </div>
    """, unsafe_allow_html=True)

# Card 3 (ASP)
with col3:
    st.markdown(f"""
        <div style="padding: 15px; background-color: #f1f1f1; border-radius: 8px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);">
            <h3 style="text-align: center; font-size: 18px;">ASP: ₹{asp:,}</h3>
        </div>
    """, unsafe_allow_html=True)

# Add space between rows
st.write("")  # You can also use `st.markdown("<br>", unsafe_allow_html=True)` for line breaks

# Create 3 more columns for the next row of cards
col4, col5, col6 = st.columns(3)

# Card 4 (DRR GMV)
with col4:
    # Check if rt% is positive or negative and set the appropriate arrow
    if rt >= 0:
        arrow = "&#x2191;"  # Up arrow (↑)
        arrow_color = "green"  # Green color for positive values
    else:
        arrow = "&#x2193;"  # Down arrow (↓)
        arrow_color = "red"  # Red color for negative values

    # Display DRR (GMV) with rt% and the corresponding arrow
    st.markdown(f"""
        <div style="padding: 15px; background-color: #f1f1f1; border-radius: 8px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);">
            <h3 style="text-align: center; font-size: 18px;">
                DRR (Sales) : ₹{drr_gmv:,.1f} Lakhs<br>
            <span style="font-size: 16px; color: {arrow_color};">
                    {arrow} {abs(rt):.2f}%
                </span>
              </h3>  
            </div>
    """, unsafe_allow_html=True)

with col5:
    # Check if ut% is positive or negative and set the appropriate arrow
    if ut >= 0:
        arrow = "&#x2191;"  # Up arrow (↑)
        arrow_color = "green"  # Green color for positive values
    else:
        arrow = "&#x2193;"  # Down arrow (↓)
        arrow_color = "red"  # Red color for negative values

    # Display DRR (GMV) with rt% and the corresponding arrow
    st.markdown(f"""
        <div style="padding: 15px; background-color: #f1f1f1; border-radius: 8px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);">
            <h3 style="text-align: center; font-size: 18px;">
                DRR (Units) : {drr_units:,.0f}<br>
            <span style="font-size: 16px; color: {arrow_color};">
                    {arrow} {abs(ut):.2f}%
                </span>
              </h3>  
            </div>
    """, unsafe_allow_html=True)

with col6:
    # Check if ut% is positive or negative and set the appropriate arrow
    if aovt >= 0:
        arrow = "&#x2191;"  # Up arrow (↑)
        arrow_color = "green"  # Green color for positive values
    else:
        arrow = "&#x2193;"  # Down arrow (↓)
        arrow_color = "red"  # Red color for negative values

    # Display AOV with aovt% and the corresponding arrow
    st.markdown(f"""
        <div style="padding: 15px; background-color: #f1f1f1; border-radius: 8px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);">
            <h3 style="text-align: center; font-size: 18px;">
                AOV : ₹{aov:,.0f}<br>
            <span style="font-size: 16px; color: {arrow_color};">
                    {arrow} {abs(aovt):.2f}%
                </span>
              </h3>  
            </div>
    """, unsafe_allow_html=True)

# Display the last month's revenue
st.write(f" ")
st.subheader('Last Month :')
# st.write(f"Sales: ₹{lmr_lakhs:,.0f} Lakhs")
# st.write(f"Revenue DRR: ₹{lm_rev_drr:,.0f} Lakhs")
# st.write(f"Units DRR :{lm_units_drr}")
# st.write(f"ASP :{last_month_asp}")
# st.write(f"AOV :{last_month_aov}")


col11, col12, col13 = st.columns(3)

# Display different elements in each column
with col11:
    st.write(f"Sales : ₹{lmr_lakhs:,.1f} Lakhs")
    
with col12:
    st.write(f"Units : {last_month_units}")
    
with col13:
    st.write(f"ASP : ₹{last_month_asp}")

col21, col22, col23 = st.columns(3)

# Display different elements in each column
with col21:
    st.write(f"DRR (Sales) : ₹{lm_rev_drr:,.1f} Lakhs")
    
with col22:
    st.write(f"DRR (Units) : {lm_units_drr}")
    
with col23:
    st.write(f"AOV : ₹{last_month_aov}")


#Filtering with date
aggregated_df = filtered_df.groupby('order-date')[['revenue', 'qty']].sum().reset_index()
aggregated_df['order-date'] = aggregated_df['order-date'].dt.date  # This will convert to just the date part

st.write(aggregated_df)

# st.write(filtered_df)


# st.markdown(f"""
#     <div style="padding: 10px; background-color: #f1f1f1; border-radius: 8px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);">
#         <h3>GMV : {tr:,.0f} lakhs</h3>
#         <h3>Units: {total_units:,.0f}</h3>
#         <h3>ASP : {asp:,}</h3>
#         <h3> DRR (GMV) : {drr_gmv:,.0f}</h3>
#         <h3> DRR (Units) : {drr_units:,.0f}</h3>
#         <h3> AOV : {aov:,.0f}</h3>
#     </div>
#     """, unsafe_allow_html=True)

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
