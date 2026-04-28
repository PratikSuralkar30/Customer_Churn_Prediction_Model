import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

warnings.filterwarnings('ignore')

# 1. Setup Directories
os.makedirs('../images', exist_ok=True)

print("--- Phase 1: Loading Ames Dataset ---")
try:
    df = pd.read_csv('../data/train.csv')
    print(f"Dataset successfully loaded! Shape: {df.shape}")
except FileNotFoundError:
    print("ERROR: Please download 'train.csv' from Kaggle and place it in the 'data/' folder.")
    exit()

# Drop 'Id' as it has no predictive power
df.drop('Id', axis=1, inplace=True)

print("\n--- Phase 2: Exploratory Data Analysis (EDA) ---")
# Get correlation of top 10 numerical features against SalePrice
numeric_df = df.select_dtypes(include=[np.number])
top_corr_features = numeric_df.corr()['SalePrice'].sort_values(ascending=False).head(10).index

plt.figure(figsize=(10, 8))
sns.heatmap(df[top_corr_features].corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Top 10 Feature Correlation Heatmap")
plt.tight_layout()
plt.savefig('../images/correlation_heatmap.png')
print("Saved correlation heatmap to /images.")

print("\n--- Phase 3: Data Preprocessing & Feature Engineering ---")
# Separate Target and Features
X = df.drop('SalePrice', axis=1)
y = df['SalePrice']

# Identify numerical and categorical columns
num_cols = X.select_dtypes(include=['int64', 'float64']).columns
cat_cols = X.select_dtypes(include=['object']).columns

# Create preprocessing pipelines
num_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')), 
    ('scaler', StandardScaler())                   
])

cat_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')), 
    ('onehot', OneHotEncoder(handle_unknown='ignore'))    
])

# Combine preprocessing steps
preprocessor = ColumnTransformer(
    transformers=[
        ('num', num_transformer, num_cols),
        ('cat', cat_transformer, cat_cols)
    ])

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("\n--- Phase 4: Model Training & Evaluation ---")
# Build Pipelines
lr_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                              ('model', LinearRegression())])

rf_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                              ('model', RandomForestRegressor(n_estimators=100, random_state=42))])

# Train Models
print("Training Linear Regression...")
lr_pipeline.fit(X_train, y_train)
lr_pred = lr_pipeline.predict(X_test)

print("Training Random Forest...")
rf_pipeline.fit(X_train, y_train)
rf_pred = rf_pipeline.predict(X_test)

def evaluate_model(name, y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    print(f"\n{name} Performance:")
    print(f"MAE:  ${mae:,.2f}")
    print(f"RMSE: ${rmse:,.2f}")
    print(f"R²:   {r2:.4f}")

evaluate_model("Linear Regression", y_test, lr_pred)
evaluate_model("Random Forest", y_test, rf_pred)

print("\n--- Phase 5: Visualization of Results ---")
plt.figure(figsize=(8, 6))
plt.scatter(y_test, rf_pred, alpha=0.4, color='green')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel("Actual Sale Price ($)")
plt.ylabel("Predicted Sale Price ($)")
plt.title("Random Forest: Actual vs Predicted Prices")
plt.tight_layout()
plt.savefig('../images/actual_vs_predicted.png')
print("Saved scatter plot to /images.")

print("\n--- Phase 6: Simulating a Real-World Prediction ---")
# Take a random unseen property from the test set
sample_house = X_test.iloc[[5]]
actual_price = y_test.iloc[5]

# Predict its price using the full pipeline
predicted_price = rf_pipeline.predict(sample_house)[0]

print("Model Predicted Value: ${:,.2f}".format(predicted_price))
print("Actual Market Value:   ${:,.2f}".format(actual_price))
print("Difference:            ${:,.2f}".format(abs(predicted_price - actual_price)))
