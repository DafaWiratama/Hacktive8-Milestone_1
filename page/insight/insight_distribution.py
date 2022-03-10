import pandas as pd
import streamlit as st
import plotly.express as px


def insight_distribution(df: pd.DataFrame):
    st.title("Distribution Insight")
    st.markdown("This Insight page is for the month of **March 2019 only**.")

    st.header("Column Correlation")
    col1, col2 = st.columns([1, 2])
    col1.plotly_chart(px.imshow(df.corr(), labels=dict(title="Correlation Matrix"), text_auto=True), use_container_width=True)
    col2.markdown("""
    ### Product Line Performance
    > This is the correlation of each variable in the month of March 2019.
    > From the matrix above, we can see that many column are in high degree of correlation but after some digging we can see that those column are in correlation
    > because they are the side effect of the same variable like `total = qty * price`.
    """)
    st.header("Correlated Columns with 'Gross Income'")
    col1, col2 = st.columns([2, 1])
    col2.plotly_chart(px.scatter(df, x="gross_income", y="quantity"), use_container_width=True)
    col1.markdown("""
    ### Product Line Performance
    > This is the scatter plot of gross_income and quantity in the month of March 2019.
    > From the graph above, we can see that more quantity per transaction to gross_income but they are correlate by same mathematical equation.
    """)
