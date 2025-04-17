# app.py
import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

# Connect to DB
conn = sqlite3.connect('database.db')

@st.cache_data
def load_data(dept=None):
    query = "SELECT * FROM employees"
    if dept:
        query += f" WHERE Department = '{dept}'"
    return pd.read_sql_query(query, conn)

# Sidebar for Department Filter
st.sidebar.title("Select Department")
departments = pd.read_sql("SELECT DISTINCT Department FROM employees", conn)['Department'].tolist()
selected_dept = st.sidebar.selectbox("Department", departments)

df = load_data(selected_dept)

# Summary Metrics
st.title("Employee Dashboard")

col1, col2, col3 = st.columns(3)
col1.metric("Employee Count", df.shape[0])
col2.metric("Attrition Count", df[df['Attrition'] == 'Yes'].shape[0])
col3.metric("Attrition Rate", f"{(df[df['Attrition'] == 'Yes'].shape[0] / df.shape[0]) * 100:.2f}%")

col4, col5, col6 = st.columns(3)
col4.metric("Avg Age", f"{df['Age'].mean():.1f}")
col5.metric("Avg Salary", f"${df['MonthlyIncome'].mean():,.0f}")
col6.metric("Avg Years at Company", f"{df['YearsAtCompany'].mean():.1f}")

# Charts
st.subheader("Attrition by Education")
fig1 = px.histogram(df[df['Attrition'] == 'Yes'], x="Education")
st.plotly_chart(fig1)

st.subheader("Attrition by Age")
fig2 = px.histogram(df[df['Attrition'] == 'Yes'], x="Age")
st.plotly_chart(fig2)

st.subheader("Attrition by Gender")
fig3 = px.histogram(df[df['Attrition'] == 'Yes'], x="Gender")
st.plotly_chart(fig3)

st.subheader("Attrition by Job Role")
fig4 = px.histogram(df[df['Attrition'] == 'Yes'], x="JobRole")
st.plotly_chart(fig4)

st.subheader("Job Satisfaction Rating by Job Role")
fig5 = px.box(df, x="JobRole", y="JobSatisfaction")
st.plotly_chart(fig5)

