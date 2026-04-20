# =========================================
# Cloud Cost Dashboard (Streamlit)
# =========================================

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

    # Cost Calculation
    df["Compute_Cost"] = df["Usage_Hours"] * df["Price_per_Hour"]
    df["Storage_Cost"] = df["Storage_GB"] * df["Price_per_GB"]
    df["Request_Cost"] = df["Requests"] * df["Price_per_Request"]

    df["Total_Cost"] = (
        df["Compute_Cost"] +
        df["Storage_Cost"] +
        df["Request_Cost"]
    )

    # Metrics
    total_cost = df["Total_Cost"].sum()
    avg_cost = df["Total_Cost"].mean()
    max_service = df.loc[df["Total_Cost"].idxmax()]

    st.subheader("💡 Key Insights")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Cost ($)", f"{total_cost:.2f}")
    col2.metric("Average Cost ($)", f"{avg_cost:.2f}")
    col3.metric("Highest Cost Service", max_service["Service"])

    # Chart
    st.subheader("📈 Cost Distribution")

    fig, ax = plt.subplots()
    ax.bar(df["Service"], df["Total_Cost"])
    ax.set_xlabel("Services")
    ax.set_ylabel("Cost ($)")
    ax.set_title("Cloud Cost Analysis")

    st.pyplot(fig)

    # Table with sorted data
    st.subheader("📋 Cost Breakdown (Sorted)")
    st.dataframe(df.sort_values("Total_Cost", ascending=False))

else:
    st.warning("Please upload an Excel file to continue.")
