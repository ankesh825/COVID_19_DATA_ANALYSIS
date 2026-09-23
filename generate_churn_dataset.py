"""
generate_churn_dataset.py
Generates a realistic, multi-feature customer churn dataset (N = 3,500)
for Machine Learning model development and comparative evaluation.
"""

import os
import numpy as np
import pandas as pd

def generate_churn_data(n_samples=3500, random_seed=42):
    np.random.seed(random_seed)
    
    # 1. Customer IDs
    customer_ids = [f"CUST_{i+1:04d}" for i in range(n_samples)]
    
    # 2. Demographics
    ages = np.clip(np.random.normal(loc=42, scale=13, size=n_samples).astype(int), 18, 80)
    genders = np.random.choice(['Male', 'Female'], size=n_samples, p=[0.50, 0.50])
    senior_citizen = (ages >= 65).astype(int)
    partner = np.random.choice(['Yes', 'No'], size=n_samples, p=[0.48, 0.52])
    dependents = np.where(partner == 'Yes', 
                          np.random.choice(['Yes', 'No'], size=n_samples, p=[0.45, 0.55]),
                          np.random.choice(['Yes', 'No'], size=n_samples, p=[0.12, 0.88]))
    
    # 3. Account Characteristics & Tenure
    # Beta distribution scaled to 1-72 months (bimodal: many new users and established users)
    tenure_raw = np.random.beta(a=0.8, b=0.9, size=n_samples) * 71 + 1
    tenure_months = np.round(tenure_raw).astype(int)
    
    contract_choices = ['Month-to-Month', 'One-Year', 'Two-Year']
    # Long tenure correlates with longer contracts
    contract_type = []
    for t in tenure_months:
        if t < 12:
            contract_type.append(np.random.choice(contract_choices, p=[0.82, 0.13, 0.05]))
        elif t < 36:
            contract_type.append(np.random.choice(contract_choices, p=[0.50, 0.35, 0.15]))
        else:
            contract_type.append(np.random.choice(contract_choices, p=[0.22, 0.38, 0.40]))
    contract_type = np.array(contract_type)
    
    paperless_billing = np.random.choice(['Yes', 'No'], size=n_samples, p=[0.62, 0.38])
    payment_methods = np.random.choice(
        ['Electronic Check', 'Mailed Check', 'Bank Transfer (automatic)', 'Credit Card (automatic)'],
        size=n_samples, p=[0.34, 0.18, 0.24, 0.24]
    )
    
    # 4. Service Subscriptions
    internet_service = np.random.choice(['Fiber Optic', 'DSL', 'No'], size=n_samples, p=[0.45, 0.38, 0.17])
    
    online_security = []
    tech_support = []
    for inet in internet_service:
        if inet == 'No':
            online_security.append('No internet service')
            tech_support.append('No internet service')
        else:
            online_security.append(np.random.choice(['Yes', 'No'], p=[0.38, 0.62]))
            tech_support.append(np.random.choice(['Yes', 'No'], p=[0.36, 0.64]))
    online_security = np.array(online_security)
    tech_support = np.array(tech_support)
    
    # 5. Customer Service Complaints / Calls
    cs_calls = np.random.poisson(lam=1.3, size=n_samples)
    cs_calls = np.clip(cs_calls, 0, 7)
    
    # 6. Monthly & Total Charges
    base_charge = 20.0
    inet_charge = np.where(internet_service == 'Fiber Optic', 50.0, np.where(internet_service == 'DSL', 25.0, 0.0))
    sec_charge = np.where(online_security == 'Yes', 12.0, 0.0)
    sup_charge = np.where(tech_support == 'Yes', 12.0, 0.0)
    noise = np.random.normal(0, 4.0, size=n_samples)
    monthly_charges = np.round(np.clip(base_charge + inet_charge + sec_charge + sup_charge + noise, 18.5, 125.0), 2)
    
    total_charges = np.round(np.clip(tenure_months * monthly_charges * np.random.uniform(0.95, 1.05, size=n_samples), 20.0, 9000.0), 2)
    
    # 7. Ground Truth Churn Logic (Logit-based generative process)
    # Log-odds calculation based on empirical telecom domain weights
    z = (
        - 1.40                                                         # Intercept
        + 1.35 * (contract_type == 'Month-to-Month')                  # Massive churn driver
        - 0.85 * (contract_type == 'Two-Year')                        # Strong retention anchor
        - 0.045 * tenure_months                                       # Experience buffer
        + 0.018 * (monthly_charges - 60.0)                            # Price sensitivity
        + 0.65 * (payment_methods == 'Electronic Check')              # Higher payment friction
        + 0.55 * (internet_service == 'Fiber Optic')                  # High cost dissatisfaction
        - 0.45 * (online_security == 'Yes')                           # Stickiness factor
        - 0.50 * (tech_support == 'Yes')                              # Relationship building
        + 0.48 * (cs_calls >= 3)                                      # Escalated frustration
        + 0.28 * senior_citizen                                       # Higher churn demographic
        - 0.30 * (dependents == 'Yes')                                # Family inertia
    )
    
    churn_prob = 1.0 / (1.0 + np.exp(-z))
    churn = (np.random.rand(n_samples) < churn_prob).astype(int)
    
    # Assemble into DataFrame
    df = pd.DataFrame({
        'customer_id': customer_ids,
        'gender': genders,
        'senior_citizen': senior_citizen,
        'partner': partner,
        'dependents': dependents,
        'tenure_months': tenure_months,
        'contract_type': contract_type,
        'paperless_billing': paperless_billing,
        'payment_method': payment_methods,
        'internet_service': internet_service,
        'online_security': online_security,
        'tech_support': tech_support,
        'customer_service_calls': cs_calls,
        'monthly_charges': monthly_charges,
        'total_charges': total_charges,
        'churn': churn
    })
    
    return df

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, ".."))
    data_dir = os.path.join(project_root, "data")
    os.makedirs(data_dir, exist_ok=True)
    
    df = generate_churn_data(n_samples=3500, random_seed=42)
    output_csv = os.path.join(data_dir, "customer_churn_data.csv")
    df.to_csv(output_csv, index=False)
    
    print(f"Customer churn dataset generated successfully at: {output_csv}")
    print(f"Dataset Dimensions: {df.shape}")
    print("\nClass Distribution (Target: Churn):")
    print(df['churn'].value_counts(normalize=True).mul(100).round(2).astype(str) + '%')
    print("\nSample Preview:")
    print(df.head(4).to_string())
