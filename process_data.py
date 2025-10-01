import pandas as pd
import os

# Step 1: Set data folder path
data_folder = "data"

# Step 2: List all CSV files in the folder
csv_files = [os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.endswith(".csv")]

# Step 3: Read and process each file
all_data = []

for file in csv_files:
    df = pd.read_csv(file)

    # Filter: Keep only "Pink Morsels"
    df = df[df["product"] == "Pink Morsel"]

    # Create "sales" field
    df["sales"] = df["quantity"] * df["price"]

    # Keep only relevant columns
    df = df[["sales", "date", "region"]]

    # Append processed data
    all_data.append(df)

# Step 4: Combine all data into one DataFrame
final_df = pd.concat(all_data, ignore_index=True)

# Step 5: Save to new CSV
final_df.to_csv("formatted_sales_data.csv", index=False)

print("Processing complete. Output saved as formatted_sales_data.csv")
