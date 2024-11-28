import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


def fetch_data():
    data_path = "../Data-Storage/processed/vehicles_cleaned.csv"
    
    try:
        df = pd.read_csv(data_path)
        return df
    except FileNotFoundError:
        print(f"Erorr file does not exist")
        return None
    except Exception as e:
        print(f"unexpected error occurred: {e}")
        return None

# Step 2: Preprocess Data
def preprocess_data(data):
    print("Preprocessing data...")
    # Validate required columns
    required_columns = ['horse_power', 'model_year', 'purchase_price', 'fuel_type', 'manufacturer_name']
    for col in required_columns:
        if col not in data.columns:
            raise ValueError("Missing required column {}.format(col)")

    # encode categorical column
    df = pd.get_dummies(data, columns=['fuel_type', 'manufacturer_name'], drop_first=True)

    # Features and target
    features = ['horse_power', 'model_year']
    for col in df.columns:
        if col.startswith('fuel_type_') or col.startswith('manufacturer_name_'):
            features.append(col)

    X = df[features]
    y = df['purchase_price']

    # split data
    return train_test_split(X, y, test_size=0.2, random_state=42), X.columns

# train Linear Regression Model
def train_model(X_train, y_train):
    print("Training Linear Regression model...")
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

# get insights
def extract_insights(model, feature_names):
    print("Extracting insights...")
    try:
        coef = model.coef_

        # pair feature names with coefficients
        insights = []
        for feature, coef_value in zip(feature_names, coef):
            insights.append((feature, abs(coef_value)))

        # sort the insights descendingly
        insights.sort(key=lambda x: x[1], reverse=True)

        # Format
        sorted_insights = [(feature, coef_value) for feature, coef_value in insights]

        print("Key Factors Affecting Purchase Price:")
        for feature, importance in insights:
            print("- {}: {:.2f} impact on price".format(feature, importance))
    except:
        print('error getting insights')

if __name__ == "__main__":
    data = fetch_data()
    if data is not None:
        try:
            (X_train, X_test, y_train, y_test), feature_names = preprocess_data(data)
            model = train_model(X_train, y_train)
            extract_insights(model, feature_names)
        except Exception as e:
            print(f"An error occurred during processing: {e}")
