import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import Ridge, Lasso
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load data
file_path = "../Data-Storage/processed/vehicles_cleaned.csv"
data = pd.read_csv(file_path)

data = pd.get_dummies(data, columns=['fuel_type', 'manufacturer_name', 'model_name'], drop_first=True)

# Features and Target
X = data[['horse_power', 'model_year'] + 
         [col for col in data.columns if 'fuel_type_' in col or 'manufacturer_name_' in col or 'model_name_' in col]]
y = data['purchase_price']

# Feature Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

# Hyperparameter Tuning using Ridge and Lasso Regression
# Define parameter grids
ridge_params = {'alpha': [0.1, 1, 10, 100]}  
lasso_params = {'alpha': [0.001, 0.01, 0.1, 1]}

# Ridge Regression with GridSearchCV
ridge = Ridge()
ridge_grid = GridSearchCV(ridge, ridge_params, cv=5, scoring='neg_mean_squared_error')
ridge_grid.fit(X_train, y_train)

# Lasso Regression with GridSearchCV
lasso = Lasso()
lasso_grid = GridSearchCV(lasso, lasso_params, cv=5, scoring='neg_mean_squared_error')
lasso_grid.fit(X_train, y_train)

# the best Ridge model
ridge_best = ridge_grid.best_estimator_
ridge_y_pred = ridge_best.predict(X_test)
print("Ridge Regression Performance:")
print(f"  Best Alpha: {ridge_grid.best_params_['alpha']}")
print(f"  MAE: {mean_absolute_error(y_test, ridge_y_pred):.2f}")
print(f"  MSE: {mean_squared_error(y_test, ridge_y_pred):.2f}")
print(f"  R-squared: {r2_score(y_test, ridge_y_pred):.2f}")

# the best Lasso model
lasso_best = lasso_grid.best_estimator_
lasso_y_pred = lasso_best.predict(X_test)
print("\nLasso Regression Performance:")
print(f"  Best Alpha: {lasso_grid.best_params_['alpha']}")
print(f"  MAE: {mean_absolute_error(y_test, lasso_y_pred):.2f}")
print(f"  MSE: {mean_squared_error(y_test, lasso_y_pred):.2f}")
print(f"  R-squared: {r2_score(y_test, lasso_y_pred):.2f}")

#Prediction
new_vehicle = {
    'horse_power': 180,
    'model_year': 2020,
    'fuel_type_Gasoline': 1,
    'manufacturer_name_Kia': 1,
    'manufacturer_name_Honda': 0,
    'model_name_Model_5': 1,
}

new_vehicle_df = pd.DataFrame([new_vehicle])
for col in X.columns:
    if col not in new_vehicle_df.columns:
        new_vehicle_df[col] = 0
new_vehicle_scaled = scaler.transform(new_vehicle_df[X.columns])

# Predict with the best Ridge model
predicted_price_ridge = ridge_best.predict(new_vehicle_scaled)[0]
print(f"\nPredicted Price (Ridge): ${predicted_price_ridge:,.2f}")

# Predict with the best Lasso model
predicted_price_lasso = lasso_best.predict(new_vehicle_scaled)[0]
print(f"Predicted Price (Lasso): ${predicted_price_lasso:,.2f}")
