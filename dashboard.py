import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv("data/bls_data.csv")

# Map series IDs to human-readable names
series_descriptions = {
    "CES0000000001": "Total Non-Farm Employment",
    "LNS14000000": "Unemployment Rate"
}
df['series_description'] = df['series_id'].map(series_descriptions)

# Streamlit App Title
st.title("US Labor Statistics Dashboard")

# Dropdown to Select a Metric
selected_series = st.selectbox(
    "Select a Metric to Visualize:",
    df['series_description'].unique()
)

# Filter Data Based on the Selection
filtered_data = df[df['series_description'] == selected_series]

# Plot the Data
fig = px.line(filtered_data, x="date", y="value",
              title=f"{selected_series} Over Time",
              labels={"value": "Value", "date": "Date"})
st.plotly_chart(fig)

# Show the Latest Data
st.subheader(f"Latest Data for {selected_series}")
latest_data = filtered_data.sort_values(by="date", ascending=False).head(1)
st.write(latest_data)



