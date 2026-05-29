import streamlit as st
import pandas as pd

# ----------------------------------------------------
# THE PAGE CONFIGURATION
# ----------------------------------------------------
# This sets the title, the icon, and it expands the layout 
st.set_page_config(
    page_title="The Vendor Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

# The Application Header and Subtitle
st.title("📊 The Vendor Performance Dashboard")
st.markdown("The interactive interface gives you access to explore vendor data, analyze sales performance, and filter metrics by individual vendor or region.")

# ----------------------------------------------------
# 1. DATA LOADING FUNCTION PROCESS
# ----------------------------------------------------
# The st.cache_data avoids reloading the dataset on every user interaction
@st.cache_data
def load_data():
    # In here, we extract name of the dataset file given
    file_name = "sellers.xlsx"
    df = pd.read_excel(file_name)
    return df
    
df = load_data()

st.dataframe(df)

st.write(df.head())

# ----------------------------------------------------
# 2. THE SIDEBAR FILTER SECTION (Region selection process)
# ----------------------------------------------------
st.sidebar.header("Filter Options")

# In here, we create a region list and group it through “All Regions” option.
regions = ["All regions"] + list(df['REGION'].unique())
selected_region = st.sidebar.selectbox("Select region to filter table and graphs:", regions)

# In here, we filter the dataframe based on the user's selected region
if selected_region == "All Regions":
    filtered_df = df
else:
    filtered_df = df[df['REGION'] == selected_region]

# ----------------------------------------------------
# 3. THE INTERACTIVE METRICS OVERVIEW
# ----------------------------------------------------

#In here, we display a section title for the metrics overview 
st.subheader("📈 The region metrics overview")

#In here, we display a summary that describes the chosen region
st.markdown(f"Summery of metrics computed for **{selected_region}**:")

# In here, we create four columns to organize key performance indicators (KPI) cards
col1, col2, col3, col4 = st.columns(4)

# In here, we show KPI metrics inside of each column

# In here, we count the total number of vendors 
with col1:
    st.metric(label="Total vendors", value=len(filtered_df)) 

 # In here, we count the total units sold
with col2:
    st.metric(label="Total units sold", value=f"{filtered_df['SOLD UNITS'].sum():,}")

# In here, we count the total sales 
with col3:
    st.metric(label="Total sales", value=f"${filtered_df['TOTAL SALES'].sum():,}")

# In here, we calculate the average sales rate
with col4:
    st.metric(label="Average sales rate", value=f"{filtered_df['SALES AVERAGE'].mean():.4f}")

st.markdown("---")

# ----------------------------------------------------
# 4. THE FILTERED DATA TABLE 
# ----------------------------------------------------

# In here, we show the title with the selected region
st.subheader(f"📋 Vendor data table - {selected_region}")

# In here, we point out that columns can be sorted out by clicking on the headers
st.markdown("Click on column headers to monitor ascending/descending.")

# In here, show an interactive table that fits screen width.
st.dataframe(
    filtered_df[['ID', 'NAME', 'REGION', 'INCOME', 'SOLD UNITS', 'TOTAL SALES', 'SALES AVERAGE']], 
    use_container_width=True, 
    hide_index=True
)

st.markdown("---")

# ----------------------------------------------------
# 5. THE PERFORMANCE VISUALIZATION GRAPHS
# ----------------------------------------------------

# In here, we show the section title 
st.subheader("📊 Performance visualizations")

# In here, we describe what the graphs compare 
st.markdown("Compare vendor performance across units sold, Total sales, and Average sales metrics.")

# In here, we create tabs in order to organize graphs which make dashboards easier to explore
tab1, tab2, tab3 = st.tabs(["🛒 Units sold", "💰 Total sales", "📉 Sales average"])

with tab1:
    st.markdown("Units sold per vendor")
    # In here, we add Streamlit bar chart giving name to units sold, and color-coded by region
    st.bar_chart(data=filtered_df, x='NAME', y='SOLD UNITS', color='REGION', use_container_width=True)

with tab2:
    st.markdown("Total sales ($) per vendor")
    # In here, we add bar chart to total revenue sales
    st.bar_chart(data=filtered_df, x='NAME', y='TOTAL SALES', color='REGION', use_container_width=True)

with tab3:
    st.markdown("Sales average ratio per vendor")
    # In here, we add bar chart to average sales ratio
    st.bar_chart(data=filtered_df, x='NAME', y='SALES AVERAGE', color='REGION', use_container_width=True)

st.markdown("---")

# ----------------------------------------------------
# 6. THE INDIVIDUAL VENDOR SELECTION
# ----------------------------------------------------

# In here, we show vendor analysis section and its instructions for chosing a vendor

st.subheader("🔍 The individual Vendor analysis")
st.markdown("Pick an individual vendor from the dropdown below. Navigate personal records and regional benchmark comparisons.")

# In here, we sort names in alphabetical order for user benefit
vendor_list = sorted(df['NAME'].unique())
selected_vendor = st.selectbox("Pick a vendor to navigate:", vendor_list)

# In here, get the specific data row that matches the selected name
vendor_data = df[df['NAME'] == selected_vendor].iloc[0]

# In here, we place details inside a styled box to separate information in a organized way.
with st.container(border=True):
    v_col1, v_col2 = st.columns(2)

with v_col1:
        st.markdown(f"Profile: **{vendor_data['NAME']}**")
        st.markdown(f"Vendor ID:** `{vendor_data['ID']}`")
        st.markdown(f"Assigned region:** {vendor_data['REGION']}")
        st.markdown(f"Income:** ${vendor_data['INCOME']:,}")

with v_col2:
        st.markdown("Performance statistics")
        v_metric1, v_metric2, v_metric3 = st.columns(3)
        v_metric1.metric("Units sold", f"{vendor_data['SOLD UNITS']:,}")
        v_metric2.metric("Total sales", f"${vendor_data['TOTAL SALES']:,}")
        v_metric3.metric("Sales average", f"{vendor_data['SALES AVERAGE']:.4f}")