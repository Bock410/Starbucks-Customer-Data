import streamlit as st
import pandas as pd
import plotly.express as px
import ast

# 1. Dashboard Styling (Starbucks Green: #00704A)
st.markdown("<h1 style='text-align: center; color: #00704A;'>Starbucks Customer Demand & Revenue Dashboard</h1>", unsafe_allow_html=True)

# 2. Data Preprocessing (Rigor: Handling the Age 118 choice)
# Loading your local source data
profile = pd.read_csv('profile.csv')
transcript = pd.read_csv('transcript.csv')

# Removing records where age 118 acts as a placeholder for missing data [1]
profile_clean = profile[profile['age'] != 118]

# Extracting numeric transaction amounts from the transcript dictionary [2]
transactions = transcript[transcript['event'] == 'transaction'].copy()
transactions['amount'] = transactions['value'].apply(lambda x: ast.literal_eval(x)['amount'])

# Merging data for segment analysis
merged_df = pd.merge(transactions, profile_clean, left_on='person', right_on='id')

# 3. Sidebar Interactivity (Section 4.2 Bonus Opportunity)
st.sidebar.header("Filter Options")
income_val = st.sidebar.slider("Select Minimum Income", 
                               int(profile_clean['income'].min()), 
                               int(profile_clean['income'].max()), 
                               50000)

# Filter the data based on user input
filtered_df = merged_df[merged_df['income'] >= income_val]

# 4. Display Charts (Requirement 3.4: Two distinct types)
# Line Chart: Sales Trend Over Time
trend_data = filtered_df.groupby('time')['amount'].sum().reset_index()
fig1 = px.line(trend_data, x='time', y='amount', 
               title="Revenue Trend Over Time",
               color_discrete_sequence=['#00704A']) # Starbucks Green
st.plotly_chart(fig1)

# Bar Chart: Revenue by Gender Segment
gender_data = filtered_df.groupby('gender')['amount'].sum().reset_index()
fig2 = px.bar(gender_data, x='gender', y='amount', 
              title="Total Revenue by Gender",
              color_discrete_sequence=['#00704A']) # Starbucks Green
st.plotly_chart(fig2)
