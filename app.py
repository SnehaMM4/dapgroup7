#import libraries
import pandas as pd
import numpy as np
import streamlit as st
import plotly as px

#page configuration
# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Trnansactions Analysis Dashboard", page_icon=":mechanical_arm:", layout="wide")

#read in data
@st.cache_data
def get_data():
    df = pd.read_csv('credit_card_transactions_truncated.csv',index_col=0)
    return df

df = get_data()

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
category = st.sidebar.multiselect(
    "Select the Category:",
    options=df["category"].unique(),
    default=df["category"].unique()
)


gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["gender"].unique(),
    default=df["gender"].unique()
)

df_selection = df.query(
    "category == @category & gender == @gender"
)

# Check if the dataframe is empty:
if df_selection.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop() # This will halt the app from further execution.

# ---- MAINPAGE ----
st.title(":bar_chart: Transactions Dashboard")
st.markdown("##")

# TOP KPI's
fraud_amount = int(df_selection["amt"].sum())
average_fraud_amount = int(df_selection["amt"].mean())
fraud_count = df_selection.shape[0]

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Fraud Amount:")
    st.subheader(f"US $ {fraud_amount}")
with middle_column:
    st.subheader("Average Fraud Amount:")
    st.subheader(f"US $ {average_fraud_amount}")
with right_column:
    st.subheader("Fraud Count:")
    st.subheader(f"{fraud_count}")

st.markdown("""---""")

# FRAUD BY CATEGORY [BAR CHART]
sales_by_product_line1 = df_selection.groupby(by=["category"])[["amt"]].sum().sort_values(by="amt")
fig_product_sales1 = px.bar(
    sales_by_product_line1,
    x="amt",
    y=sales_by_product_line1.index,
    orientation="h",
    title="<b>FRAUD BY CATEGORY</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line1),
    template="plotly_white",
)
fig_product_sales1.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# FRAUD BY STATE [BAR CHART]
sales_by_product_line2 = df_selection.groupby(by=["state"])[["amt"]].sum().sort_values(by="amt")
fig_product_sales2 = px.bar(
    sales_by_product_line2,
    x="amt",
    y=sales_by_product_line2.index,
    orientation="h",
    title="<b>FRAUD BY STATE</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line2),
    template="plotly_white",
)
fig_product_sales2.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# FRAUD BY GENDER [BAR CHART]
sales_by_product_line3 = df_selection.groupby(by=["gender"])[["amt"]].sum().sort_values(by="amt")
fig_product_sales3 = px.bar(
    sales_by_product_line3,
    x="amt",
    y=sales_by_product_line3.index,
    orientation="h",
    title="<b>FRAUD BY GENDER</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line3),
    template="plotly_white",
)
fig_product_sales3.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

left_column, middle_column, right_column = st.columns(3)
left_column.plotly_chart(fig_product_sales1, use_container_width=True)
middle_column.plotly_chart(fig_product_sales2, use_container_width=True)
right_column.plotly_chart(fig_product_sales3, use_container_width=True)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
