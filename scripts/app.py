from database import extract, transform, load, drop
from read_queries import query
import streamlit as st
import plotly.express as px
from PIL import Image

def main():
    # ----- PAGE SETUP -----
    st.set_page_config(page_title='Personal Finance Dashboard',
                    page_icon=':money_with_wings:',
                    layout='wide')

    # ----- TITLE & TABS -----
    st.title('Personal Finance Dashboard')
    tab1, tab2, tab3, tab4 = st.tabs(['Home', 'Data', 'Dashboard', 'Documentation'])

    # ----- SIDE BAR ----- 
    with st.sidebar:
        st.header('Filters')
        # Accounts filter
        column_options = ['binance', 'gcash', 'grabpay', 'maya', 'ronin', 'seabank', 'shopeepay', 'unionbank', 'wallet', 'net_worth']
        selected_columns = st.multiselect('Select accounts to display:', column_options, default='net_worth')
        # Views filter
        view = st.radio("Select view:", ["monthly", "weekly", "daily"], index=1, horizontal = True, key = "sidebar")

    # ----- HOME TAB -----
    with tab1:
        with st.container():
            st.subheader('Project Overview')
            st.markdown("""
                        The Personal Finance Dashboard extracts expenditure data from Bluecoins and creates a dashboard to aid in budgeting and financial management. 
                        Bluecoins is an expense tracking app that allows export of data in CSV format. The Personal Finance Dashboard takes this file or 
                        any other file with the same CSV format to generate analytics.
                        """ )
            try:
                personal_finance = Image.open('images/finance.jpg')
                st.image(personal_finance, caption='Source: LittlePigPower/Shutterstock.com', use_column_width=True)
            except FileNotFoundError:
                st.warning(f"Image not found")

        with st.container():
            st.subheader('Motivation Behind the Project')
            st.markdown("""
                        I’ve been using the Bluecoins app to track my expenses for over a year now, and using my recorded data, I want to gain insights about my expenditure. 
                        Some of the questions I aim to answer are as follows:

                        1. Where am I spending the most?
                        2. What should be my daily, weekly, and monthly budget based on my spending patterns?
                        3. Where do most of my money come from?
                        4. What are my most preferred payment and receiving methods?
                        5. How much money comes in and out of my accounts over time?

                        In addition, I wanted to apply what I’ve learned in programming so far. This covers Python (Pandas, SQLAlchemy, Plotly, Streamlit), 
                        SQL (relational databases, how to write queries), Git workflow, project management and documentation.
                        """ )
            try:
                architecture_diagram = Image.open('images/Architecture Diagram.jpg')
                st.image(architecture_diagram, caption='Technologies used', use_column_width=True)
            except FileNotFoundError:
                st.warning(f"Image not found")

        with st.container():
            st.subheader('Get Started')
            st.markdown("""
                        To use the app, kindly follow these instructions:

                        1. Export transactions data from Bluecoins app. This will create a file called ‘transactions_list.csv’.
                        2. Go to the ‘Data’ tab and upload the file. The dashboard is created automatically once the file is uploaded. Dataframes containing raw and
                        derived data are also shown. You can explore the data by clicking on the expanders.
                        3. Go to the ‘Dashboard’ tab and explore the charts. Use the filters on the left sidebar to show specific plots or views.
                        """ )
    try:
        # ----- DATA TAB -----
        with tab2:
            # File input
            connection_uri = "postgresql://postgres:password@postgres:5432/personal_finance_dashboard"
            file = st.file_uploader("Upload file here")

            if st.button("Generate Dashboard"):
                if file is not None:
                    raw_transactions = extract(file)
                    load(raw_transactions, "raw_transactions", connection_uri)
                    cleaned_transactions = transform(raw_transactions)
                    load(cleaned_transactions, "transactions", connection_uri)
                else:
                    st.error("Please upload a file before generating the dashboard.")
            
            if st.button("Clear Data"):
                drop("raw_transactions", connection_uri)
                drop("transactions", connection_uri) 
            
            # DataFrames
            with st.expander('Raw Transactions Data'):
                raw_transactions = query("raw_transactions")
                st.dataframe(raw_transactions, height=400, use_container_width= True)
            with st.expander('Cleaned Transactions Data'):
                cleaned_transactions = query("transactions")
                st.dataframe(cleaned_transactions, height=400, use_container_width= True)
            with st.expander('Accounts Data'):
                accounts = query("daily_amount_over_time")
                st.dataframe(accounts, height=400, use_container_width= True)

        # ----- DASHBOARD TAB -----
        with tab3:
            # Account Balance Over Time
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
            # Payment Methods
            with b1:
                payment_methods = query("payment_methods")
                fig_payment_methods = px.bar(payment_methods, x='account', y='amount', title='Payment Methods')
                st.plotly_chart(fig_payment_methods, use_container_width= True)
            # Receiving Methods
            with b2:
                receiving_methods = query("receiving_methods")
                fig_receiving_methods = px.bar(receiving_methods, x='account', y='amount', title='Receiving Methods')
                st.plotly_chart(fig_receiving_methods, use_container_width= True)

            st.markdown("""---""")

            c1, c2 = st.columns(2)
            # Expenses Per Category
            with c1:
                expenses_per_category = query("expenses_per_category")
                fig_expenses_by_category = px.pie(expenses_per_category, values='expenses', title='Expenses Per Category', names='category', hole=0.4)
                fig_expenses_by_category.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_expenses_by_category, use_container_width= True)
            # Income Per Category
            with c2:
                income_per_category = query("income_per_category")
                fig_income = px.pie(income_per_category, values='income', names='category', title='Income Per Category', hole=0.4)
                fig_income.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_income, use_container_width= True)

            st.markdown("""---""")

            d1, d2 = st.columns(2)
            # Top Expenses
            with d1:
                st.markdown("###### Top Expenses")
                st.dataframe(expenses_per_category, height=400, use_container_width= True)
            # Top Income Sources
            with d2:
                st.markdown("###### Top Income Sources")
                st.dataframe(income_per_category, height=400, use_container_width= True)

            st.markdown("""---""")

            # Expenses Over Time
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
    except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    # ----- DOCUMENTATIONS TAB -----
    with tab4:
        st.subheader('Architecture Diagram')
        try:
            architecture_diagram = Image.open('images/Architecture Diagram.jpg')
            st.image(architecture_diagram)
        except FileNotFoundError:
                st.warning(f"Image not found")

        st.subheader('How It Works')
        try:
            architecture_diagram = Image.open('images/workflow.png')
            st.image(architecture_diagram)
        except FileNotFoundError:
                st.warning(f"Image not found")


if __name__ == '__main__':
    main()
