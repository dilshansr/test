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

# Get the top 10 payers and top 10 payees
top_payers = df['payer_bank_name'].value_counts().nlargest(10).index
top_payees = df['final_payee_bank_name'].value_counts().nlargest(10).index

# Filter the DataFrame based on the top payers and payees
filtered_df = df[df['payer_bank_name'].isin(top_payers) & df['final_payee_bank_name'].isin(top_payees)]

# Set up the Streamlit app
st.title("Interactive Bank-to-Bank Transactions Heatmap")

# Radio buttons for selecting between 'Count' and 'Amount'
selected_value = st.radio('Select Metric:', ['transaction_count', 'total_amount'])

# Group by payer_bank_name, final_payee_bank_name, and calculate count and total amount
grouped_df = filtered_df.groupby(['payer_bank_name', 'final_payee_bank_name']).agg(
    transaction_count=pd.NamedAgg(column='paying_amount', aggfunc='count'),
    total_amount=pd.NamedAgg(column='paying_amount', aggfunc='sum')
).reset_index()

# Pivot the DataFrame to create a matrix of payer banks vs. final payee banks
pivot_df = grouped_df.pivot(index='payer_bank_name', columns='final_payee_bank_name', values=selected_value).fillna(0)

# Divide the values by 1000 for 'total_amount' and format the annotations accordingly
if selected_value == 'total_amount':
    pivot_df = pivot_df / 1000

# Sort the index (Y-axis) in descending order
pivot_df = pivot_df.sort_index(ascending=False)

# Plotting a heatmap with adjusted parameters for clarity and expanded cell size
fig, ax = plt.subplots(figsize=(18, 12))  # Adjust the figsize for expanded cell size
sns.heatmap(pivot_df, cmap='YlGnBu', annot=True, fmt='.1f' if selected_value == 'total_amount' else '.0f',
            cbar_kws={'label': selected_value}, linewidths=0.5, square=True, annot_kws={'size': 8})

# Adjust font size or rotate axis labels
plt.xticks(rotation=45, ha='right', fontsize=8)
plt.yticks(rotation=0, ha='right', fontsize=8)

plt.title('Bank-to-Bank Transactions Heatmap')
plt.xlabel('Final Payee Bank Name')
plt.ylabel('Payer Bank Name')

# Display the heatmap image
st.pyplot(fig)

# Close the plot
plt.close()
