"""
train_and_evaluate_models.py
Executes the complete Machine Learning pipeline:
- Data ingestion and EDA
- Scikit-Learn Pipeline and ColumnTransformer
- Training Logistic Regression, Decision Tree, and Random Forest
- 5-Fold Stratified Cross-Validation
- Multi-metric test evaluation (Accuracy, Precision, Recall, F1, ROC-AUC, PR-AUC, MCC)
- Generates 6 publication-grade figures (300 DPI)
- Exports metrics to JSON
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate, learning_curve
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, balanced_accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, average_precision_score, matthews_corrcoef,
    brier_score_loss, confusion_matrix, roc_curve, precision_recall_curve
)

# Plot styling
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

def run_ml_pipeline(data_path, vis_dir, output_json_path):
    os.makedirs(vis_dir, exist_ok=True)
    df = pd.read_csv(data_path)
    
    # -------------------------------------------------------------
    # 1. Exploratory Data Analysis & Summary Statistics
    # -------------------------------------------------------------
    n_total = len(df)
    churn_counts = df['churn'].value_counts()
    churn_rate = float(df['churn'].mean())
    
    eda_stats = {
        'total_samples': n_total,
        'retained_count': int(churn_counts.get(0, 0)),
        'churned_count': int(churn_counts.get(1, 0)),
        'churn_rate_pct': float(churn_rate * 100),
        'tenure_summary': {
            'mean': float(df['tenure_months'].mean()),
            'median': float(df['tenure_months'].median()),
            'std': float(df['tenure_months'].std())
        },
        'monthly_charges_summary': {
            'mean': float(df['monthly_charges'].mean()),
            'median': float(df['monthly_charges'].median()),
            'std': float(df['monthly_charges'].std())
        },
        'total_charges_summary': {
            'mean': float(df['total_charges'].mean()),
            'median': float(df['total_charges'].median()),
            'std': float(df['total_charges'].std())
        },
        'contract_churn_rates': df.groupby('contract_type')['churn'].mean().mul(100).round(2).to_dict(),
        'internet_churn_rates': df.groupby('internet_service')['churn'].mean().mul(100).round(2).to_dict()
    }
    
    # Figure 1: Exploratory Data Analysis & Correlations
    fig, axes = plt.subplots(2, 2, figsize=(14, 11))
    
    # Target distribution
    sns.countplot(data=df, x='churn', ax=axes[0, 0], palette=['#4A90E2', '#E74C3C'], hue='churn', legend=False)
    axes[0, 0].set_title(f"Target Class Distribution (Churn Rate: {churn_rate*100:.1f}%)", fontsize=12, fontweight='bold')
    axes[0, 0].set_xticklabels(['Retained (Class 0)', 'Churned (Class 1)'])
    axes[0, 0].set_ylabel("Customer Count")
    for p in axes[0, 0].patches:
        h = p.get_height()
        axes[0, 0].annotate(f"{int(h):,} ({h/n_total*100:.1f}%)", (p.get_x() + p.get_width()/2., h/2),
                            ha='center', va='center', color='white', fontweight='bold', fontsize=11)
        
    # Churn rate by contract type
    contract_df = df.groupby('contract_type')['churn'].agg(['count', 'mean']).reset_index()
    contract_df['churn_pct'] = contract_df['mean'] * 100
    sns.barplot(data=contract_df, x='contract_type', y='churn_pct', ax=axes[0, 1], palette='Reds_r', hue='contract_type', legend=False)
    axes[0, 1].set_title("Empirical Churn Rate (%) by Contract Type", fontsize=12, fontweight='bold')
    axes[0, 1].set_ylabel("Churn Rate (%)")
    axes[0, 1].set_xlabel("Contract Agreement")
    for p in axes[0, 1].patches:
        axes[0, 1].annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width()/2., p.get_height()/2),
                            ha='center', va='center', color='white', fontweight='bold', fontsize=11)
        
    # Tenure vs Monthly Charges distribution by Churn
    sns.scatterplot(data=df.sample(min(800, len(df)), random_state=42), 
                    x='tenure_months', y='monthly_charges', hue='churn', 
                    palette=['#2B5C8F', '#E74C3C'], alpha=0.6, ax=axes[1, 0])
    axes[1, 0].set_title("Tenure vs Monthly Charges (Sample N=800)", fontsize=12, fontweight='bold')
    axes[1, 0].set_xlabel("Tenure (Months)")
    axes[1, 0].set_ylabel("Monthly Charges ($)")
    axes[1, 0].legend(title="Churn", labels=['Retained', 'Churned'])
    
    # Correlation Heatmap for Numerical Features
    num_cols = ['tenure_months', 'monthly_charges', 'total_charges', 'customer_service_calls', 'senior_citizen', 'churn']
    corr_matrix = df[num_cols].corr()
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="vlag", center=0, ax=axes[1, 1], linewidths=1)
    axes[1, 1].set_title("Numerical Feature Correlation Matrix", fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    fig1_path = os.path.join(vis_dir, "fig1_eda_and_correlations.png")
    plt.savefig(fig1_path, dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # 2. Data Preprocessing & Column Transformation
    # -------------------------------------------------------------
    feature_cols = [
        'gender', 'senior_citizen', 'partner', 'dependents', 'tenure_months',
        'contract_type', 'paperless_billing', 'payment_method', 'internet_service',
        'online_security', 'tech_support', 'customer_service_calls',
        'monthly_charges', 'total_charges'
    ]
    X = df[feature_cols].copy()
    y = df['churn'].copy()
    
    # Identify column types
    numeric_features = ['tenure_months', 'monthly_charges', 'total_charges', 'customer_service_calls']
    categorical_features = [
        'gender', 'partner', 'dependents', 'contract_type', 'paperless_billing',
        'payment_method', 'internet_service', 'online_security', 'tech_support'
    ]
    passthrough_features = ['senior_citizen']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'), categorical_features),
            ('pass', 'passthrough', passthrough_features)
        ]
    )
    
    # Stratified Train-Test Split (80% Train, 20% Test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, stratify=y, random_state=42
    )
    
    split_info = {
        'train_total': len(X_train),
        'train_churn': int(y_train.sum()),
        'train_churn_pct': float(y_train.mean() * 100),
        'test_total': len(X_test),
        'test_churn': int(y_test.sum()),
        'test_churn_pct': float(y_test.mean() * 100)
    }

    # -------------------------------------------------------------
    # 3. Model Definition & 5-Fold Cross-Validation
    # -------------------------------------------------------------
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, C=1.0, solver='lbfgs', random_state=42),
        'Decision Tree (Pruned)': DecisionTreeClassifier(max_depth=5, min_samples_split=20, min_samples_leaf=10, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=150, max_depth=8, min_samples_leaf=5, random_state=42)
    }
    
    # Cross-validation setup
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scoring = {
        'accuracy': 'accuracy',
        'balanced_accuracy': 'balanced_accuracy',
        'precision': 'precision',
        'recall': 'recall',
        'f1': 'f1',
        'roc_auc': 'roc_auc'
    }
    
    cv_results = {}
    fitted_pipelines = {}
    test_metrics = {}
    y_preds = {}
    y_probs = {}
    
    for name, clf in models.items():
        pipe = Pipeline([
            ('preprocessor', preprocessor),
            ('classifier', clf)
        ])
        
        # Cross-validation on train set
        scores = cross_validate(pipe, X_train, y_train, cv=skf, scoring=scoring, return_train_score=False)
        cv_summary = {metric: {'mean': float(np.mean(scores[f'test_{metric}'])), 
                               'std': float(np.std(scores[f'test_{metric}']))} 
                      for metric in scoring}
        cv_results[name] = cv_summary
        
        # Fit on entire training set
        pipe.fit(X_train, y_train)
        fitted_pipelines[name] = pipe
        
        # Predict on holdout test set
        pred = pipe.predict(X_test)
        prob = pipe.predict_proba(X_test)[:, 1]
        y_preds[name] = pred
        y_probs[name] = prob
        
        cm = confusion_matrix(y_test, pred)
        tn, fp, fn, tp = cm.ravel()
        
        test_metrics[name] = {
            'accuracy': float(accuracy_score(y_test, pred)),
            'balanced_accuracy': float(balanced_accuracy_score(y_test, pred)),
            'precision': float(precision_score(y_test, pred, zero_division=0)),
            'recall': float(recall_score(y_test, pred)),
            'specificity': float(tn / (tn + fp)),
            'f1_score': float(f1_score(y_test, pred)),
            'roc_auc': float(roc_auc_score(y_test, prob)),
            'average_precision_pr_auc': float(average_precision_score(y_test, prob)),
            'mcc': float(matthews_corrcoef(y_test, pred)),
            'brier_score': float(brier_score_loss(y_test, prob)),
            'confusion_matrix': {
                'tn': int(tn), 'fp': int(fp),
                'fn': int(fn), 'tp': int(tp)
            }
        }

    # -------------------------------------------------------------
    # 4. Visualizations
    # -------------------------------------------------------------
    
    # Figure 2: Confusion Matrices
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    cm_palettes = ['Blues', 'Oranges', 'Greens']
    
    for idx, (name, metrics) in enumerate(test_metrics.items()):
        cm = np.array([[metrics['confusion_matrix']['tn'], metrics['confusion_matrix']['fp']],
                       [metrics['confusion_matrix']['fn'], metrics['confusion_matrix']['tp']]])
        cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        
        labels = np.asarray([
            f"{val:,}\n({pct:.1%})" for val, pct in zip(cm.flatten(), cm_norm.flatten())
        ]).reshape(2, 2)
        
        sns.heatmap(cm_norm, annot=labels, fmt="", cmap=cm_palettes[idx], ax=axes[idx], cbar=False,
                    xticklabels=['Pred Retained', 'Pred Churned'],
                    yticklabels=['True Retained', 'True Churned'],
                    linewidths=1.5, annot_kws={"size": 11, "weight": "bold"})
        
        axes[idx].set_title(f"{name}\nAccuracy: {metrics['accuracy']:.3f} | F1: {metrics['f1_score']:.3f}", 
                            fontsize=12, fontweight='bold', pad=10)
        axes[idx].set_ylabel("Actual Class" if idx == 0 else "")
        
    plt.tight_layout()
    fig2_path = os.path.join(vis_dir, "fig2_confusion_matrices.png")
    plt.savefig(fig2_path, dpi=300)
    plt.close()

    # Figure 3: ROC and Precision-Recall Curves
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    colors = {'Logistic Regression': '#1F77B4', 'Decision Tree (Pruned)': '#FF7F0E', 'Random Forest': '#2CA02C'}
    
    # ROC Curve
    for name in models:
        fpr, tpr, _ = roc_curve(y_test, y_probs[name])
        auc_val = test_metrics[name]['roc_auc']
        ax1.plot(fpr, tpr, color=colors[name], lw=2.2, label=f"{name} (AUC = {auc_val:.3f})")
    ax1.plot([0, 1], [0, 1], color='gray', linestyle='--', lw=1.2, label='Chance Baseline (AUC = 0.50)')
    ax1.set_title("Receiver Operating Characteristic (ROC) Curves", fontsize=12, fontweight='bold')
    ax1.set_xlabel("False Positive Rate (1 - Specificity)", fontsize=11)
    ax1.set_ylabel("True Positive Rate (Recall / Sensitivity)", fontsize=11)
    ax1.set_xlim([-0.02, 1.02])
    ax1.set_ylim([-0.02, 1.02])
    ax1.legend(loc='lower right', frameon=True)
    
    # Precision-Recall Curve
    no_skill_baseline = float(y_test.mean())
    for name in models:
        prec, rec, _ = precision_recall_curve(y_test, y_probs[name])
        ap_val = test_metrics[name]['average_precision_pr_auc']
        ax2.plot(rec, prec, color=colors[name], lw=2.2, label=f"{name} (PR-AUC / AP = {ap_val:.3f})")
    ax2.plot([0, 1], [no_skill_baseline, no_skill_baseline], color='gray', linestyle='--', lw=1.2,
             label=f'Baseline Proportion ({no_skill_baseline:.1%})')
    ax2.set_title("Precision-Recall (PR) Curves for Imbalanced Churn", fontsize=12, fontweight='bold')
    ax2.set_xlabel("Recall (Coverage of Churners)", fontsize=11)
    ax2.set_ylabel("Precision (Accuracy of Churn Alerts)", fontsize=11)
    ax2.set_xlim([-0.02, 1.02])
    ax2.set_ylim([-0.02, 1.02])
    ax2.legend(loc='upper right', frameon=True)
    
    plt.tight_layout()
    fig3_path = os.path.join(vis_dir, "fig3_roc_and_pr_curves.png")
    plt.savefig(fig3_path, dpi=300)
    plt.close()

    # Figure 4: 5-Fold Cross-Validation Metrics Comparison
    fig, ax = plt.subplots(figsize=(12, 6))
    metric_keys = ['accuracy', 'balanced_accuracy', 'precision', 'recall', 'f1', 'roc_auc']
    metric_labels = ['Accuracy', 'Balanced Acc.', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC']
    
    bar_width = 0.25
    x_indices = np.arange(len(metric_keys))
    
    for i, (name, col) in enumerate(colors.items()):
        means = [cv_results[name][m]['mean'] for m in metric_keys]
        stds = [cv_results[name][m]['std'] for m in metric_keys]
        pos = x_indices + (i - 1) * bar_width
        ax.bar(pos, means, yerr=stds, width=bar_width, capsize=4, label=name, color=col, alpha=0.85, edgecolor='black')
        
    ax.set_title("5-Fold Stratified Cross-Validation Generalization Performance", fontsize=13, fontweight='bold')
    ax.set_xticks(x_indices)
    ax.set_xticklabels(metric_labels, fontsize=11, fontweight='bold')
    ax.set_ylabel("Metric Score", fontsize=11)
    ax.set_ylim(0, 1.05)
    ax.legend(loc='lower left', frameon=True)
    
    plt.tight_layout()
    fig4_path = os.path.join(vis_dir, "fig4_cv_performance_comparison.png")
    plt.savefig(fig4_path, dpi=300)
    plt.close()

    # Figure 5: Feature Importance Comparison (Logistic Regression vs Random Forest)
    # Extract feature names after One-Hot Encoding
    ohe = fitted_pipelines['Logistic Regression'].named_steps['preprocessor'].named_transformers_['cat']
    encoded_cat_names = list(ohe.get_feature_names_out(categorical_features))
    all_feature_names = numeric_features + encoded_cat_names + passthrough_features
    
    # Logistic Regression standardized coefficients
    lr_coefs = fitted_pipelines['Logistic Regression'].named_steps['classifier'].coef_[0]
    # Random Forest feature importances
    rf_importances = fitted_pipelines['Random Forest'].named_steps['classifier'].feature_importances_
    
    feat_df = pd.DataFrame({
        'Feature': all_feature_names,
        'LR_Coef': lr_coefs,
        'RF_Importance': rf_importances,
        'Abs_LR_Coef': np.abs(lr_coefs)
    })
    
    top_rf = feat_df.sort_values(by='RF_Importance', ascending=False).head(10)
    top_lr = feat_df.sort_values(by='Abs_LR_Coef', ascending=False).head(10)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Logistic Regression Coefficients
    sns.barplot(data=top_lr, y='Feature', x='LR_Coef', ax=ax1, palette='vlag', hue='Feature', legend=False)
    ax1.set_title("Top 10 Feature Weights: Logistic Regression (Log-Odds Impact)", fontsize=12, fontweight='bold')
    ax1.set_xlabel("Standardized Coefficient (Positive = Increases Churn)", fontsize=11)
    ax1.axvline(0, color='gray', linestyle='--')
    
    # Random Forest Feature Importance
    sns.barplot(data=top_rf, y='Feature', x='RF_Importance', ax=ax2, palette='Blues_r', hue='Feature', legend=False)
    ax2.set_title("Top 10 Feature Importance: Random Forest (Gini Impurity Decrease)", fontsize=12, fontweight='bold')
    ax2.set_xlabel("Mean Decrease in Impurity", fontsize=11)
    
    plt.tight_layout()
    fig5_path = os.path.join(vis_dir, "fig5_feature_importance.png")
    plt.savefig(fig5_path, dpi=300)
    plt.close()

    # Figure 6: Learning Curves & Overfitting Diagnosis (Decision Tree Unpruned vs Pruned vs Random Forest)
    # Include an unpruned decision tree to empirically demonstrate severe overfitting
    unpruned_dt = DecisionTreeClassifier(random_state=42) # unconstrained
    unpruned_pipe = Pipeline([('pre', preprocessor), ('clf', unpruned_dt)])
    
    train_sizes = np.linspace(0.1, 1.0, 6)
    
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    diagnostics = [
        ('Unpruned Decision Tree\n(Overfitting: High Variance)', unpruned_pipe),
        ('Pruned Decision Tree\n(Balanced: Max Depth = 5)', fitted_pipelines['Decision Tree (Pruned)']),
        ('Random Forest Ensemble\n(Generalization: 150 Trees)', fitted_pipelines['Random Forest'])
    ]
    
    for idx, (title, pipe_to_eval) in enumerate(diagnostics):
        t_sizes, t_scores, v_scores = learning_curve(
            pipe_to_eval, X_train, y_train, cv=skf, scoring='f1',
            train_sizes=train_sizes, random_state=42, n_jobs=-1
        )
        t_mean, t_std = np.mean(t_scores, axis=1), np.std(t_scores, axis=1)
        v_mean, v_std = np.mean(v_scores, axis=1), np.std(v_scores, axis=1)
        
        axes[idx].plot(t_sizes, t_mean, 'o-', color='#E74C3C', label='Training F1-Score', lw=2)
        axes[idx].fill_between(t_sizes, t_mean - t_std, t_mean + t_std, alpha=0.15, color='#E74C3C')
        axes[idx].plot(t_sizes, v_mean, 'o-', color='#2B5C8F', label='Validation F1-Score', lw=2)
        axes[idx].fill_between(t_sizes, v_mean - v_std, v_mean + v_std, alpha=0.15, color='#2B5C8F')
        
        axes[idx].set_title(title, fontsize=11, fontweight='bold', pad=10)
        axes[idx].set_xlabel("Training Set Size", fontsize=10)
        axes[idx].set_ylabel("F1-Score" if idx == 0 else "", fontsize=10)
        axes[idx].set_ylim(0.2, 1.05)
        axes[idx].legend(loc='lower right' if idx == 0 else 'lower right', frameon=True)
        
    plt.tight_layout()
    fig6_path = os.path.join(vis_dir, "fig6_learning_curves_overfitting.png")
    plt.savefig(fig6_path, dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # 5. Export Structured JSON Results
    # -------------------------------------------------------------
    results = {
        'eda': eda_stats,
        'split_info': split_info,
        'cv_results': cv_results,
        'test_metrics': test_metrics,
        'top_features_rf': top_rf[['Feature', 'RF_Importance']].round(4).to_dict(orient='records'),
        'top_features_lr': top_lr[['Feature', 'LR_Coef']].round(4).to_dict(orient='records')
    }
    
    with open(output_json_path, 'w') as f:
        json.dump(results, f, indent=4)
        
    print(f"ML Pipeline executed successfully!")
    print(f"Results written to: {output_json_path}")
    print(f"Visualizations saved to: {vis_dir}")
    return results

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, ".."))
    data_file = os.path.join(project_root, "data", "customer_churn_data.csv")
    vis_folder = os.path.join(project_root, "visualizations")
    res_file = os.path.join(project_root, "data", "ml_evaluation_results.json")
    
    run_ml_pipeline(data_file, vis_folder, res_file)
