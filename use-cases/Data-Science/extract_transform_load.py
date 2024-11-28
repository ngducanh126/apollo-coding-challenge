import requests
import pandas as pd
import os

def extract_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        print(f"Successfully fetched {len(data)} records.")
        return data
    else:
        print(f"Failed to fetch data from API. Status code: {response.status_code}")
        return []

def transform_data(raw_data):
    df = pd.DataFrame(raw_data)

    # Handle missing values
    df.dropna(subset=["manufacturer_name", "fuel_type"], inplace=True)  # Drop rows with with important missing values
    df["description"] = df["description"].fillna("No description available")  # fill missing description
    
    # Remove duplicates
    df.drop_duplicates(subset=["vin"], inplace=True)

    # Normalize columns
    df["manufacturer_name"] = df["manufacturer_name"].str.strip().str.title()
    df["model_name"] = df["model_name"].str.strip().str.title()

    # Ensure numeric values are valid
    df["horse_power"] = pd.to_numeric(df["horse_power"], errors="coerce")
    df["purchase_price"] = pd.to_numeric(df["purchase_price"], errors="coerce")

    print(f"Data cleaned. Remaining records: {len(df)}")
    return df

def load_data(df, output_file):
    print(f"Saving cleaned data to {output_file}...")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, index=False)
    print("Data successfully saved!")

if __name__ == "__main__":
    # Extract
    API_URL = "http://127.0.0.1:5000/vehicle"
    OUTPUT_FILE = "Data-Storage/processed/vehicles_cleaned.csv"
    raw_data = extract_data(API_URL)
    if raw_data: 
        cleaned_data = transform_data(raw_data)
        load_data(cleaned_data, OUTPUT_FILE)
