import pandas as pd
from sqlalchemy import create_engine
import streamlit

def extract():
    raw_transactions = pd.read_csv('../data/transactions_list.csv')
    return raw_transactions

def transform(df):
    col_names = ['Type', 'Date', 'Title', 'Amount', 'Currency', 'Category', 'Account', 'Status']
    cleaned_df = df.loc[df['Status'] == 'Reconciled', col_names]
    new_col_names = ['type', 'date', 'item', 'amount', 'currency', 'category', 'account', 'status']
    cleaned_df.columns = new_col_names
    cleaned_df['date'] = pd.to_datetime(cleaned_df['date'])
    return cleaned_df

def load(df, db_table, connection_uri):
    db_engine = create_engine(connection_uri)
    df.to_sql(
        name = db_table,
        con = db_engine,
        if_exists = "replace",
        index = False)

def etl(connection_uri):
    raw_transactions = extract()
    cleaned_transactions = transform(raw_transactions)
    load(cleaned_transactions, "transactions", connection_uri)

def read_query_from_file(file_path, query_name):
    with open(file_path, 'r') as file:
        content = file.read()

    queries = [q.strip() for q in content.split('--@name:')]
    for q in queries:
        lines = q.split('\n', 1)
        name = lines[0].strip()
        query = lines[1].strip() if len(lines) > 1 else ''
        if name == query_name:
            return query

    raise ValueError(f"Query with name '{query_name}' not found in the file.")

def query_from_file(file_path, query_name, connection_uri):
    query = read_query_from_file(file_path, query_name)
    db_engine = create_engine(connection_uri)
    df = pd.read_sql(query, db_engine)
    return df

connection_uri = "postgresql+psycopg2://postgres:password@localhost:5432/personal_finance_dashboard"

etl(connection_uri)
networth_over_time = query_from_file("queries.sql", "net_worth_over_time", connection_uri)

print(networth_over_time.head(20))