# =========================================
# Retail Cloud Cost Calculator (main.py)
# =========================================

import pandas as pd
import matplotlib.pyplot as plt

def load_data(file_path):
    try:
        df = pd.read_excel(file_path)
        print("✅ File loaded successfully!\n")
        return df
    except FileNotFoundError:
        print("❌ Error: File not found. Please check the file path.")
        exit()

def calculate_cost(df):
    df["Compute_Cost"] = df["Usage_Hours"] * df["Price_per_Hour"]
    df["Storage_Cost"] = df["Storage_GB"] * df["Price_per_GB"]
    df["Request_Cost"] = df["Requests"] * df["Price_per_Request"]

    df["Total_Cost"] = (
        df["Compute_Cost"] +
        df["Storage_Cost"] +
        df["Request_Cost"]
    )
    return df

def analyze_data(df):
    total_cost = df["Total_Cost"].sum()
    print(f"\n💰 Total Cloud Cost: ${total_cost}")

    print("\n📊 Cost Breakdown:")
    print(df.sort_values("Total_Cost", ascending=False))

def visualize_data(df):
    plt.figure()
    plt.bar(df["Service"], df["Total_Cost"])
    plt.xlabel("Cloud Services")
    plt.ylabel("Cost ($)")
    plt.title("Retail Cloud Cost Analysis")
    plt.show()

def export_results(df):
    df.to_excel("cloud_cost_result.xlsx", index=False)
    print("\n📁 Results saved to cloud_cost_result.xlsx")

def main():
    file_path = "cloud_usage_sample.xlsx"

    df = load_data(file_path)
    df = calculate_cost(df)
    analyze_data(df)
    visualize_data(df)
    export_results(df)

if __name__ == "__main__":
    main()
