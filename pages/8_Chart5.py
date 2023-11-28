import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Dataset URL
dataset_url = 'https://raw.githubusercontent.com/dilshansr/Centrix_Data/c88fd42421393ad04b0f235d78fbb199c085e37c/SampleNewDF.csv'

# Load the dataset
df = pd.read_csv(dataset_url)

# Convert 'created_at' column to datetime format
df['created_at'] = pd.to_datetime(df['created_at'])

# Calculate the yearly average transaction count for each payment category
avg_df = df.groupby(['payment_category', df['created_at'].dt.year])['id'].count().reset_index()

# Initialize Streamlit app
st.title('Yearly Average Transaction Count by Payment Category')

# Plotting the pie chart using Plotly Graph Objects
fig = go.Figure(data=[go.Pie(
    labels=avg_df['payment_category'],
    values=avg_df['id'],
    title='Yearly Average Transaction Count by Payment Category'
)])

# Display the pie chart in Streamlit app
st.plotly_chart(fig)
