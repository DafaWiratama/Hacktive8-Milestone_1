import pandas as pd
import streamlit as st
import plotly.express as px


def group_by_day(df: pd.DataFrame):
    df = df.groupby(["city", df.time.dt.strftime("%d %B %Y")]).agg({"invoice_id": "count", "quantity": "sum", "rating": "mean", "gross_income": "sum"})
    df = df.reset_index()
    df = df.sort_values("time")
    df.time = pd.to_datetime(df.time)
    df = df.rename(columns={"time": "date", "invoice_id": "count"})
    return df


opened_tab = None


def plot_sub_article(df, x, y, color, title=None, body=None):
    with st.expander(label=title):
        col1, col2 = st.columns([2, 1])
        col1.plotly_chart(px.area(df, x=x, y=y, color="city", line_shape='spline'), use_container_width=True)
        col2.plotly_chart(px.box(df, x=color, y=y, color="city", points="all"), use_container_width=True)
        st.markdown("""
        ### Analysis  
        {}
        """.format(body)) if body else None


articles = [
    {
        "title": "Transaction History",
        "x": "date",
        "y": "count",
        "color": "city",
        "body": """
        > This graph shows the number of transactions per day over one month.  
        > and from this we can see that the number of transactions is decreasing over the month and i think we should make new marketing movement to increase the sales , 
        """
    },
    {
        "title": "Sales Quantity History",
        "x": "date",
        "y": "quantity",
        "color": "city",
        "body": """
        > This graph shows the sales quantity per day over one month.  
        > and from this we can see that the sales quantity is decreasing over the month and i think we should make new marketing bundle to increase the quantity of each product sales , 
        """
    },
    {
        "title": "Transaction Rating History",
        "x": "date",
        "y": "rating",
        "color": "city",
        "body": """
        > This graph shows the rating of transactions per day over one month.  
        > and from this we can see that the rating of transactions is decreasing over the month my suggestion is that we should investigate more on our customer facing employee to see why the rating is decreasing , 
        """,
    },
    {
        "title": "Gross Income History",
        "x": "date",
        "y": "gross_income",
        "color": "city",
        "body": """
        > This Graph shows the gross income per day over one month.  
        > and from this we can see that the gross income is decreasing over the month this graph reflects the decrease of transaction and sales quantity to improve the income we should improve those 2 factors , 
        """,
    }
]


def insight_sales(df: pd.DataFrame):
    st.title("Sales Insight")
    st.markdown("This Insight page is for the month of **March 2019 only**.")

    df = group_by_day(df)
    for article in articles:
        plot_sub_article(df, x=article["x"], y=article["y"], color=article["color"], title=article["title"], body=article["body"])
