import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import requests

# Load data from the provided CSV link
url = 'https://raw.githubusercontent.com/dilshansr/Centrix_Data/c88fd42421393ad04b0f235d78fbb199c085e37c/SampleNewDF.csv'
response = requests.get(url)
data = BytesIO(response.content)
df = pd.read_csv(data)

# Convert 'created_at' column to datetime format
df['created_at'] = pd.to_datetime(df['created_at'])

# Extract the hour of the day and day of the week
df['hour_of_day'] = df['created_at'].dt.hour
df['day_of_week'] = df['created_at'].dt.day_name()

# Reorder days of the week
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df['day_of_week'] = pd.Categorical(df['day_of_week'], categories=day_order, ordered=True)

# Create a pivot table for the heatmap
heatmap_data = df.pivot_table(index='hour_of_day', columns='day_of_week', aggfunc='size', fill_value=0)

# Streamlit app
st.title("Number of Transactions by Hour of Day and Day of Week")

# Plotting
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, cmap="YlGnBu", annot=True, fmt=".0f", linewidths=.5)
plt.title('Number of Transactions by Hour of Day and Day of Week')
plt.xlabel('Day of Week')
plt.ylabel('Hour of Day')

# Save the plot to a BytesIO object
buffer = BytesIO()
plt.savefig(buffer, format='png', bbox_inches='tight')
buffer.seek(0)

# Encode the plot image to base64 for displaying in Streamlit
encoded_image = base64.b64encode(buffer.read()).decode()

# Close the plot
plt.close()

# Display the heatmap image
st.image(f'data:image/png;base64,{encoded_image}')
