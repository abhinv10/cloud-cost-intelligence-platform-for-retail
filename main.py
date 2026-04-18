import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("cloud_usage_sample.xlsx")

df["Compute_Cost"] = df["Usage_Hours"] * df["Price_per_Hour"]
df["Storage_Cost"] = df["Storage_GB"] * df["Price_per_GB"]
df["Request_Cost"] = df["Requests"] * df["Price_per_Request"]

df["Total_Cost"] = df["Compute_Cost"] + df["Storage_Cost"] + df["Request_Cost"]

total_cost = df["Total_Cost"].sum()

print("Total Retail Cloud Cost: $", total_cost)
# Average Cost
average_cost = df["Total_Cost"].mean()

print(f"Average Cost per Service: ${average_cost:.2f}")

df.sort_values("Total_Cost", ascending=False)
plt.bar(df["Service"], df["Total_Cost"])
plt.xlabel("Cloud Services")
plt.ylabel("Cost ($)")
plt.title("Retail Cloud Service Cost Analysis")
plt.show()

df.to_excel("cloud_cost_result.xlsx", index=False)
