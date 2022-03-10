import pandas as pd
import streamlit as st
import plotly.express as px

day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def insight_store_performance(df: pd.DataFrame):
    df = df.copy()
    st.title("Store Performance")
    st.markdown("This Insight page is for the month of **March 2019 only**.")

    df["date"] = df.time.dt.strftime("%d")
    df["day"] = df.time.dt.strftime("%A")
    df["time"] = df.time.dt.strftime("%H")

    daily_df = df

    col1, col2 = st.columns([2, 1])
    col1.plotly_chart(px.bar(df, x="date", y="total", color="city", barmode='group'), use_container_width=True)
    col2.markdown("""
    ### Store Performance
    > This is the total sales of each store in the month of March 2019.
    > From the graph above, we can see that highest sales are in **Yangon**.
    """)

    col1, col2 = st.columns([1, 2])
    col2.plotly_chart(px.bar(daily_df, x="day", y="total", color="product_line", barmode='group'), use_container_width=True)
    col1.markdown("""
    ### Product Line Performance
    > This is the total sales of each product line in the month of March 2019.
    > From the graph above, we can see that highest average sales are in **Saturday**.
    """)

    col1, col2 = st.columns([2, 1])
    col1.plotly_chart(px.bar(daily_df, x="day", y="quantity", color="payment", barmode='group'), use_container_width=True)
    col2.markdown("""
        ### Sale Quantity Performance
        > This is the total sales of quantity in the month of March 2019.
        > From the graph above, we can see that highest average quantity sales are in **Saturday**.
        """)
