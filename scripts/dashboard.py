import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
try:
    df = pd.read_csv("data/bls_data.csv")
except FileNotFoundError:
    st.error("Data file not found. Please run `fetch_bls_data.py` to fetch the data.")
    st.stop()

# Map series IDs to human-readable names
series_descriptions = {
    "CES0000000001": "Total Non-Farm Employment",
    "LNS14000000": "Unemployment Rate",
    "LNS11300000": "Labor Force Participation Rate",
    "CES0500000003": "Average Hourly Earnings"
}
df['series_description'] = df['series_id'].map(series_descriptions)

# Sidebar for metric selection
st.sidebar.title("Dashboard Navigation")
selected_series = st.sidebar.selectbox(
    "Select a Metric to Visualize:",
    df['series_description'].unique()
)

# Sidebar for date filter
st.sidebar.subheader("Filter Data by Date")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2022-01-01").date())
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2023-12-01").date())

# Ensure start_date and end_date are converted to datetime64[ns]
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter data based on selection and date range
filtered_data = df[df['series_description'] == selected_series]
filtered_data = filtered_data[
    (pd.to_datetime(filtered_data['date']) >= start_date) &
    (pd.to_datetime(filtered_data['date']) <= end_date)
]

# App title
st.title("US Labor Statistics Dashboard")

# Display metrics for the selected series
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Latest Value", f"{filtered_data['value'].iloc[-1]:,.0f}")
with col2:
    st.metric("Max Value", f"{filtered_data['value'].max():,.0f}")
with col3:
    st.metric("Min Value", f"{filtered_data['value'].min():,.0f}")

# Add a divider
st.markdown("---")

# Plot the data with Plotly
fig = px.line(
    filtered_data,
    x="date",
    y="value",
    title=f"{selected_series} Over Time",
    labels={"value": "Value", "date": "Date"},
    template="plotly_white"
)

# Customize plot layout
fig.update_traces(line=dict(width=3), marker=dict(size=8))
fig.update_layout(
    plot_bgcolor="#f9f9f9",  # Light gray background
    paper_bgcolor="#ffffff",  # White paper
    title_font=dict(size=24, color="blue"),
    xaxis=dict(showgrid=False),
    yaxis=dict(gridwidth=0.5, gridcolor="#d3d3d3"),
    margin=dict(l=20, r=20, t=50, b=20)  # Add padding
)
st.plotly_chart(fig)

# Display the latest data in a table
st.subheader(f"Latest Data for {selected_series}")
latest_data = filtered_data.sort_values(by="date", ascending=False).head(1)
st.write(latest_data)

# Allow users to download filtered data as a CSV
@st.cache_data
def convert_df_to_csv(dataframe):
    return dataframe.to_csv(index=False).encode('utf-8')

csv = convert_df_to_csv(filtered_data)

st.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_data.csv",
    mime="text/csv"
)

