import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load data from the provided CSV file
data_url = 'https://raw.githubusercontent.com/dilshansr/Centrix_Data/c88fd42421393ad04b0f235d78fbb199c085e37c/SampleNewDF.csv'
df = pd.read_csv(data_url)

# Title
st.title("Distribution of Transactions by Fund Transfer Type")

# Query to retrieve fund_transfer_type and count of each type
pie_data = df['fund_transfer_type'].value_counts().reset_index()
pie_data.columns = ['fund_transfer_type', 'transaction_count']

# Create a pie chart using plotly.graph_objects
fig = go.Figure(data=[go.Pie(labels=pie_data['fund_transfer_type'], values=pie_data['transaction_count'])])
fig.update_layout(title='Distribution of Transactions by Fund Transfer Type')

# Display the pie chart using Streamlit
st.plotly_chart(fig)
