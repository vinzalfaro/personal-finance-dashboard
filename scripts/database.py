import pandas as pd
from sqlalchemy import create_engine
from read_queries import query

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


