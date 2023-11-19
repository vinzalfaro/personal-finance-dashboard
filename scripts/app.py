import pandas as pd
from sqlalchemy import create_engine
from database import etl
from read_queries import query
import streamlit as st
import plotly.express as px

st.set_page_config(page_title='My Personal Finance App',
                   page_icon=':money_with_wings:',
                   layout='wide')

st.title('My Personal Finance App')

tab1, tab2, tab3, tab4 = st.tabs(['Net Worth', 'Accounts', 'Expenses Per Category', 'Insights'])

connection_uri = "postgresql+psycopg2://postgres:password@localhost:5432/personal_finance_dashboard"
etl(connection_uri)
net_worth_over_time = query("net_worth_over_time")
accounts_over_time = query("accounts_over_time")
amount_over_time = pd.merge(net_worth_over_time, accounts_over_time, on='date')
print(amount_over_time.head(20))


with tab1:
    st.header("Net Worth")

    column_options = ['binance', 'gcash', 'grabpay', 'maya', 'ronin', 'seabank', 'shopeepay', 'unionbank', 'wallet', 'net_worth']
    selected_columns = st.multiselect('Select accounts to display:', column_options, default='net_worth')

    # create a line chart using the selected columns
    fig_account_balance = px.line(amount_over_time , x='date', y=selected_columns, title='Account Balance Over Time', 
    width=1200, height= 600)

    # display the chart
    st.plotly_chart(fig_account_balance)
with tab2:
    st.header("Accounts")