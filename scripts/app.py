from database import extract, transform, load
from read_queries import query
import streamlit as st
import plotly.express as px

st.set_page_config(page_title='My Personal Finance App',
                   page_icon=':money_with_wings:',
                   layout='wide')

st.title('Personal Finance App')
tab1, tab2, tab3 = st.tabs(['Home', 'Data', 'Dashboard'])

with st.sidebar:
    st.header('Filters')
    column_options = ['binance', 'gcash', 'grabpay', 'maya', 'ronin', 'seabank', 'shopeepay', 'unionbank', 'wallet', 'net_worth']
    selected_columns = st.multiselect('Select accounts to display:', column_options, default='net_worth')
    view = st.radio("Select view:", ["monthly", "weekly", "daily"], horizontal = True, key = "sidebar")

with tab1:
    with st.container():
        st.markdown("""
                    Hi! Welcome to Personal Finance App. You can find the app's GitHub repository [here](https://github.com/vinzalfaro/bluecoins_dashboard).
                    Personal Finance App creates an informative dashboard from your Bluecoins transaction data. 
                    Bluecoins is an expense tracking app which allows exporting of your data in csv format. 
                    Please upload your transactions csv file below and go to the "Dashboard" tab to see your analytics dashboard. 
                    """ )

with tab2:
    file = st.file_uploader("Upload file here")
    if file is not None:
        connection_uri = "postgresql+psycopg2://postgres:password@localhost:5432/personal_finance_dashboard"
        raw_transactions = extract(file)
        load(raw_transactions, "raw_transactions", connection_uri)
        cleaned_transactions = transform(raw_transactions)
        load(cleaned_transactions, "transactions", connection_uri)

    with st.expander('See raw transactions data'):
        raw_transactions = query("raw_transactions")
        st.dataframe(raw_transactions, height=400, use_container_width= True)
    with st.expander('See cleaned transactions data'):
        cleaned_transactions = query("transactions")
        st.dataframe(cleaned_transactions, height=400, use_container_width= True)
    with st.expander('See accounts data'):
        accounts = query("daily_amount_over_time")
        st.dataframe(accounts, height=400, use_container_width= True)

with tab3:
    with st.container():
        if view == 'monthly':   
            monthly_amount_over_time = query("monthly_amount_over_time")
            fig_accounts_over_time = px.line(monthly_amount_over_time , x='month', y=selected_columns, title='Account Balance Over Time')
            st.plotly_chart(fig_accounts_over_time, use_container_width= True)

        elif view == 'weekly':   
            weekly_amount_over_time = query("weekly_amount_over_time")
            fig_accounts_over_time = px.line(weekly_amount_over_time , x='week', y=selected_columns, title='Account Balance Over Time')
            st.plotly_chart(fig_accounts_over_time, use_container_width= True)

        elif view == 'daily':   
            daily_amount_over_time = query("daily_amount_over_time")
            fig_accounts_over_time = px.line(daily_amount_over_time , x='day', y=selected_columns, title='Account Balance Over Time')
            st.plotly_chart(fig_accounts_over_time, use_container_width= True)

    st.markdown("""---""")

    b1, b2 = st.columns(2)
    with b1:
        payment_methods = query("payment_methods")
        fig_payment_methods = px.bar(payment_methods, x='account', y='amount', title='Payment Methods')
        st.plotly_chart(fig_payment_methods, use_container_width= True)
    with b2:
        receiving_methods = query("receiving_methods")
        fig_receiving_methods = px.bar(receiving_methods, x='account', y='amount', title='Receiving Methods')
        st.plotly_chart(fig_receiving_methods, use_container_width= True)

    st.markdown("""---""")

    c1, c2 = st.columns(2)
    with c1:
        expenses_per_category = query("expenses_per_category")
        fig_expenses_by_category = px.pie(expenses_per_category, values='expenses', title='Expenses per category', names='category', hole=0.4)
        fig_expenses_by_category.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_expenses_by_category, use_container_width= True)
        with st.expander("See top expenses"):
            st.header("Top expenses")
            st.dataframe(expenses_per_category, height=400, use_container_width= True)
    with c2:
        income_per_category = query("income_per_category")
        fig_income = px.pie(income_per_category, values='income', names='category', title='Income per category', hole=0.4)
        fig_income.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_income, use_container_width= True)
        with st.expander("See top income sources"):
            st.header("Top income sources")
            st.dataframe(income_per_category, height=400, use_container_width= True)

    st.markdown("""---""")

    with st.container():
        if view == 'monthly':
            monthly_expenses = query("monthly_expenses")
            fig_monthly_expenses = px.line(monthly_expenses, x='month', y='expenses', title='Monthly Expenses')
            st.plotly_chart(fig_monthly_expenses, use_container_width= True)
        elif view == "weekly":
            weekly_expenses = query("weekly_expenses")
            fig_weekly_expenses = px.line(weekly_expenses, x='week', y='expenses', title='Weekly Expenses')
            st.plotly_chart(fig_weekly_expenses, use_container_width= True)
        elif view == "daily":
            daily_expenses = query("daily_expenses")
            fig_daily_expenses = px.line(daily_expenses, x='day', y='expenses', title='Daily Expenses')
            st.plotly_chart(fig_daily_expenses, use_container_width= True)
