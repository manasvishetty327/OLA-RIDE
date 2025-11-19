# ---------------------------------------------------------------- #
#                  PHASE 1: DATA CLEANING SCRIPT                   #
# ---------------------------------------------------------------- #

import pandas as pd

# --- Step 1: Load the datasets ---
# Assumes the CSV files are in the same folder as this script.
try:
    df_sheet1 = pd.read_csv('OLA_DataSet.csv')
    df_sheet2 = pd.read_csv('OLA_DataSet2.csv') # This might be metadata, we will inspect
    df_july = pd.read_csv('OLA_DataSet3icons.csv')
    print("All three files loaded successfully!")
except FileNotFoundError:
    print("Error: Make sure all three CSV files are in the same folder as the script.")
    exit()

# --- Step 2: Inspect the DataFrames --

print("\n--- Inspecting the data ---")
print("Columns in Sheet1:", df_sheet1.columns.tolist())
print("Columns in July:", df_july.columns.tolist())
print("Columns in Sheet2:", df_sheet2.columns.tolist())

# Let's assume Sheet2 is not part of the main dataset for now and combine the ride data.
# If the columns are the same, we can concatenate them.
if df_sheet1.columns.equals(df_july.columns):
    df = pd.concat([df_sheet1, df_july], ignore_index=True)
    print("\n'Sheet1' and 'July' data have been combined into a single DataFrame.")
else:
    print("\nColumn mismatch between Sheet1 and July. Using only Sheet1 for now.")
    df = df_sheet1

print(f"Total rides in combined dataset: {len(df)}")

# --- Step 3: Clean and Preprocess the Data ---
print("\n--- Starting Data Cleaning ---")

# 1. Get initial info and check for missing values
print("\nInitial Info:")
df.info()

print("\nInitial Missing Values:")
print(df.isnull().sum())

# 2. Handle Missing Values
# Example: Fill missing 'driver_rating' with the median
if 'driver_rating' in df.columns:
    median_rating = df['driver_rating'].median()
    df['driver_rating'].fillna(median_rating, inplace=True)
    print(f"\nMissing 'driver_rating' filled with median value: {median_rating}")

# Example: Fill missing 'cancellation_reason' with 'Not Available'
if 'cancellation_reason' in df.columns:
    df['cancellation_reason'].fillna('Not Available', inplace=True)
    print("Missing 'cancellation_reason' filled with 'Not Available'.")

# 3. Correct Data Types
# Example: Convert a date column from 'object' to 'datetime'
if 'booking_time' in df.columns:
    df['booking_time'] = pd.to_datetime(df['booking_time'], errors='coerce')
    print("'booking_time' column converted to datetime.")

# 4. Remove Duplicate Rows
initial_rows = len(df)
df.drop_duplicates(inplace=True)
print(f"Removed {initial_rows - len(df)} duplicate rows.")

# --- Step 4: Final Verification and Saving ---
print("\n--- Cleaning Complete ---")
print("Final Missing Values Check:")
print(df.isnull().sum())

print("\nFinal DataFrame Info:")
df.info()

# Save the final cleaned data to a new CSV file
df.to_csv('ola_data_cleaned.csv', index=False)
print("\nSuccessfully saved the cleaned data to 'ola_data_cleaned.csv'")
print("You can now proceed with Phase 2 (SQL) using this new file.")
