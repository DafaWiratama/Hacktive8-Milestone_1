import streamlit as st
import pandas as pd

from page.page_dashboard import dashboard_page
from page.page_hypothesis_testing import hypothesis_testing_page
from page.page_landing import landing_page
from page.page_insight import insight_page

st.set_page_config(
    page_title='Hacktive8 - Dafa Wiratama - Data Science - Batch 09',
    page_icon="https://avatars.githubusercontent.com/u/43711291",
    layout='wide', initial_sidebar_state='auto')


@st.cache()
def load_data():
    _df = pd.read_csv("dataset/supermarket_sales - Sheet1.csv")
    _df = _df.drop(['Branch', "Tax 5%", "gross margin percentage"], axis=1)
    _df.columns = [
        'invoice_id',
        'city',
        'customer_type',
        'gender',
        'product_line',
        'unit_price',
        'quantity',
        'total',
        'date',
        'time',
        'payment',
        'cogs',
        'gross_income',
        'rating',
    ]

    _df['time'] = pd.to_datetime(_df['time'] + ' ' + _df['date'])
    _df = _df.drop(['date'], axis=1)
    return _df


def container(_df: pd.DataFrame):
    selected_ui = st.sidebar.selectbox(label='Select a UI', options=["Landing", "Dashboard", "Insights", "Hypothesis Testing"], index=0)
    if selected_ui == "Landing":
        landing_page(_df)
    if selected_ui == "Dashboard":
        dashboard_page(_df)
    if selected_ui == "Insights":
        insight_page(_df)
    if selected_ui == "Hypothesis Testing":
        hypothesis_testing_page(_df)


if __name__ == '__main__':
    df = load_data()
    container(df)
