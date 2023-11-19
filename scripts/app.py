import pandas as pd
from sqlalchemy import create_engine
from database import etl
from read_queries import query
import streamlit as st

st.set_page_config(page_title='My Personal Finance App',
                   page_icon=':money_with_wings:',
                   layout='wide')

st.title('My Personal Finance App')

tab1, tab2, tab3, tab4 = st.tabs(['Cash Flow', 'Account Balance Over Time', 'Expenses Per Category', 'Insights'])

connection_uri = "postgresql+psycopg2://postgres:password@localhost:5432/personal_finance_dashboard"
etl(connection_uri)
net_worth_over_time = query("net_worth_over_time")

print(net_worth_over_time.head(20))

#st.line_chart(net_worth_over_time, x = "date", y = "net_worth")