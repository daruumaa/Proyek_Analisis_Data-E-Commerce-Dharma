import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import streamlit as st
import urllib
from func import DataAnalyzer, BrazilMapPlotter
from babel.numbers import format_currency
sns.set(style='dark')
st.set_option('deprecation.showPyplotGlobalUse', False)

# Dataset
datetime_cols = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]
all_df = pd.read_csv('/content/data/all_data.csv')
all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(inplace=True)

# Geolocation Dataset
geolocation = pd.read_csv('/content/data/geolocation.csv')
data = geolocation.drop_duplicates(subset='customer_unique_id')

for col in datetime_cols:
    all_df[col] = pd.to_datetime(all_df[col])

min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()

# Sidebar
with st.sidebar:
    # Logo Image
    st.image("/content/dharmacc.png")

    # Date Range
    start_date, end_date = st.date_input(
        label="# Select Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

# Main
main_df = all_df[(all_df["order_approved_at"] >= str(start_date)) & 
                 (all_df["order_approved_at"] <= str(end_date))]

function = DataAnalyzer(main_df)
map_plot = BrazilMapPlotter(data, plt, mpimg, urllib, st)

daily_orders_df = function.create_daily_orders_df()
sum_spend_df = function.create_sum_spend_df()
sum_order_items_df = function.create_sum_order_items_df()
review_score, common_score = function.review_score_df()
state, most_common_state = function.create_bystate_df()
order_status, common_status = function.create_order_status()

# Title
st.header("E-Commerce Dashboard :convenience_store:")

st.subheader("Main Order Data")
tab1, tab2 = st.tabs(["Daily Orders", "Customer Spend Money"])

with tab1:
    st.subheader("Daily Orders")
    col1, col2 = st.columns(2)

    with col1:
        st.metric(label= "Total Order", value = daily_orders_df["order_count"].sum())

    with col2:
        st.metric(label= "Total Revenue", value = format_currency(daily_orders_df["revenue"].sum(), "IDR", locale="id_ID"))
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(
        daily_orders_df["order_approved_at"],
        daily_orders_df["order_count"],
        marker="o",
        linewidth=2,
        color="#FE6B38"
    )
    ax.tick_params(axis="x", rotation=45)
    ax.tick_params(axis="y", labelsize=15)
    st.pyplot(fig)

with tab2:
    st.subheader("Customer Spend Money")
    col1, col2 = st.columns(2)

    with col1:
        st.metric(label= "Total Spend", value = format_currency(sum_spend_df["total_spend"].sum(), "IDR", locale="id_ID"))

    with col2:
        st.metric(label= "Average Spend", value = format_currency(sum_spend_df["total_spend"].mean(), "IDR", locale="id_ID"))

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(45, 25))

    colors = ["#FE6B38", "#652B20", "#652B20", "#652B20", "#652B20"]

    sns.barplot(x="product_count", y="product_category_name_english", data=sum_order_items_df.head(5), palette=colors, ax=ax[0])
    ax[0].set_ylabel(None)
    ax[0].set_xlabel("Number of Sales", fontsize=30)
    ax[0].set_title("Produk paling banyak terjual", loc="center", fontsize=50)
    ax[0].tick_params(axis ='y', labelsize=35)
    ax[0].tick_params(axis ='x', labelsize=30)

    sns.barplot(x="product_count", y="product_category_name_english", data=sum_order_items_df.sort_values(by="product_count", ascending=True).head(5), palette=colors, ax=ax[1])
    ax[1].set_ylabel(None)
    ax[1].set_xlabel("Number of Sales", fontsize=30)
    ax[1].invert_xaxis()
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_title("Produk paling sedikit terjual", loc="center", fontsize=50)
    ax[1].tick_params(axis='y', labelsize=35)
    ax[1].tick_params(axis='x', labelsize=30)

    st.pyplot(fig)

# Order Items
st.subheader("Order Items")
col1, col2 = st.columns(2)

with col1:
    st.metric(label= "Total Items", value = sum_order_items_df["product_count"].sum())

with col2:
    st.metric(label= "Average Items", value = sum_order_items_df["product_count"].mean())

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(45, 25))

colors = ["#FE6B38", "#652B20", "#652B20", "#652B20", "#652B20"]

sns.barplot(x="product_count", y="product_category_name_english", data=sum_order_items_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=30)
ax[0].set_title("Produk paling banyak terjual", loc="center", fontsize=50)
ax[0].tick_params(axis ='y', labelsize=35)
ax[0].tick_params(axis ='x', labelsize=30)

sns.barplot(x="product_count", y="product_category_name_english", data=sum_order_items_df.sort_values(by="product_count", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Produk paling sedikit terjual", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

# Review Score
st.subheader("Review Score")
col1,col2 = st.columns(2)

with col1:
    st.metric(label= "Average Review Score", value = review_score.mean())

with col2:
    st.metric(label= "Most Common Review Score", value = review_score.value_counts().index[0])

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=review_score.index, 
            y=review_score.values, 
            order=review_score.index,
            palette=["#FE6B38" if score == common_score else "#652B20" for score in review_score.index]
            )

plt.title("Rating by customers for service", fontsize=15)
plt.xlabel("Rating")
plt.ylabel("Count")
plt.xticks(fontsize=12)
st.pyplot(fig)

# Customer Demographic
st.subheader("Review Score")
col1,col2 = st.columns(2)

with col1:
  st.metric(label= "Most Common State", value = state.customer_state.value_counts().index[0])

  fig, ax = plt.subplots(figsize=(12, 6))
  sns.barplot(x=state.customer_state.value_counts().index,
                y=state.customer_count.values, 
                data=state,
                palette=["#FE6B38" if score == most_common_state else "#652B20" for score in state.customer_state.value_counts().index]
                    )

  plt.title("Number customers from State", fontsize=15)
  plt.xlabel("State")
  plt.ylabel("Number of Customers")
  plt.xticks(fontsize=12)
  st.pyplot(fig)

with col2:
    st.metric(label= "Most Common Order Status", value = order_status.value_counts().index[0])

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=order_status.index,
                y=order_status.values,
                order=order_status.index,
                palette=["#FE6B38" if score == common_status else "#652B20" for score in order_status.index]
                )
    
    plt.title("Order Status", fontsize=15)
    plt.xlabel("Status")
    plt.ylabel("Count")
    plt.xticks(fontsize=12)
    st.pyplot(fig)


# Customer Spend Money
st.subheader("Geolocation")
col1,col2 = st.columns(2)

with col1:
    map_plot.plot()

with col2:
    with st.expander("See Explanation"):
        st.write('Menurut grafik yang telah dibuat, terlihat bahwa terdapat lebih banyak pelanggan di wilayah tenggara dan selatan. Selain itu, ditemukan bahwa lebih banyak pelanggan berada di kota-kota yang berfungsi sebagai ibu kota, seperti São Paulo, Rio de Janeiro, Porto Alegre, dan lain-lain.')

st.caption('Copyright (C) Abimanyu Dharma Kamanungsan 2024')

