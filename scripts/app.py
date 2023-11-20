import pandas as pd
from sqlalchemy import create_engine
from database import etl
from read_queries import query
import streamlit as st
import plotly.express as px

connection_uri = "postgresql+psycopg2://postgres:password@localhost:5432/personal_finance_dashboard"
etl(connection_uri)

st.set_page_config(page_title='My Personal Finance App',
                   page_icon=':money_with_wings:',
                   layout='wide')

st.title('My Personal Finance App')

tab1, tab2, tab3 = st.tabs(['Accounts', 'Expenses', 'Income'])

with tab1:
    st.header("Accounts")

    amount_over_time = query("amount_over_time")
    column_options = ['binance', 'gcash', 'grabpay', 'maya', 'ronin', 'seabank', 'shopeepay', 'unionbank', 'wallet', 'net_worth']
    selected_columns = st.multiselect('Select accounts to display:', column_options, default='net_worth')
    fig_accounts_over_time = px.line(amount_over_time , x='date', y=selected_columns, title='Account Balance Over Time', 
    width=1200, height= 600)

    st.plotly_chart(fig_accounts_over_time)

with tab2:
    st.header("Expenses")

    expenses_per_category = query("expenses_per_category")
    
    fig_expenses = px.pie(expenses_per_category, values='expenses', names='category', width=700, height=700, hole=0.4,)
    fig_expenses.update_traces(textposition='inside', textinfo='percent+label')

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig_expenses)

    with col2:
        st.dataframe(expenses_per_category, height=550, use_container_width= True)

with tab3:
    st.header("Income")

    income_per_category = query("income_per_category")
    
    fig_income = px.pie(income_per_category, values='income', names='category', width=700, height=700, hole=0.4,)
    fig_income.update_traces(textposition='inside', textinfo='percent+label')

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig_income)

    with col2:
        st.dataframe(income_per_category, height=550, use_container_width= True)