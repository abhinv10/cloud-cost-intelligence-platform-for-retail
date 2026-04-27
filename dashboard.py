import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Cloud Cost Dashboard", layout="wide")

st.title("☁️ Retail Cloud Cost Dashboard")

# Upload File
uploaded_file = st.file_uploader("Upload your cloud usage Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.subheader("📊 Raw Data")
    st.dataframe(df)

    # ===============================
    # Cost Calculations
    # ===============================
    df["Compute_Cost"] = df["Usage_Hours"] * df["Price_per_Hour"]
    df["Storage_Cost"] = df["Storage_GB"] * df["Price_per_GB"]
    df["Request_Cost"] = df["Requests"] * df["Price_per_Request"]

    df["Total_Cost"] = (
        df["Compute_Cost"] +
        df["Storage_Cost"] +
        df["Request_Cost"]
    )

    # Weekly & Monthly
    df["Weekly_Cost"] = df["Total_Cost"] / 4
    df["Monthly_Cost"] = df["Total_Cost"]

    # Daily Cost (Assuming 30 days month)
    df["Daily_Cost"] = df["Total_Cost"] / 30

    # ===============================
    # Metrics
    # ===============================
    total_cost = df["Total_Cost"].sum()
    avg_cost = df["Total_Cost"].mean()
    max_service = df.loc[df["Total_Cost"].idxmax()]

    st.subheader("💡 Key Insights")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Cost ($)", f"{total_cost:.2f}")
    col2.metric("Average Cost ($)", f"{avg_cost:.2f}")
    col3.metric("Highest Cost Service", max_service["Service"])

    # ===============================
    # Bar Chart - Total Cost
    # ===============================
    st.subheader("📊 Cost Distribution")

    fig1, ax1 = plt.subplots()
    ax1.bar(df["Service"], df["Total_Cost"])
    ax1.set_xlabel("Services")
    ax1.set_ylabel("Cost ($)")
    ax1.set_title("Total Cost per Service")

    st.pyplot(fig1)

    # ===============================
    # Weekly vs Monthly Comparison
    # ===============================
    st.subheader("📊 Weekly vs Monthly Cost Comparison")

    x = range(len(df["Service"]))

    fig2, ax2 = plt.subplots()
    ax2.bar(x, df["Weekly_Cost"], width=0.4, label="Weekly")
    ax2.bar([i + 0.4 for i in x], df["Monthly_Cost"], width=0.4, label="Monthly")

    ax2.set_xticks([i + 0.2 for i in x])
    ax2.set_xticklabels(df["Service"])
    ax2.set_xlabel("Services")
    ax2.set_ylabel("Cost ($)")
    ax2.set_title("Weekly vs Monthly Cost")
    ax2.legend()

    st.pyplot(fig2)

    # ===============================
    # Daily Cost Trend (LINE CHART 🔥)
    # ===============================
    st.subheader("📈 Daily Cost Trend (Estimated)")

    # Simulate 30 days
    days = list(range(1, 31))

    # Total daily cost trend (sum across services)
    daily_total = df["Daily_Cost"].sum()

    daily_values = [daily_total for _ in days]

    fig3, ax3 = plt.subplots()
    ax3.plot(days, daily_values, marker='o')
    ax3.set_xlabel("Days")
    ax3.set_ylabel("Cost ($)")
    ax3.set_title("Estimated Daily Cloud Cost Trend")

    st.pyplot(fig3)

    # ===============================
    # Sorted Table
    # ===============================
    st.subheader("📋 Cost Breakdown (Sorted)")
    st.dataframe(df.sort_values("Total_Cost", ascending=False))

else:
    st.warning("Please upload an Excel file to continue.")
