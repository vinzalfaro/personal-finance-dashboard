import pandas as pd
from sqlalchemy import create_engine

def extract(file):
    raw_transactions = pd.read_csv(file)
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

def drop(table, connection_uri):
    db_engine = create_engine(connection_uri)
    with db_engine.connect() as connection:
        connection.execute(f"DROP TABLE IF EXISTS {table};")
