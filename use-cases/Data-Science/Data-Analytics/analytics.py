import os
import pandas as pd

def load_data(file_path):
    script_dir = os.path.dirname(os.path.abspath(__file__)) 
    resolved_file_path = os.path.join(script_dir, file_path) 
    try:
        df = pd.read_csv(resolved_file_path)
        return df
    except FileNotFoundError:
        print(f"Error: The file {resolved_file_path} does not exist.")
        return None


def analyze_data(df):
    print("\n--- Data Insights ---")
    
    # Total records
    print("Total Vehicles: {}".format(len(df)))
    
    # Most common manufacturer
    most_common_manufacturer = df['manufacturer_name'].value_counts().idxmax()
    print("Most Common Manufacturer: {}".format(most_common_manufacturer))
    
    # Average purchase price
    avg_price = df['purchase_price'].mean()
    print("Average Purchase Price: ${:.2f}".format(avg_price))
    
    # Distribution of fuel types
    print("\nFuel Type Distribution:")
    fuel_type_counts = df['fuel_type'].value_counts()
    print("{}".format(fuel_type_counts))
    
    # Average horsepower by manufacturer
    print("\nAverage Horsepower by Manufacturer:")
    avg_horsepower_by_manufacturer = df.groupby('manufacturer_name')['horse_power'].mean()
    print("{}".format(avg_horsepower_by_manufacturer))
    
    # Top 5 most expensive vehicles
    print("\nTop 5 Most Expensive Vehicles:")
    top_expensive = df.nlargest(5, 'purchase_price')[['manufacturer_name', 'model_name', 'purchase_price']]
    print("{}".format(top_expensive))


if __name__ == "__main__":
    file_path = "../Data-Storage/processed/vehicles_cleaned.csv"
    df = load_data(file_path)
    if df is not None:
        analyze_data(df)
