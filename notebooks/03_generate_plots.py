import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, roc_curve, auc
import os
import shap

# Ensure images directory exists
os.makedirs("images", exist_ok=True)

# 1. Load Data and Model
df = pd.read_csv("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})

X = df.drop(columns=['customerID', 'Churn'])
y = df['Churn']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
model = joblib.load("models/churn_model_pipeline.pkl")

preds = model.predict(X_test)
probs = model.predict_proba(X_test)[:, 1]

# 2. Confusion Matrix Plot
cm = confusion_matrix(y_test, preds)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['Predicted Stay', 'Predicted Churn'],
            yticklabels=['Actual Stay', 'Actual Churn'],
            annot_kws={"size": 16})
plt.title('Confusion Matrix - XGBoost Churn Model', fontsize=16)
plt.tight_layout()
plt.savefig("images/confusion_matrix.png", dpi=300)
plt.close()

# 3. ROC Curve Plot
fpr, tpr, _ = roc_curve(y_test, probs)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate', fontsize=12)
plt.ylabel('True Positive Rate', fontsize=12)
plt.title('Receiver Operating Characteristic (ROC)', fontsize=16)
plt.legend(loc="lower right", fontsize=12)
plt.tight_layout()
plt.savefig("images/roc_curve.png", dpi=300)
plt.close()

# 4. Feature Importance Plot (Using XGBoost native importance)
classifier = model.named_steps['classifier']
preprocessor = model.named_steps['preprocessor']

# Get feature names
num_cols = preprocessor.transformers_[0][2]
cat_cols = preprocessor.transformers_[1][1].named_steps['encoder'].get_feature_names_out(preprocessor.transformers_[1][2])
feature_names = list(num_cols) + list(cat_cols)

importances = classifier.feature_importances_
indices = np.argsort(importances)[-10:] # Top 10

plt.figure(figsize=(10, 8))
plt.title('Top 10 Feature Importances', fontsize=16)
plt.barh(range(len(indices)), importances[indices], color='b', align='center')
plt.yticks(range(len(indices)), [feature_names[i] for i in indices])
plt.xlabel('Relative Importance', fontsize=12)
plt.tight_layout()
plt.savefig("images/feature_importance.png", dpi=300)
plt.close()

print("Successfully generated and saved images to the 'images/' folder.")
