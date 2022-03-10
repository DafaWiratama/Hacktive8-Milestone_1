import pandas as pd
import streamlit as st
from page.insight.insight_sales import insight_sales
from page.insight.insight_distribution import insight_distribution
from page.insight.insight_store_performance import insight_store_performance


def insight_page(df: pd.DataFrame):
    selected_sub = st.sidebar.selectbox("Category", ["Transaction", "Distribution", "Store Performance"], index=0)
    if selected_sub == "Transaction":
        insight_sales(df)
    elif selected_sub == "Distribution":
        insight_distribution(df)
    elif selected_sub == "Store Performance":
        insight_store_performance(df)
