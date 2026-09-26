# 📊 Data Science & Machine Learning Portfolio — YuvaIntern Internship

[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.9+-F7931E?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Pandas](https://img.shields.io/badge/Pandas-3.0+-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![SciPy](https://img.shields.io/badge/SciPy-1.17+-0054A6?logo=scipy&logoColor=white)](https://scipy.org/)
[![Statsmodels](https://img.shields.io/badge/Statsmodels-0.15+-4C72B0)](https://www.statsmodels.org/)
[![Seaborn](https://img.shields.io/badge/Seaborn-0.13+-3776AB)](https://seaborn.pydata.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive, production-grade **Data Science, Statistical Inference, and Machine Learning Portfolio** completed as part of the **YuvaIntern / NSDC Virtual Data Science with Python Apprentice Internship**.

This repository documents the progressive journey from raw data wrangling and visual storytelling to inferential hypothesis testing and predictive machine learning modeling.

---

## 👨‍💻 Student & Internship Profile

- **Student / Intern:** Ankesh Diwakar ([@ankesh825](https://github.com/ankesh825))
- **Program:** YuvaIntern / NSDC Virtual Data Science with Python Apprentice Internship
- **Domain:** Data Science, Advanced Python Analytics & Machine Learning
- **Workload Allocation:** 30–35 Hours per Milestone Milestone Standard
- **Core Technology Stack:** Python 3.11, Pandas, NumPy, Scikit-Learn, SciPy Stats, Statsmodels, Matplotlib, Seaborn, python-docx

---

## 🗺️ 5-Week Internship Roadmap Overview

| Milestone | Task Title | Core Focus | Dataset / Domain | Key Deliverable |
| :--- | :--- | :--- | :--- | :--- |
| **Week 1** | **Data Acquisition, Cleaning & EDA** | Large-scale data wrangling, missing value treatment, summary statistics, correlation profiling | OWID COVID-19 Worldwide Dataset ($402,910$ records) | [`Week1_Data_Analysis_Report_humanized.docx`](./Week1_Data_Analysis_Report_humanized.docx) |
| **Week 2** | **Advanced Data Visualization & Storytelling** | Time-series wave analysis, vaccination rollout curves, age-specific mortality, health pressure | WHO Global COVID-19 Multi-Source Datasets | [`Week2_Advanced_COVID_Data_Storytelling_Report_FINAL.docx`](./Week2_Advanced_COVID_Data_Storytelling_Report_FINAL.docx) |
| **Week 3** | **Statistical Analysis & Hypothesis Testing** | Two-Sample Welch's $t$-test, Pearson's $\chi^2$ Test, One-Way ANOVA, Tukey HSD, Paired $t$-test | Curated E-Commerce A/B Experiment ($N = 3,000$) | [`Week3_Statistical_Analysis_Report.docx`](./Week3_Statistical_Analysis_Report.docx) |
| **Week 4** | **Machine Learning Model Development & Evaluation** | Supervised classification, leak-free Scikit-Learn pipelines, 5-Fold Stratified CV, Bias-Variance diagnostics | Enterprise Customer Churn Dataset ($N = 3,500$) | [`Week4_Machine_Learning_Model_Development_Report.docx`](./Week4_Machine_Learning_Model_Development_Report.docx) |
| **Week 5** | **Capstone Project / Model Deployment** | End-to-end model serving, pipeline deployment, production monitoring | Enterprise Business Case Study | *Upcoming Final Milestone* |

---

## 📋 Table of Contents
1. [Week 1: Data Acquisition, Cleaning & Exploratory Analysis](#-week-1--data-acquisition-cleaning--exploratory-analysis)
2. [Week 2: Advanced Data Visualization & Storytelling](#-week-2--advanced-data-visualization--storytelling)
3. [Week 3: Statistical Analysis & Hypothesis Testing](#-week-3--statistical-analysis--hypothesis-testing)
4. [Week 4: Machine Learning Model Development & Evaluation](#-week-4--machine-learning-model-development--evaluation)
5. [Complete Repository Structure](#-complete-repository-structure)
6. [Installation & Reproduction Guide](#-installation--reproduction-guide)
7. [Official Deliverable Reports](#-official-deliverable-reports)

---

# 🦠 Week 1 — Data Acquisition, Cleaning & Exploratory Analysis

### Objective
The primary objective of Week 1 was to ingest, audit, and clean an extensive real-world epidemiological dataset, building a robust preprocessing pipeline for Exploratory Data Analysis (EDA).

### Dataset Overview
- **Data Source:** Our World in Data (OWID) COVID-19 Global Dataset
- **Raw Volume:** $429,435$ rows $\times$ $67$ columns
- **Features Captured:** Daily and cumulative confirmed cases/deaths, testing policies, vaccination rates, population demographics, GDP per capita, median age, and hospital capacity.

### Data Cleaning & Preprocessing Pipeline
1. **Datetime Parsing:** Converted string date fields to ISO datetime objects for chronological indexing.
2. **Entity Deduplication:** Filtered out aggregate supranational entities (e.g., "World", "Upper middle income", "Europe") to maintain national granularity.
3. **Daily Flow Imputation:** Replaced unrecorded daily cases (`new_cases`) and deaths (`new_deaths`) with zero values, representing days without reported transmission.
4. **Cumulative Forward-Filling:** Applied localized forward-filling (`ffill()`) within each country's timeline to preserve monotonicity in cumulative metrics (`total_cases`, `total_deaths`).
5. **Static Indicator Imputation:** Filled invariant socioeconomic variables (`population`, `gdp_per_capita`, `median_age`) using country-level bidirectional filling (`ffill().bfill()`).
6. **Curated Analytical Dataset:** Reduced to a leak-free shape of **$402,910$ rows $\times$ $19$ core columns** with $0\%$ missing values in primary analytical fields.

### Key EDA Insights
- **Demographic Vulnerability:** National median age showed a strong positive correlation with reported case fatality rates ($r \approx 0.68$).
- **Economic Disparity in Immunization:** Countries in the top GDP per capita quartile attained $70\%$ primary vaccination coverage 8 months faster than lower-quartile nations.
- **Asynchronous Wave Dynamics:** Distinct transmission waves peaked at different periods across continents, underscoring geographic and seasonal variation.

*Script:* [`Week_1_Data Acquisition, Cleaning, and Exploratory Analysis.python`](./Week_1_Data%20Acquisition%2C%20Cleaning%2C%20and%20Exploratory%20Analysis.python)  
*Report:* [`Week1_Data_Analysis_Report_humanized.docx`](./Week1_Data_Analysis_Report_humanized.docx)

---

# 📈 Week 2 — Advanced Data Visualization & Storytelling

### Objective
Week 2 shifted the focus from descriptive tables to visual communication and data storytelling, producing multi-panel publication-grade figures that communicate public health trends.

### Data Sources
Utilized official World Health Organization (WHO) datasets encompassing global daily trends, regional vaccination uptake, hospitalization/ICU admissions, and age-stratified mortality.

### Visual Stories Developed
1. **Global Case & Mortality Trajectories:** Dual-axis longitudinal time-series tracking global transmission surges and corresponding mortality peaks.
2. **Cross-Country Comparative Waves:** 4-week rolling averages comparing transmission curves across five anchor nations (India, United States, Brazil, United Kingdom, and Germany).
3. **Vaccination Uptake Velocity:** Progress curves illustrating primary series completion rates against emerging variant waves.
4. **Cross-National Immunization Benchmarking:** Horizontal comparative bar charts highlighting global vaccination disparities.
5. **Age-Stratified Mortality Profiles:** Distributional breakdown showing that populations aged $65+$ accounted for $>75\%$ of cumulative global fatalities.
6. **Per-Capita Excess Mortality Ranking:** Normalized death rates per $100,000$ population identifying the hardest-hit national healthcare systems.
7. **Hospital & ICU Bed Utilization:** Healthcare strain analysis demonstrating bed capacity saturation during peak variant surges.

*Script:* [`Week 2 Python code .py`](./Week%202%20Python%20code%20.py)  
*Report:* [`Week2_Advanced_COVID_Data_Storytelling_Report_FINAL.docx`](./Week2_Advanced_COVID_Data_Storytelling_Report_FINAL.docx)

---

# 🧪 Week 3 — Statistical Analysis & Hypothesis Testing

### Objective
Week 3 transitioned from exploratory analysis to **inferential statistics**, using statistical methods to validate or refute four distinct business hypotheses on a curated experimental dataset ($N = 3,000$ user sessions).

### Experimental Setup
- **Sample Size:** $N = 3,000$ user sessions (Control: $1,485$; Treatment: $1,515$)
- **Significance Level:** Pre-specified $\alpha = 0.05$ with $95\%$ Confidence Intervals
- **Diagnostic Battery:** Shapiro-Wilk and D'Agostino-Pearson tests for normality, Levene's test for homoscedasticity, and Q-Q distributional inspections.

### Hypotheses Battery & Empirical Findings

```text
                                  WEEK 3 HYPOTHESIS TESTING BATTERY
┌─────────────────────────────────┬───────────────────────────────┬───────────────────────────────┬──────────────┐
│ Hypothesis Ref. & Target Metric │ Statistical Test Executed     │ Test Statistic & p-Value      │ Effect Size  │
├─────────────────────────────────┼───────────────────────────────┼───────────────────────────────┼──────────────┤
│ H1: Average Order Value (AOV)   │ Welch's Two-Sample t-Test     │ t = 3.324, p = 9.56e-04       │ Cohen's d    │
│     (Treatment vs Control)      │ Mann-Whitney U (Non-param)    │ U = 34,620.5, p = 2.40e-03    │ = 0.30       │
├─────────────────────────────────┼───────────────────────────────┼───────────────────────────────┼──────────────┤
│ H2: Device vs Conversion        │ Pearson's Chi-Square (χ²)     │ χ²(2) = 20.985, p = 2.77e-05  │ Cramér's V   │
│     (Desktop, Mobile, Tablet)   │ Residual Heatmap Analysis     │ df = 2                        │ = 0.084      │
├─────────────────────────────────┼───────────────────────────────┼───────────────────────────────┼──────────────┤
│ H3: Channel vs Session Duration │ One-Way ANOVA                 │ F(3, 2996) = 402.37, p < 1e-100│ Eta-Squared  │
│     (Email, Organic, Paid, Soc) │ Tukey's HSD Post-Hoc          │ All 6 pairs: p_adj < 0.001    │ η² = 0.287   │
├─────────────────────────────────┼───────────────────────────────┼───────────────────────────────┼──────────────┤
│ H4: Longitudinal Loyalty Score  │ Paired Samples t-Test         │ t(525) = 35.16, p = 4.26e-140 │ Cohen's dz   │
│     (Pre vs Post Onboarding)    │ Wilcoxon Signed-Rank          │ W = 587.5, p = 2.15e-77       │ = 1.53       │
└─────────────────────────────────┴───────────────────────────────┴───────────────────────────────┴──────────────┘
```

### Key Statistical Results
1. **$H_1$ Revenue Uplift Validated:** Converted Treatment AOV ($\$92.01$) significantly exceeded Control AOV ($\$85.46$) by $+\$6.55$ ($95\%\text{ CI}: [+\$2.68, +\$10.42]$, $p = 9.56 \times 10^{-4}$).
2. **$H_2$ Device Dependency Confirmed:** Desktop converted at $20.06\%$ (Std. Residual $+2.87$), whereas Mobile converted at only $13.68\%$ (Std. Residual $-2.79$), rejecting independence ($\chi^2 = 20.985, p = 2.77 \times 10^{-5}$).
3. **$H_3$ Marketing Channel Heterogeneity:** Session duration varied across channels ($F = 402.37, p < 10^{-100}, \eta^2 = 0.287$), with Email ($6.71$ min) and Organic ($5.54$ min) driving $2\times$ the dwell time of Social Media ($2.80$ min).
4. **$H_4$ Customer Retention Impact:** Repeat customer loyalty scores exhibited an average gain of $+1.34$ points on a 10-point scale ($t(525) = 35.16, p = 4.26 \times 10^{-140}$, Cohen's $d_z = 1.53$).

### Week 3 Visualizations Embedded in Report
- `fig1_normality_qq_plots.png`: Normality histograms and Q-Q distribution plots.
- `fig2_hypothesis1_aov_ttest.png`: AOV violin and box plot with statistical significance bracket.
- `fig3_hypothesis2_chisquare.png`: Conversion rates by hardware class and Pearson residuals heatmap.
- `fig4_hypothesis3_anova.png`: Session duration density distributions and Tukey HSD 95% confidence intervals.
- `fig5_hypothesis4_paired_ttest.png`: Individual loyalty trajectories and empirical pairwise differences histogram.

*Scripts:* [`run_statistical_tests.py`](./run_statistical_tests.py), [`generate_dataset.py`](./generate_dataset.py), [`build_word_report.py`](./build_word_report.py)  
*Dataset & Metrics:* [`ecommerce_ab_test_data.csv`](./ecommerce_ab_test_data.csv), [`statistical_test_results.json`](./statistical_test_results.json)  
*Report:* [`Week3_Statistical_Analysis_Report.docx`](./Week3_Statistical_Analysis_Report.docx)

---

# 🤖 Week 4 — Machine Learning Model Development & Evaluation

### Objective
Week 4 focuses on the core principles of **supervised machine learning**. The objective was to construct, benchmark, and critically evaluate three distinct classification model families for **Customer Churn Prediction** in an enterprise subscription setting ($N = 3,500$ accounts).

### Problem Formulation
Predicting the binary outcome $y \in \{0, 1\}$ (where $1 = \text{Churned}$, $0 = \text{Retained}$) to enable targeted proactive retention.

### Algorithms Selected & Theoretical Justification
1. **Logistic Regression (Parametric Linear Baseline):** Regularized with an $L_2$ Ridge penalty ($C = 1.0$), optimizing log-loss. Offers well-calibrated posterior probabilities and direct log-odds interpretability.
2. **Decision Tree Classifier (Non-Linear Rule Induction):** Recursive partitioning via the CART algorithm with Gini impurity criteria. Evaluated with cost-complexity depth constraints (`max_depth=5`, `min_samples_leaf=10`) to prevent catastrophic memorization.
3. **Random Forest Classifier (Ensemble Bagging):** Ensemble of $B = 150$ de-correlated trees utilizing bootstrap aggregation and feature subspace sampling ($\sqrt{p}$) to reduce single-tree variance.

### Leak-Free Engineering Pipeline
Constructed using Scikit-Learn's `ColumnTransformer` and `Pipeline`:
- **Stratified Split:** 80% Train ($N_{\text{train}} = 2,800$), 20% Holdout Test ($N_{\text{test}} = 700$), preserving the $15.57\%$ baseline churn incidence.
- **`StandardScaler`:** Fitted strictly on training numerical attributes (`tenure_months`, `monthly_charges`, `total_charges`, `customer_service_calls`).
- **`OneHotEncoder(drop='first')`:** Applied to nominal categorical variables to prevent the dummy variable trap.

### Comprehensive Model Performance Benchmark

#### Holdout Test Set Evaluation ($N_{\text{test}} = 700$)

| Evaluation Metric | Logistic Regression (L2) | Decision Tree (Pruned) | Random Forest (150 Trees) | Top Performing Architecture |
| :--- | :--- | :--- | :--- | :--- |
| **Accuracy** | **86.57%** | 84.14% | 85.86% | **Logistic Regression** |
| **Balanced Accuracy** | **63.99%** | 58.44% | 59.08% | **Logistic Regression** |
| **Precision (Positive Churn)** | 64.15% | 47.92% | **64.71%** | **Random Forest** |
| **Recall (Sensitivity)** | **31.19%** | 21.10% | 20.18% | **Logistic Regression** |
| **Specificity** | 96.79% | 95.77% | **97.97%** | **Random Forest** |
| **F1-Score** | **0.420** | 0.293 | 0.308 | **Logistic Regression** |
| **ROC-AUC** | **0.864** | 0.796 | 0.845 | **Logistic Regression** |
| **PR-AUC (Average Precision)**| **0.546** | 0.416 | 0.514 | **Logistic Regression** |
| **Matthews Corr. Coef. (MCC)**| **0.383** | 0.242 | 0.306 | **Logistic Regression** |
| **Brier Score (Calibration)** | **0.096** | 0.108 | 0.102 | **Logistic Regression** |

#### 5-Fold Stratified Cross-Validation (Mean $\pm$ Std)

| Algorithm | CV Accuracy | CV Balanced Acc. | CV Precision | CV Recall | CV F1-Score | CV ROC-AUC |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Logistic Regression** | $85.25\% \pm 0.70\%$ | $61.06\% \pm 2.05\%$ | $56.15\% \pm 5.24\%$ | $25.92\% \pm 4.75\%$ | $0.351 \pm 0.048$ | **$0.837 \pm 0.016$** |
| **Decision Tree (Pruned)** | $84.79\% \pm 0.41\%$ | $58.45\% \pm 1.50\%$ | $53.90\% \pm 4.11\%$ | $20.19\% \pm 4.06\%$ | $0.290 \pm 0.036$ | $0.770 \pm 0.018$ |
| **Random Forest** | **$85.61\% \pm 0.68\%$** | $59.21\% \pm 2.21\%$ | **$60.86\% \pm 5.76\%$** | $20.88\% \pm 4.60\%$ | $0.309 \pm 0.054$ | $0.822 \pm 0.016$ |

### Visualizations Embedded in Report (6 Figures)

```text
├── fig1_eda_and_correlations.png      # Class imbalance (15.6%), contract churn rates & correlation matrix
├── fig2_confusion_matrices.png        # Side-by-side normalized confusion matrices across all 3 models
├── fig3_roc_and_pr_curves.png         # Multi-model ROC-AUC and Precision-Recall discriminatory curves
├── fig4_cv_performance_comparison.png # 5-Fold Stratified CV metric stability comparison
├── fig5_feature_importance.png        # Logistic Regression log-odds weights vs Random Forest Gini importance
└── fig6_learning_curves_overfitting.png # Empirical learning curves diagnosing overfitting vs generalization
```

### Critical Discussion: Error Asymmetry & Bias-Variance
1. **Cost Asymmetry of Classification Errors:** In subscriber churn, a False Negative (failing to identify a defecting customer) costs $> \$800$ in lost lifetime value, whereas a False Positive (dispatching an unnecessary retention discount) costs $\approx \$15$. Shifting the classification threshold from $0.50$ down to $0.28$ more than doubles model recall from $31\%$ to $>65\%$.
2. **Bias-Variance Diagnosis via Learning Curves (Figure 6):** Unconstrained decision trees exhibited extreme overfitting ($100\%$ training F1 vs $25\%$ validation F1). Pre-pruning and ensemble bootstrap aggregation successfully compressed the generalization gap.
3. **Class Imbalance Limitations:** Because $84.4\%$ of accounts remain retained, raw accuracy is an uninformative metric (a trivial majority-class predictor achieves $84.4\%$ accuracy with zero utility). Balanced Accuracy, PR-AUC, and F1-Score provide the true operational benchmarks.

*Scripts:* [`train_and_evaluate_models.py`](./train_and_evaluate_models.py), [`generate_churn_dataset.py`](./generate_churn_dataset.py), [`build_ml_word_report.py`](./build_ml_word_report.py)  
*Dataset & Metrics:* [`customer_churn_data.csv`](./customer_churn_data.csv), [`ml_evaluation_results.json`](./ml_evaluation_results.json)  
*Report:* [`Week4_Machine_Learning_Model_Development_Report.docx`](./Week4_Machine_Learning_Model_Development_Report.docx)

---

# 📂 Complete Repository Structure

```text
COVID_19_DATA_ANALYSIS/
│
├── README.md                                                 # Master 5-Week Portfolio Documentation
├── requirements.txt                                          # Universal Python Dependencies
├── submission_description.txt                                # Portal Submission Summary Text
├── .gitignore                                                # Git exclusion configuration
│
├── [WEEK 1: DATA WRANGLING & EDA]
│   ├── Week_1_Data Acquisition, Cleaning, and Exploratory Analysis.python
│   └── Week1_Data_Analysis_Report_humanized.docx             # Official Week 1 Report
│
├── [WEEK 2: DATA VISUALIZATION & STORYTELLING]
│   ├── Week 2 Python code .py
│   └── Week2_Advanced_COVID_Data_Storytelling_Report_FINAL.docx # Official Week 2 Report
│
├── [WEEK 3: STATISTICAL ANALYSIS & HYPOTHESIS TESTING]
│   ├── generate_dataset.py                                   # E-commerce A/B Data Generator
│   ├── run_statistical_tests.py                              # SciPy & Statsmodels Test Battery
│   ├── build_word_report.py                                  # Week 3 DOCX Report Builder
│   ├── ecommerce_ab_test_data.csv                            # Experimental Dataset (3,000 rows)
│   ├── statistical_test_results.json                         # Structured Statistical Test Output
│   ├── Week3_Statistical_Analysis_Report.docx                # Official Week 3 Report (1.45 MB)
│   ├── fig1_normality_qq_plots.png                           # Normality & Q-Q Plots
│   ├── fig2_hypothesis1_aov_ttest.png                        # AOV Hypothesis Test Plot
│   ├── fig3_hypothesis2_chisquare.png                        # Chi-Square Residuals Plot
│   ├── fig4_hypothesis3_anova.png                            # ANOVA & Tukey HSD Plot
│   └── fig5_hypothesis4_paired_ttest.png                     # Paired Loyalty Test Plot
│
└── [WEEK 4: MACHINE LEARNING MODEL DEVELOPMENT]
    ├── generate_churn_dataset.py                             # Churn Dataset Generator
    ├── train_and_evaluate_models.py                          # Scikit-Learn Training & CV Pipeline
    ├── build_ml_word_report.py                               # Week 4 DOCX Report Builder
    ├── customer_churn_data.csv                               # Enterprise Churn Dataset (3,500 rows)
    ├── ml_evaluation_results.json                            # Structured ML Test Metrics & CV
    ├── Week4_Machine_Learning_Model_Development_Report.docx  # Official Week 4 Report (2.24 MB)
    ├── fig1_eda_and_correlations.png                         # EDA & Correlation Matrix
    ├── fig2_confusion_matrices.png                           # Multi-Model Confusion Matrices
    ├── fig3_roc_and_pr_curves.png                            # ROC-AUC & Precision-Recall Curves
    ├── fig4_cv_performance_comparison.png                    # 5-Fold Stratified CV Comparison
    ├── fig5_feature_importance.png                           # Feature Importance Scorecard
    └── fig6_learning_curves_overfitting.png                  # Bias-Variance Learning Curves
```

---

# ▶️ Installation & Reproduction Guide

### 1. Clone the Repository
```bash
git clone https://github.com/ankesh825/COVID_19_DATA_ANALYSIS.git
cd COVID_19_DATA_ANALYSIS
```

### 2. Set Up Environment & Dependencies
```bash
pip install -r requirements.txt
```

### 3. Execute Individual Weekly Pipelines

#### Run Week 1 (Data Cleaning & EDA):
```bash
python "Week_1_Data Acquisition, Cleaning, and Exploratory Analysis.python"
```

#### Run Week 2 (Visual Storytelling):
```bash
python "Week 2 Python code .py"
```

#### Run Week 3 (Statistical Hypothesis Testing):
```bash
python run_statistical_tests.py
python build_word_report.py
```

#### Run Week 4 (Machine Learning Model Training & Evaluation):
```bash
python train_and_evaluate_models.py
python build_ml_word_report.py
```

---

# 📑 Official Deliverable Reports

Each milestone's official comprehensive Word report is compiled and available in the repository root:

- 📄 **Week 1 Report:** [`Week1_Data_Analysis_Report_humanized.docx`](./Week1_Data_Analysis_Report_humanized.docx)
- 📄 **Week 2 Report:** [`Week2_Advanced_COVID_Data_Storytelling_Report_FINAL.docx`](./Week2_Advanced_COVID_Data_Storytelling_Report_FINAL.docx)
- 📄 **Week 3 Report:** [`Week3_Statistical_Analysis_Report.docx`](./Week3_Statistical_Analysis_Report.docx)
- 📄 **Week 4 Report:** [`Week4_Machine_Learning_Model_Development_Report.docx`](./Week4_Machine_Learning_Model_Development_Report.docx)
