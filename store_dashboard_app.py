# store_dashboard_app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page setup
st.set_page_config(page_title="💼 Store Sales Dashboard", layout="wide")

# Custom CSS to improve aesthetics
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }
    .big-font {
        font-size:22px !important;
        font-weight:600;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("📊 Store Sales & Profit Analysis")
st.markdown("##### Unlock insights from your retail data with interactive visualizations and smart filters.")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("Sample - Superstore.csv", encoding='latin1')

df = load_data()

# Clean data
df.drop(columns=["Row ID", "Postal Code"], inplace=True)
df.drop_duplicates(inplace=True)
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])
df["Month-Year"] = df["Order Date"].dt.to_period('M')

# Sidebar filters
with st.sidebar:
    st.header("🔍 Filter Panel")
    category_filter = st.multiselect("Choose Categories", df["Category"].unique(), default=df["Category"].unique())
    segment_filter = st.multiselect("Choose Segments", df["Segment"].unique(), default=df["Segment"].unique())

# Filtered data
filtered_df = df[(df["Category"].isin(category_filter)) & (df["Segment"].isin(segment_filter))]

# Tabs for each section
tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "📊 Categories", "🎯 Segments", "🗂️ Extras"])

with tab1:
    st.markdown("### 📅 Monthly Sales & Profit Trends")
    monthly_sales = filtered_df.groupby('Month-Year')[['Sales', 'Profit']].sum()
    fig1, ax1 = plt.subplots(figsize=(12, 4))
    monthly_sales.plot(ax=ax1, marker='o')
    ax1.set_title("Monthly Sales and Profit")
    ax1.grid(True)
    st.pyplot(fig1)

with tab2:
    st.markdown("### 🧺 Category-wise Insights")
    
    # Category bar chart
    cat_summary = filtered_df.groupby("Category")[["Sales", "Profit"]].sum().reset_index()
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.barplot(data=cat_summary, x="Category", y="Sales", color="skyblue", label="Sales", ax=ax2)
    sns.barplot(data=cat_summary, x="Category", y="Profit", color="orange", label="Profit", ax=ax2)
    ax2.set_title("Sales vs Profit by Category")
    ax2.legend()
    st.pyplot(fig2)

    # Sub-Category horizontal bar
    st.markdown("### 📌 Profit by Sub-Category")
    subcat_profit = filtered_df.groupby("Sub-Category")["Profit"].sum().sort_values()
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    subcat_profit.plot(kind='barh', color='mediumseagreen', ax=ax3)
    ax3.set_title("Profit by Sub-Category")
    ax3.grid(True)
    st.pyplot(fig3)

with tab3:
    st.markdown("### 🎯 Segment Performance Overview")

    seg_perf = filtered_df.groupby("Segment")[["Sales", "Profit"]].sum().reset_index()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 📊 Bar Chart")
        fig4, ax4 = plt.subplots(figsize=(6, 4))
        sns.barplot(data=seg_perf, x="Segment", y="Sales", color="lightblue", label="Sales", ax=ax4)
        sns.barplot(data=seg_perf, x="Segment", y="Profit", color="salmon", label="Profit", ax=ax4)
        ax4.legend()
        st.pyplot(fig4)

    with col2:
        st.markdown("#### 🥧 Pie Chart")
        fig5, ax5 = plt.subplots()
        ax5.pie(seg_perf["Sales"], labels=seg_perf["Segment"], autopct='%1.1f%%', startangle=90)
        ax5.set_title("Sales by Segment")
        st.pyplot(fig5)

with tab4:
    st.markdown("### 🗂️ Extra Visuals & Insights")

    st.markdown("#### 📍 Top & Bottom States by Profit")
    col3, col4 = st.columns(2)
    top_states = filtered_df.groupby("State")[["Sales", "Profit"]].sum().sort_values(by="Profit", ascending=False).head(10)
    bottom_states = filtered_df.groupby("State")[["Sales", "Profit"]].sum().sort_values(by="Profit").head(10)

    with col3:
        st.dataframe(top_states.style.highlight_max(axis=0))
    with col4:
        st.dataframe(bottom_states.style.highlight_min(axis=0))

    st.markdown("#### 💸 Discount vs Profit (Scatter Plot)")
    fig6, ax6 = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=filtered_df, x="Discount", y="Profit", hue="Category", ax=ax6)
    ax6.set_title("Discount vs Profit")
    ax6.grid(True)
    st.pyplot(fig6)

# Footer
st.markdown("---")
st.markdown("Built  by **Nandita** ")
