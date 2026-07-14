import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import joblib
import os

st.set_page_config(page_title="Sales Forecasting Dashboard", page_icon="📈", layout="wide")

# Custom CSS for better styling
st.markdown("""
<style>
    .stMetric {
        background-color: #1f1f1f;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(255,255,255,0.05);
        border: 1px solid #333333;
    }
    .main-header {
        font-weight: 700;
        color: #1abc9c;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_dashboard_data():
    if not os.path.exists('dashboard_data.pkl'):
        return None
    return joblib.load('dashboard_data.pkl')

data = load_dashboard_data()

if data is None:
    st.error("Could not find 'dashboard_data.pkl'. Please ensure you have run the export code in your Jupyter Notebook.")
    st.stop()

# Extract data components
df = data['df']
monthly_sales = data['monthly_sales']
forecasts = data['forecasts']
weekly_df = data['weekly_df']
anomalies_if = data['anomalies_if']
cluster_df = data['cluster_df']
pca_variance = data['pca_variance']

# Sidebar Navigation
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=60)
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a Dashboard", [
    "Sales Overview", 
    "Forecast Explorer", 
    "Anomaly Report", 
    "Product Segments"
])

st.sidebar.markdown("---")
st.sidebar.info("Executive Dashboard for analyzing historical sales, forecasting demand, and detecting anomalies.")

if page == "Sales Overview":
    st.markdown("<h2 class='main-header'>Global Sales Overview</h2>", unsafe_allow_html=True)
    
    # KPIs
    total_sales = df['Sales'].sum()
    total_orders = df.shape[0]
    avg_order = df['Sales'].mean()
    total_customers = df['Customer ID'].nunique()
    total_products = df['Product ID'].nunique()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Revenue", f"${total_sales:,.2f}")
    col2.metric("Total Orders", f"{total_orders:,}")
    col3.metric("Avg Order Value", f"${avg_order:,.2f}")
    col4.metric("Total Customers", f"{total_customers:,}")
    col5.metric("Total Products", f"{total_products:,}")
    
    st.markdown("---")
    
    col_chart1, col_chart2 = st.columns(2)
    
    # Yearly Sales Bar Chart
    yearly_sales = df.groupby('Year')['Sales'].sum().reset_index()
    fig_year = px.bar(yearly_sales, x='Year', y='Sales', title="Total Sales by Year", 
                      color='Sales', color_continuous_scale='Mint')
    fig_year.update_layout(xaxis_type='category')
    col_chart1.plotly_chart(fig_year, use_container_width=True)
    
    # Monthly Sales Trend
    monthly_sales_df = monthly_sales.reset_index()
    fig_month = px.line(monthly_sales_df, x='Order Date', y='Sales', title="Monthly Sales Trend",
                        markers=True, line_shape="spline")
    fig_month.update_traces(line_width=3)
    col_chart2.plotly_chart(fig_month, use_container_width=True)
    
    st.markdown("---")
    
    # New row of charts
    row2_col1, row2_col2, row2_col3 = st.columns(3)
    
    # Sales by Segment (Donut)
    segment_sales = df.groupby('Segment')['Sales'].sum().reset_index()
    fig_seg = px.pie(segment_sales, values='Sales', names='Segment', title="Sales by Segment", hole=0.4)
    row2_col1.plotly_chart(fig_seg, use_container_width=True)
    
    # Top 10 Cities
    city_sales = df.groupby('City')['Sales'].sum().reset_index().sort_values('Sales', ascending=False).head(10)
    fig_city = px.bar(city_sales, x='Sales', y='City', orientation='h', title="Top 10 Cities by Sales", color='Sales', color_continuous_scale='Mint')
    fig_city.update_layout(yaxis={'categoryorder':'total ascending'})
    row2_col2.plotly_chart(fig_city, use_container_width=True)
    
    # Sales by Ship Mode
    ship_sales = df.groupby('Ship Mode')['Sales'].sum().reset_index()
    fig_ship = px.pie(ship_sales, values='Sales', names='Ship Mode', title="Sales by Ship Mode")
    row2_col3.plotly_chart(fig_ship, use_container_width=True)
    
    st.markdown("### Regional & Category Breakdown")
    # Filters
    f_col1, f_col2 = st.columns(2)
    sel_region = f_col1.multiselect("Filter by Region", df['Region'].unique(), default=df['Region'].unique())
    sel_category = f_col2.multiselect("Filter by Category", df['Category'].unique(), default=df['Category'].unique())
    
    filtered_df = df[(df['Region'].isin(sel_region)) & (df['Category'].isin(sel_category))]
    
    if not filtered_df.empty:
        cat_reg_sales = filtered_df.groupby(['Region', 'Category'])['Sales'].sum().reset_index()
        fig_treemap = px.treemap(cat_reg_sales, path=['Region', 'Category'], values='Sales', 
                                 title="Sales Distribution (Treemap)", color='Sales', color_continuous_scale='Teal')
        st.plotly_chart(fig_treemap, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")

elif page == "Forecast Explorer":
    st.markdown("<h2 class='main-header'>Demand Forecasting Engine</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 3])
    
    # The forecasts dictionary keys are: 'Furniture', 'Technology', 'Office Supplies', 'West Region', 'East Region'
    available_segments = list(forecasts.keys())
    
    with col1:
        st.markdown("### Controls")
        segment = st.selectbox("Select Segment to Forecast", available_segments)
        st.markdown("---")
        st.write("Using pre-computed **SARIMA** model forecasts (3-Month Horizon).")
    
    with col2:
        forecast_series = forecasts[segment]
        
        if forecast_series is not None:
            # Get historical data for the selected segment to plot alongside forecast
            if "Region" in segment:
                reg_name = segment.replace(" Region", "")
                segment_df = df[df['Region'] == reg_name]
            else:
                segment_df = df[df['Category'] == segment]
                
            historical_monthly = segment_df.set_index('Order Date')['Sales'].resample('MS').sum()
            
            fig = go.Figure()
            
            # Historical
            fig.add_trace(go.Scatter(x=historical_monthly.index, y=historical_monthly.values,
                                     mode='lines+markers', name='Historical Sales',
                                     line=dict(width=2)))
            
            # Forecast
            fig.add_trace(go.Scatter(x=forecast_series.index, y=forecast_series.values,
                                     mode='lines+markers', name='Forecast (SARIMA)',
                                     line=dict(width=2, dash='dash')))
                                     
            fig.update_layout(title=f"{segment} Sales Forecast",
                              xaxis_title="Date", yaxis_title="Sales ($)",
                              hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("### Forecast Values")
            forecast_df = forecast_series.reset_index()
            forecast_df.columns = ['Date', 'Forecasted Sales']
            forecast_df['Date'] = forecast_df['Date'].dt.strftime('%Y-%m')
            forecast_df['Forecasted Sales'] = forecast_df['Forecasted Sales'].apply(lambda x: f"${x:,.2f}")
            st.dataframe(forecast_df, hide_index=True, use_container_width=True)
        else:
            st.error(f"No forecast data available for {segment}.")

elif page == "Anomaly Report":
    st.markdown("<h2 class='main-header'>Sales Anomaly Detection</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    col1.metric("Total Weeks Analyzed", len(weekly_df))
    col2.metric("Anomalies Detected", len(anomalies_if), delta_color="inverse")
    
    # Plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=weekly_df.index, y=weekly_df['Sales'],
                             mode='lines', name='Weekly Sales',
                             line=dict(width=2)))
                             
    fig.add_trace(go.Scatter(x=anomalies_if.index, y=anomalies_if['Sales'],
                             mode='markers', name='Anomaly (Isolation Forest)',
                             marker=dict(color='red', size=10, symbol='x')))
                             
    fig.update_layout(title="Weekly Sales Anomalies",
                      xaxis_title="Date", yaxis_title="Sales ($)")
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### Detailed Anomaly Log")
    display_anomalies = anomalies_if.copy().reset_index()
    if 'Order Date' in display_anomalies.columns:
        display_anomalies['Order Date'] = display_anomalies['Order Date'].dt.strftime('%Y-%m-%d')
    display_anomalies['Sales'] = display_anomalies['Sales'].apply(lambda x: f"${x:,.2f}")
    if 'Anomaly_IF' in display_anomalies.columns:
        display_anomalies = display_anomalies.drop(columns=['Anomaly_IF'])
    
    st.dataframe(display_anomalies, use_container_width=True, hide_index=True)

elif page == "Product Segments":
    st.markdown("<h2 class='main-header'>Product Demand Segmentation</h2>", unsafe_allow_html=True)
    
    if not cluster_df.empty:
        kpi_cols = st.columns(4)
        clusters = cluster_df['Cluster_Label'].value_counts()
        for i, (label, count) in enumerate(clusters.items()):
            kpi_cols[i % 4].metric(label, f"{count} Sub-Categories")
        
        st.markdown("---")
        
        # Scatter Plot
        fig = px.scatter(cluster_df.reset_index(), x='PCA_1', y='PCA_2', 
                         color='Cluster_Label', hover_name='Sub-Category',
                         title="Product Demand Clusters (PCA Projection)",
                         labels={'PCA_1': f'PCA Component 1 ({pca_variance[0]*100:.1f}%)', 
                                 'PCA_2': f'PCA Component 2 ({pca_variance[1]*100:.1f}%)'},
                         color_discrete_sequence=px.colors.qualitative.Bold)
                         
        fig.update_traces(marker=dict(size=12, line=dict(width=1, color='DarkSlateGrey')))
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### Cluster Assignments & Strategy")
        
        display_df = cluster_df[['Cluster_Label', 'Total_Sales', 'Growth_Rate', 'Sales_Volatility']].copy()
        display_df['Total_Sales'] = display_df['Total_Sales'].apply(lambda x: f"${x:,.2f}")
        display_df['Growth_Rate'] = display_df['Growth_Rate'].apply(lambda x: f"{x:.1f}%")
        display_df['Sales_Volatility'] = display_df['Sales_Volatility'].apply(lambda x: f"${x:,.2f}")
        display_df = display_df.reset_index().rename(columns={'Cluster_Label': 'Demand Segment'})
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.error("No cluster data available.")
