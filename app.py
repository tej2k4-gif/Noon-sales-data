import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Noon UAE — Sales Dashboard", page_icon="🛒", layout="wide")

# ----------------------------------------------------------------------------
# Data loading
# ----------------------------------------------------------------------------
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["order_date"])
    return df


DATA_PATH = "noon_uae_sales_data.csv"
df = load_data(DATA_PATH)

st.title("🛒 Noon UAE — Sales Dashboard")
st.caption(
    "Synthetic 3-month order dataset (Apr–Jun 2026) for demo purposes. "
    "Not real Noon data."
)

# ----------------------------------------------------------------------------
# Sidebar filters
# ----------------------------------------------------------------------------
st.sidebar.header("Filters")

min_date, max_date = df["order_date"].min().date(), df["order_date"].max().date()
date_range = st.sidebar.date_input(
    "Order date range", value=(min_date, max_date), min_value=min_date, max_value=max_date
)

cities = st.sidebar.multiselect("City", sorted(df["city"].unique()), default=[])
categories = st.sidebar.multiselect("Category", sorted(df["category"].unique()), default=[])
statuses = st.sidebar.multiselect("Delivery status", sorted(df["delivery_status"].unique()), default=[])
vip_only = st.sidebar.checkbox("Noon VIP orders only", value=False)

filtered = df.copy()
if isinstance(date_range, tuple) and len(date_range) == 2:
    start, end = date_range
    filtered = filtered[
        (filtered["order_date"].dt.date >= start) & (filtered["order_date"].dt.date <= end)
    ]
if cities:
    filtered = filtered[filtered["city"].isin(cities)]
if categories:
    filtered = filtered[filtered["category"].isin(categories)]
if statuses:
    filtered = filtered[filtered["delivery_status"].isin(statuses)]
if vip_only:
    filtered = filtered[filtered["is_noon_vip"]]

if filtered.empty:
    st.warning("No orders match the selected filters.")
    st.stop()

# ----------------------------------------------------------------------------
# KPI row
# ----------------------------------------------------------------------------
total_revenue = filtered["total_amount_aed"].sum()
total_orders = len(filtered)
avg_order_value = filtered["total_amount_aed"].mean()
delivered_rate = (filtered["delivery_status"] == "Delivered").mean() * 100
avg_rating = filtered["customer_rating"].mean()

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Revenue", f"AED {total_revenue:,.0f}")
k2.metric("Total Orders", f"{total_orders:,}")
k3.metric("Avg Order Value", f"AED {avg_order_value:,.0f}")
k4.metric("Delivered Rate", f"{delivered_rate:.1f}%")
k5.metric("Avg Rating", f"{avg_rating:.2f} ★")

st.divider()

# ----------------------------------------------------------------------------
# Charts
# ----------------------------------------------------------------------------
c1, c2 = st.columns((2, 1))

with c1:
    st.subheader("Daily Revenue Trend")
    daily = (
        filtered.set_index("order_date")
        .resample("D")["total_amount_aed"]
        .sum()
        .reset_index()
    )
    fig = px.line(daily, x="order_date", y="total_amount_aed", labels={
        "order_date": "Date", "total_amount_aed": "Revenue (AED)"
    })
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Orders by City")
    city_counts = filtered["city"].value_counts().reset_index()
    city_counts.columns = ["city", "orders"]
    fig = px.pie(city_counts, names="city", values="orders", hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

c3, c4 = st.columns(2)

with c3:
    st.subheader("Revenue by Category")
    cat_rev = (
        filtered.groupby("category")["total_amount_aed"]
        .sum()
        .sort_values(ascending=True)
        .reset_index()
    )
    fig = px.bar(cat_rev, x="total_amount_aed", y="category", orientation="h", labels={
        "total_amount_aed": "Revenue (AED)", "category": "Category"
    })
    st.plotly_chart(fig, use_container_width=True)

with c4:
    st.subheader("Payment Method Split")
    pay = filtered["payment_method"].value_counts().reset_index()
    pay.columns = ["payment_method", "orders"]
    fig = px.bar(pay, x="payment_method", y="orders", labels={
        "payment_method": "Payment Method", "orders": "Orders"
    })
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Delivery Status Breakdown")
status_counts = filtered["delivery_status"].value_counts().reset_index()
status_counts.columns = ["delivery_status", "orders"]
fig = px.bar(status_counts, x="delivery_status", y="orders", color="delivery_status")
st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------------------------
# Raw data
# ----------------------------------------------------------------------------
st.subheader("Order-Level Data")
st.dataframe(filtered, use_container_width=True, height=350)

st.download_button(
    "Download filtered data as CSV",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="noon_uae_filtered_orders.csv",
    mime="text/csv",
)
