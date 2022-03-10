from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st


def offset_month(date, n):
    return date.replace(month=date.month + n if date.month + n > 0 else 12)


def __sidebar(df: pd.DataFrame):
    st.sidebar.header("Filter")
    _store = st.sidebar.selectbox("Select Store", ["All Store", *df.city.unique()], index=0)
    _time = st.sidebar.selectbox("Select Time", ["Lifetime", *df.time.sort_values().dt.strftime('%B %Y').unique()], index=0)

    df = df[df.city == _store] if _store != "All Store" else df
    current_df = df[df.time.dt.strftime('%B %Y') == _time] if _time != "Lifetime" else df

    if _time != "Lifetime":
        previous_month = datetime.strptime(_time, '%B %Y')
        previous_month = offset_month(previous_month, -1).strftime('%B %Y')
        previous_df = df[df.time.dt.strftime('%B %Y') == previous_month]
    else:
        previous_df = df.iloc[0:0]
    return previous_df, current_df


def __overview(current_df: pd.DataFrame, previous_df: pd.DataFrame = pd.DataFrame()):
    st.subheader("Overview")

    col1, col2, col3, col4 = st.columns(4)
    previous_transaction, current_transaction = len(previous_df.index), len(current_df.index)
    delta_transaction = current_transaction - previous_transaction

    col1.metric(label="Total Sales", value=current_transaction, delta=delta_transaction)

    previous_item_sold, current_item_sold = previous_df.quantity.sum(), current_df.quantity.sum()
    delta_item_sold = current_item_sold - previous_item_sold

    col2.metric(label="Item Sold", value=current_item_sold, delta=str(delta_item_sold))

    previous_gross_income, current_gross_income = previous_df.gross_income.sum(), current_df.gross_income.sum()
    delta_gross_income = current_gross_income - previous_gross_income

    col3.metric(label="Total Sales", value=f'{current_gross_income:,.2f}', delta='%.2f' % delta_gross_income)

    previous_rating, current_rating = previous_df.rating.mean(), current_df.rating.mean()
    delta_rating = current_rating - previous_rating

    col4.metric(label="Rating", value=f'{current_rating:.1f}/10', delta='%.1f' % delta_rating)

    sales = current_df.groupby(current_df.time.dt.strftime('%d %B %Y')).sum().reset_index()
    sales.time = pd.to_datetime(sales.time)

    col1, col2 = st.columns([3, 1])
    col1.subheader("Revenue History")
    col2.subheader("Revenue Distribution")
    fig = px.bar(sales, x="time", y="gross_income")

    col1.plotly_chart(fig, use_container_width=True)

    sales_dist = current_df.groupby("city").agg({"gross_income": "sum"}).reset_index()
    sales_dist.columns = ["city", "revenue"]
    col2.plotly_chart(px.pie(sales_dist, names="city", values="revenue"), use_container_width=True)

    st.title("Daily Performance")

    weekly_df = current_df.groupby([current_df.time.dt.strftime('%F'), current_df.time.dt.strftime('%A')]).agg({"invoice_id": "count"})
    weekly_df.index.names = ["date", "day"]
    weekly_df = weekly_df.groupby("day").mean().reset_index()

    daily_df = current_df.groupby([current_df.time.dt.strftime('%D'), current_df.time.dt.strftime('%H')]).agg({"invoice_id": "count"})
    daily_df.index.names = ["date", "hour"]
    daily_df = daily_df.groupby("hour").mean().reset_index()

    col1, col2 = st.columns([2, 1])
    col1.plotly_chart(px.bar(weekly_df, x="day", y="invoice_id"), use_container_width=True)
    col2.plotly_chart(px.bar(daily_df, x="hour", y="invoice_id"), use_container_width=True)

    st.title("Sales Distribution")

    sales_source = current_df.groupby([current_df.time.dt.strftime("%d %B %Y"), "product_line"]).agg(
        {"invoice_id": "count", "quantity": "sum", "gross_income": "sum"}).reset_index()

    selected_line = st.multiselect("Select Product Line", sales_source.product_line.unique(), ["Electronic accessories"])
    line_df = sales_source[sales_source.product_line.isin(selected_line)]

    col1, col2 = st.columns([2, 1])
    col1.subheader("Sales History")
    col1.plotly_chart(px.bar(line_df, x="time", y="quantity", color="product_line"), use_container_width=True)
    product_line_df = line_df.groupby("product_line").agg({"quantity": "sum", "gross_income": "sum"}).reset_index()

    col2.subheader("Revenue Distribution")
    col2.plotly_chart(px.pie(product_line_df, names="product_line", values="gross_income"), use_container_width=True)

    st.title("Customer Distribution")
    col1, col2, col3 = st.columns(3)

    gender_df = current_df.groupby("gender").agg({"invoice_id": "count"}).reset_index().replace({"invoice_id", "count"})
    payment_df = current_df.groupby("payment").agg({"invoice_id": "count"}).reset_index().replace({"invoice_id", "count"})
    member_df = current_df.groupby("customer_type").agg({"invoice_id": "count"}).reset_index().replace({"invoice_id", "count"})

    col1.plotly_chart(px.pie(gender_df, labels="gender", values="invoice_id", title="Gender"), use_container_width=True)
    col2.plotly_chart(px.pie(payment_df, labels="payment", values="invoice_id", title="Payment"), use_container_width=True)
    col3.plotly_chart(px.pie(member_df, labels="customer_type", values="invoice_id", title="Customer Membership"), use_container_width=True)

    st.title("Customer Satisfaction")
    col1, col2 = st.columns([2, 1])

    rating_history_df = current_df.groupby(current_df.time.dt.strftime('%d %B %Y')).agg({"rating": "mean"}).reset_index()
    rating_history_df.time = pd.to_datetime(rating_history_df.time)
    rating_history_df = rating_history_df.sort_values("time")

    col1.subheader("Rating History")
    col1.plotly_chart(px.line(rating_history_df, x="time", y="rating"), use_container_width=True)

    rating_df = current_df.copy()
    rating_df.rating = current_df.rating.round().astype(int)
    rating_df = rating_df.groupby("rating").agg({"invoice_id": "count"}).reset_index().replace({"invoice_id", "count"})
    rating_df.columns = ["rating", "count"]
    rating_df = rating_df.sort_values("rating")

    col2.subheader("Rating Distribution")
    col2.plotly_chart(px.bar(rating_df, x="rating", y="count"), use_container_width=True)


def dashboard_page(df: pd.DataFrame):
    st.title("Dashboard")
    previous_df, current_df = __sidebar(df)
    __overview(current_df, previous_df)
