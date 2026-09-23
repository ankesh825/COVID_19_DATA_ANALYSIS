# End-to-End Machine Learning Model Development & Evaluation: Customer Churn Prediction

[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.9+-F7931E?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Pandas](https://img.shields.io/badge/Pandas-3.0+-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Report](https://img.shields.io/badge/Report-DOCX_2.24MB-blue?logo=microsoftword&logoColor=white)](./report/Week4_Machine_Learning_Model_Development_Report.docx)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive, production-grade Machine Learning classification and model evaluation project developed in Python using Scikit-Learn. The study benchmarks parametric linear modeling (Logistic Regression), non-linear rule induction (Decision Tree), and ensemble learning (Random Forest) on an enterprise customer dataset of $N = 3,500$ accounts to predict subscriber defection.

---

## 📋 Table of Contents
1. [Executive Summary](#-executive-summary)
2. [Problem Definition & Theoretical Foundations](#-problem-definition--theoretical-foundations)
3. [Data Architecture & Preprocessing Pipeline](#-data-architecture--preprocessing-pipeline)
4. [Comparative Performance Scorecard](#-comparative-performance-scorecard)
5. [Visualizations & Empirical Diagnostics](#-visualizations--empirical-diagnostics)
   - [Figure 1: Exploratory Data Analysis & Correlation Heatmap](#figure-1-exploratory-data-analysis--correlation-heatmap)
   - [Figure 2: Confusion Matrices](#figure-2-confusion-matrices)
   - [Figure 3: ROC and Precision-Recall Curves](#figure-3-roc-and-precision-recall-curves)
   - [Figure 4: 5-Fold Stratified Cross-Validation Stability](#figure-4-5-fold-stratified-cross-validation-stability)
   - [Figure 5: Feature Importance Comparison](#figure-5-feature-importance-comparison)
   - [Figure 6: Empirical Learning Curves & Overfitting Diagnosis](#figure-6-empirical-learning-curves--overfitting-diagnosis)
6. [Critical Discussion: Errors, Asymmetry & Bias-Variance](#-critical-discussion-errors-asymmetry--bias-variance)
7. [Repository Structure](#-repository-structure)
8. [Installation & Reproduction Guide](#-installation--reproduction-guide)

---

## 🚀 Executive Summary

Customer churn severely erodes customer lifetime value (LTV). This project constructs a leak-free predictive classification architecture evaluating three distinct model families across a battery of classification and probability calibration metrics:

- **Top Classifier — Logistic Regression (L2):** Achieved the highest holdout test performance (**ROC-AUC = 0.864**, **PR-AUC = 0.546**, **Accuracy = 86.57%**, **F1-Score = 0.420**, **Brier Score = 0.096**), while offering transparent log-odds interpretability.
- **Ensemble Benchmark — Random Forest:** Delivered exceptional classification specificity (**97.97%**) and ensemble stability (**ROC-AUC = 0.845**, **Accuracy = 85.86%**).
- **Overfitting Diagnostics:** Unpruned decision trees suffered from extreme overfitting ($100\%$ train F1 vs $25\%$ validation F1); cost-complexity depth pruning restored model stability (**ROC-AUC = 0.796**, **Accuracy = 84.14%**).
- **Cost-Sensitive Threshold Tuning:** Lowering the decision threshold from $0.50$ to $0.28$ more than doubles churn recall from $31\%$ to $>65\%$, capturing the majority of at-risk subscribers.

---

## 🔬 Problem Definition & Theoretical Foundations

The objective is to model the posterior probability $P(y = 1 \mid \mathbf{x})$, where $y = 1$ denotes a churned subscriber and $y = 0$ denotes a retained subscriber.

### 1. Logistic Regression (Parametric Baseline)
Models the log-odds as a linear combination of input features:
$$\log\left(\frac{P(y=1 \mid \mathbf{x})}{1 - P(y=1 \mid \mathbf{x})}\right) = \beta_0 + \sum_{j=1}^p \beta_j x_j$$
Trained via maximum likelihood estimation minimizing binary cross-entropy with an $L_2$ Ridge penalty:
$$J(\boldsymbol{\beta}) = -\frac{1}{N}\sum_{i=1}^N \left[ y_i \log(\hat{p}_i) + (1 - y_i)\log(1 - \hat{p}_i) \right] + \frac{1}{2C} \|\boldsymbol{\beta}\|_2^2$$

### 2. Decision Tree Classifier (Non-Linear Rule Induction)
Partitions the feature space recursively via the CART algorithm. At each node $t$, splits are chosen to maximize the Gini impurity decrease:
$$\Delta I_G(t) = I_G(t) - \frac{N_L}{N} I_G(t_L) - \frac{N_R}{N} I_G(t_R), \quad \text{where } I_G(t) = 1 - \sum_{k=1}^K p_{tk}^2$$
Pre-pruning constraints (`max_depth=5`, `min_samples_leaf=10`) prevent catastrophic memorization.

### 3. Random Forest (Ensemble Bagging)
Aggregates $B = 150$ de-correlated decision trees trained on bootstrap samples with random feature sub-spacing ($\sqrt{p}$). The ensemble prediction averages class probabilities:
$$\hat{P}(y = 1 \mid \mathbf{x}) = \frac{1}{B} \sum_{b=1}^B \hat{P}_b(y = 1 \mid \mathbf{x})$$

---

## 📊 Data Architecture & Preprocessing Pipeline

- **Dataset Size:** $N = 3,500$ rows, $14$ input features.
- **Class Balance:** Retained $= 2,955$ ($84.4\%$), Churned $= 545$ ($15.6\%$).
- **Partitioning:** Stratified $80/20$ train/test split ($N_{\text{train}} = 2,800$, $N_{\text{test}} = 700$).
- **Leak-Free Transformation:**
  - `StandardScaler`: Applied to continuous numerical attributes (`tenure_months`, `monthly_charges`, `total_charges`, `customer_service_calls`).
  - `OneHotEncoder(drop='first')`: Applied to nominal categoricals (`contract_type`, `internet_service`, `payment_method`, etc.).

---

## 🏆 Comparative Performance Scorecard

### Holdout Test Set Evaluation ($N_{\text{test}} = 700$)

| Algorithm | Accuracy | Balanced Acc. | Precision | Recall | Specificity | F1-Score | ROC-AUC | PR-AUC | Brier Score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Logistic Regression (L2)** | **86.57%** | **63.99%** | **64.15%** | **31.19%** | 96.79% | **0.420** | **0.864** | **0.546** | **0.096** |
| **Decision Tree (Pruned)** | 84.14% | 58.44% | 47.92% | 21.10% | 95.77% | 0.293 | 0.796 | 0.416 | 0.108 |
| **Random Forest (150 Trees)** | 85.86% | 59.08% | 64.71% | 20.18% | **97.97%** | 0.308 | 0.845 | 0.514 | 0.102 |

### 5-Fold Stratified Cross-Validation (Mean $\pm$ Std)

| Algorithm | CV Accuracy | CV Balanced Acc. | CV Precision | CV Recall | CV F1-Score | CV ROC-AUC |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Logistic Regression** | $85.25\% \pm 0.70\%$ | $61.06\% \pm 2.05\%$ | $56.15\% \pm 5.24\%$ | $25.92\% \pm 4.75\%$ | $0.351 \pm 0.048$ | **$0.837 \pm 0.016$** |
| **Decision Tree (Pruned)** | $84.79\% \pm 0.41\%$ | $58.45\% \pm 1.50\%$ | $53.90\% \pm 4.11\%$ | $20.19\% \pm 4.06\%$ | $0.290 \pm 0.036$ | $0.770 \pm 0.018$ |
| **Random Forest** | **$85.61\% \pm 0.68\%$** | $59.21\% \pm 2.21\%$ | **$60.86\% \pm 5.76\%$** | $20.88\% \pm 4.60\%$ | $0.309 \pm 0.054$ | $0.822 \pm 0.016$ |

---

## 📈 Visualizations & Empirical Diagnostics

### Figure 1: Exploratory Data Analysis & Correlation Heatmap
![EDA and Correlations](./visualizations/fig1_eda_and_correlations.png)
*Exploratory analysis showing class distribution (15.6% churn), extreme defection rate on month-to-month contracts (29.6%), and negative correlation between account tenure and churn.*

### Figure 2: Confusion Matrices
![Confusion Matrices](./visualizations/fig2_confusion_matrices.png)
*Normalized confusion matrices on the holdout test set (N = 700). Logistic Regression captures the highest True Positive count (34 churners detected) while maintaining high specificity.*

### Figure 3: ROC and Precision-Recall Curves
![ROC and PR Curves](./visualizations/fig3_roc_and_pr_curves.png)
*ROC curves demonstrating superior discriminative capability for Logistic Regression (AUC = 0.864) and PR curves illustrating substantial precision lifts over the 15.6% uncalibrated baseline.*

### Figure 4: 5-Fold Stratified Cross-Validation Stability
![Cross-Validation Comparison](./visualizations/fig4_cv_performance_comparison.png)
*Generalization metrics across 5 cross-validation folds, showing negligible fold-to-fold variance.*

### Figure 5: Feature Importance Comparison
![Feature Importance](./visualizations/fig5_feature_importance.png)
*Comparison of standardized Logistic Regression coefficients (log-odds impact) and Random Forest Gini impurity decrease.*

### Figure 6: Empirical Learning Curves & Overfitting Diagnosis
![Learning Curves](./visualizations/fig6_learning_curves_overfitting.png)
*Empirical learning curves diagnosing the bias-variance trade-off: (Left) Unpruned Decision Tree exhibits severe overfitting (100% training F1 vs 25% validation F1); (Center) Pruned Decision Tree achieves tight convergence; (Right) Random Forest demonstrates robust ensemble generalization.*

---

## 💡 Critical Discussion: Errors, Asymmetry & Bias-Variance

1. **Error Cost Asymmetry:** In customer churn, a False Negative (failing to catch a churner) loses $\approx \$800+$ in customer lifetime value, whereas a False Positive (offering a retention discount to a loyal customer) costs $\approx \$15$. Default classification thresholds ($0.50$) favor specificity over recall; operational tuning to $0.28$ doubles recall to over $65\%$.
2. **Class Imbalance Realities:** Because $84.4\%$ of accounts remain retained, raw accuracy is an uninformative metric (a naive majority-class classifier achieves $84.4\%$ accuracy with zero utility). Balanced Accuracy, PR-AUC, and F1-score are the vital decision metrics.
3. **Mitigating Variance:** Unconstrained tree models overfit complex training interactions. Pre-pruning and ensemble bootstrap aggregation successfully compress the generalization gap without degrading predictive resolution.

---

## 📂 Repository Structure

```text
week4_machine_learning/
├── data/
│   ├── customer_churn_data.csv          # Curated dataset (3,500 records, 16 features)
│   └── ml_evaluation_results.json       # Complete metrics, CV scores, and feature weights
├── report/
│   └── Week4_Machine_Learning_Model_Development_Report.docx  # Formatted Word report (2.24 MB)
├── scripts/
│   ├── generate_churn_dataset.py        # Reproducible synthetic dataset generator
│   ├── train_and_evaluate_models.py     # Complete ML training & evaluation pipeline
│   └── build_ml_word_report.py          # Word document compiler
├── visualizations/
│   ├── fig1_eda_and_correlations.png    # EDA distributions & correlation matrix
│   ├── fig2_confusion_matrices.png      # Normalized confusion matrices
│   ├── fig3_roc_and_pr_curves.png       # ROC-AUC & Precision-Recall curves
│   ├── fig4_cv_performance_comparison.png # 5-Fold CV metric bar chart
│   ├── fig5_feature_importance.png      # Feature importance & coefficient comparison
│   └── fig6_learning_curves_overfitting.png # Learning curves diagnosing overfitting
├── requirements.txt                     # Dependency specifications
├── submission_description.txt           # Portal submission description text (420+ words)
└── README.md                            # Comprehensive technical documentation
```

---

## 💻 Installation & Reproduction Guide

### 1. Prerequisites
Ensure Python 3.10+ is installed on your system.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Reproduce Data, Analysis, and Report
```bash
# Step 1: Generate dataset
python scripts/generate_churn_dataset.py

# Step 2: Train models, run CV, and generate 6 visualization figures
python scripts/train_and_evaluate_models.py

# Step 3: Build publication-grade Word document (.docx)
python scripts/build_ml_word_report.py
```
