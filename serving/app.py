import sys
import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import numpy as np
import shap

app = FastAPI(title="Customer Churn Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model pipeline at startup
MODEL_PATH = "models/churn_model_pipeline.pkl"
try:
    pipeline = joblib.load(MODEL_PATH)
except Exception as e:
    print(f"Failed to load model: {e}")
    pipeline = None

class CustomerData(BaseModel):
    gender: str = "Female"
    SeniorCitizen: int = 0
    Partner: str = "Yes"
    Dependents: str = "No"
    tenure: int = Field(default=12, ge=0)
    PhoneService: str = "Yes"
    MultipleLines: str = "No"
    InternetService: str = "Fiber optic"
    OnlineSecurity: str = "No"
    OnlineBackup: str = "Yes"
    DeviceProtection: str = "No"
    TechSupport: str = "No"
    StreamingTV: str = "Yes"
    StreamingMovies: str = "Yes"
    Contract: str = "Month-to-month"
    PaperlessBilling: str = "Yes"
    PaymentMethod: str = "Electronic check"
    MonthlyCharges: float = 85.5
    TotalCharges: float = 1000.0

@app.post("/score")
def score_customer(customer: CustomerData):
    if not pipeline:
        raise HTTPException(status_code=500, detail="Model pipeline not loaded.")
    
    # Convert input to DataFrame
    df = pd.DataFrame([customer.model_dump()])
    
    # Predict
    try:
        prediction = pipeline.predict(df)[0]
        probability = pipeline.predict_proba(df)[0, 1]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {e}")
        
    return {
        "churn_prediction": int(prediction),
        "churn_probability": float(probability),
        "risk_level": "High" if probability > 0.6 else "Medium" if probability > 0.3 else "Low"
    }

@app.post("/explain")
def explain_customer(customer: CustomerData):
    if not pipeline:
        raise HTTPException(status_code=500, detail="Model pipeline not loaded.")
        
    df = pd.DataFrame([customer.model_dump()])
    
    try:
        # We need to extract the preprocessor to transform the data, and the classifier for SHAP
        preprocessor = pipeline.named_steps['preprocessor']
        classifier = pipeline.named_steps['classifier']
        
        X_transformed = preprocessor.transform(df)
        
        # Calculate expected value and shap values 
        # For tree explainer, we can just pass the classifier
        explainer = shap.TreeExplainer(classifier)
        shap_values = explainer.shap_values(X_transformed)
        
        # Get feature names after transformation
        feature_names = []
        if hasattr(preprocessor, 'get_feature_names_out'):
            feature_names = preprocessor.get_feature_names_out()
        else:
            feature_names = [f"Feature {i}" for i in range(X_transformed.shape[1])]
            
        # Map values to feature names
        importance = []
        for i, val in enumerate(shap_values[0]):
            importance.append({
                "feature": feature_names[i] if i < len(feature_names) else f"Feature {i}",
                "impact": float(val)
            })
            
        # Sort by absolute impact
        importance.sort(key=lambda x: abs(x["impact"]), reverse=True)
        
        return {
            "top_drivers": importance[:5]
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Explanation error: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
