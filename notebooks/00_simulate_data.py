import pandas as pd
import numpy as np
import os

def simulate_data(input_path, output_path):
    print("Loading base data...")
    df = pd.read_csv(input_path)
    
    np.random.seed(42)
    n = len(df)
    
    print("Simulating advanced features...")
    # Simulate support tickets (more tickets if churned, generally)
    # Churn column is 'Churn' with values 'Yes' and 'No'
    is_churn = df['Churn'] == 'Yes'
    
    df['support_tickets'] = np.where(
        is_churn,
        np.random.poisson(lam=3, size=n),
        np.random.poisson(lam=0.5, size=n)
    )
    
    df['sla_breaches'] = np.where(
        is_churn,
        np.random.poisson(lam=1.5, size=n),
        np.random.poisson(lam=0.1, size=n)
    )
    
    # Active days in the last 30 days
    df['active_days'] = np.where(
        is_churn,
        np.random.randint(1, 15, size=n),
        np.random.randint(15, 31, size=n)
    )
    
    # Monthly usage hours
    df['monthly_usage_hours'] = np.where(
        is_churn,
        np.random.normal(loc=50, scale=20, size=n).clip(min=0),
        np.random.normal(loc=120, scale=30, size=n).clip(min=0)
    )
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Saved simulated data to {output_path}")

if __name__ == "__main__":
    simulate_data(
        "data/WA_Fn-UseC_-Telco-Customer-Churn.csv",
        "data/simulated_churn_data.csv"
    )
