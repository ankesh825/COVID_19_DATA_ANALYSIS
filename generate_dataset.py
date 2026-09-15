"""
generate_dataset.py
Generates a realistic, reproducible e-commerce A/B testing and user behavior dataset
for inferential statistics and hypothesis testing.
"""

import os
import numpy as np
import pandas as pd

def generate_ecommerce_data(n_samples=3000, random_seed=42):
    np.random.seed(random_seed)
    
    # 1. User IDs
    user_ids = [f"USR_{i+1:04d}" for i in range(n_samples)]
    
    # 2. Experiment Group (50/50 split between Control and Treatment)
    groups = np.random.choice(['Control', 'Treatment'], size=n_samples, p=[0.5, 0.5])
    
    # 3. Device Category: Mobile (55%), Desktop (35%), Tablet (10%)
    devices = np.random.choice(['Mobile', 'Desktop', 'Tablet'], size=n_samples, p=[0.55, 0.35, 0.10])
    
    # 4. Marketing Channel: Organic Search (30%), Paid Search (25%), Social Media (25%), Email Campaign (20%)
    channels = np.random.choice(['Organic Search', 'Paid Search', 'Social Media', 'Email Campaign'], 
                                size=n_samples, p=[0.30, 0.25, 0.25, 0.20])
    
    # 5. Session Duration (Minutes) across Marketing Channels
    channel_means = {
        'Organic Search': (4.5, 1.2),  # shape, scale -> mean ~5.4 mins
        'Paid Search': (3.8, 1.0),     # mean ~3.8 mins
        'Social Media': (3.2, 0.9),    # mean ~2.88 mins
        'Email Campaign': (5.2, 1.3)   # mean ~6.76 mins
    }
    
    session_durations = []
    for ch in channels:
        shape, scale = channel_means[ch]
        duration = np.random.gamma(shape, scale)
        session_durations.append(round(max(0.5, duration), 2))
    session_durations = np.array(session_durations)
    
    # 6. Pages Visited correlated with session duration
    pages_visited = np.maximum(1, np.random.poisson(session_durations * 1.5))
    
    # 7. Conversion Status (Dependent on Device and Group)
    base_conv_prob = {
        'Desktop': 0.18,
        'Mobile': 0.11,
        'Tablet': 0.13
    }
    
    converted = []
    for grp, dev in zip(groups, devices):
        prob = base_conv_prob[dev]
        if grp == 'Treatment':
            prob += 0.045  # 4.5% uplift in treatment
        conv = 1 if np.random.rand() < prob else 0
        converted.append(conv)
    converted = np.array(converted)
    
    # 8. Average Order Value (AOV in USD) for Converted Users
    order_values = []
    for grp, is_conv in zip(groups, converted):
        if is_conv == 1:
            if grp == 'Control':
                val = np.random.normal(loc=85.2, scale=20.5)
            else:
                val = np.random.normal(loc=94.6, scale=22.8)
            order_values.append(round(max(15.0, val), 2))
        else:
            order_values.append(np.nan)
    
    # 9. Pre and Post Loyalty / Customer Satisfaction Scores (Scale 1-10)
    is_repeat = np.random.choice([True, False], size=n_samples, p=[0.35, 0.65])
    pre_loyalty = []
    post_loyalty = []
    
    for rep, grp in zip(is_repeat, groups):
        if rep:
            pre = int(np.clip(np.random.normal(loc=6.2, scale=1.4), 1, 10))
            if grp == 'Treatment':
                shift = np.random.normal(loc=1.4, scale=0.85)
            else:
                shift = np.random.normal(loc=0.1, scale=0.75)
            post = int(np.clip(round(pre + shift), 1, 10))
            pre_loyalty.append(pre)
            post_loyalty.append(post)
        else:
            pre_loyalty.append(np.nan)
            post_loyalty.append(np.nan)
            
    # 10. Assemble DataFrame
    df = pd.DataFrame({
        'user_id': user_ids,
        'group': groups,
        'device_category': devices,
        'marketing_channel': channels,
        'session_duration_mins': session_durations,
        'pages_visited': pages_visited,
        'converted': converted,
        'order_value_usd': order_values,
        'pre_loyalty_score': pre_loyalty,
        'post_loyalty_score': post_loyalty
    })
    
    return df

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, ".."))
    data_dir = os.path.join(project_root, "data")
    os.makedirs(data_dir, exist_ok=True)
    
    df = generate_ecommerce_data(n_samples=3000, random_seed=42)
    output_path = os.path.join(data_dir, "ecommerce_ab_test_data.csv")
    df.to_csv(output_path, index=False)
    
    print(f"Dataset successfully created at: {output_path}")
    print(f"Shape: {df.shape}")
    print("\nGroup Counts:\n", df['group'].value_counts())
    print("\nConversion Crosstab:\n", pd.crosstab(df['group'], df['converted'], margins=True))
