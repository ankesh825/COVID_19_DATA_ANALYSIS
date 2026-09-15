# Empirical Evaluation of Digital Product Interventions: A Multi-Factor Hypothesis Testing & Inferential Statistical Analysis

[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![SciPy](https://img.shields.io/badge/SciPy-1.17+-0054A6?logo=scipy&logoColor=white)](https://scipy.org/)
[![Statsmodels](https://img.shields.io/badge/Statsmodels-0.15+-4C72B0)](https://www.statsmodels.org/)
[![Pandas](https://img.shields.io/badge/Pandas-3.0+-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Report](https://img.shields.io/badge/Report-DOCX_1.45MB-blue?logo=microsoftword&logoColor=white)](./report/Week3_Statistical_Analysis_Report.docx)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A rigorous, end-to-end inferential statistical analysis and hypothesis testing study investigating the impact of product interventions, device characteristics, acquisition channels, and personalized retention onboarding on e-commerce user engagement and revenue.

---

## 📋 Table of Contents
1. [Executive Summary](#-executive-summary)
2. [Formulated Hypotheses Battery](#-formulated-hypotheses-battery)
3. [Dataset Architecture & Exploratory Analysis](#-dataset-architecture--exploratory-analysis)
4. [Statistical Methodology & Diagnostics](#-statistical-methodology--diagnostics)
5. [Key Inferential Findings & Visualizations](#-key-inferential-findings--visualizations)
   - [Hypothesis 1: Revenue Impact (Welch's t-Test & Mann-Whitney U)](#hypothesis-1-revenue-impact-on-average-order-value-aov)
   - [Hypothesis 2: Device Conversion Independence (Pearson Chi-Square)](#hypothesis-2-device-category-vs-conversion-independence)
   - [Hypothesis 3: Marketing Channel Heterogeneity (One-Way ANOVA & Tukey HSD)](#hypothesis-3-marketing-channel-impact-on-session-duration)
   - [Hypothesis 4: Customer Retention Dynamics (Paired t-Test & Wilcoxon Signed-Rank)](#hypothesis-4-within-subject-customer-loyalty-intervention)
6. [Hypothesis Validation Matrix](#-hypothesis-validation-matrix)
7. [Repository Structure](#-repository-structure)
8. [Installation & Reproduction Guide](#-installation--reproduction-guide)

---

## 🚀 Executive Summary

Modern e-commerce enterprises rely on controlled experimentation (A/B testing) to make capital and engineering decisions. This study applies classical parametric and non-parametric hypothesis testing frameworks across $N = 3,000$ user sessions to evaluate key platform initiatives.

**Core Findings:**
- **AOV Uplift ($+\$6.55$):** Treatment checkout flow yielded a statistically significant increase in Average Order Value ($t(472.4) = 3.32, p = 9.56 \times 10^{-4}$, Cohen's $d = 0.30$), reinforced by non-parametric Mann-Whitney U ($p = 2.40 \times 10^{-3}$).
- **Severe Mobile Friction:** Conversion rate is strongly dependent on device type ($\chi^2(2) = 20.98, p = 2.77 \times 10^{-5}$, Cramér's $V = 0.084$), with mobile converting at only $13.68\%$ (residual $-2.79$) versus desktop at $20.06\%$ (residual $+2.87$).
- **Channel Engagement Heterogeneity:** Acquisition channels drive massive variance in on-site dwell time (One-Way ANOVA $F(3, 2996) = 402.37, p < 10^{-100}, \eta^2 = 0.287$). Email and Organic search generate over $2\times$ the session duration of Social Media.
- **Loyalty Program Success:** Personalized onboarding generated an average within-subject gain of $+1.34$ points on a 10-point satisfaction scale ($t(525) = 35.16, p = 4.26 \times 10^{-140}$, Cohen's $d_z = 1.53$).

---

## 🎯 Formulated Hypotheses Battery

| Hypothesis Ref. | Target Variable & Metric | Null Hypothesis ($H_0$) | Alternative Hypothesis ($H_1$) | Statistical Test |
| :--- | :--- | :--- | :--- | :--- |
| **$H_1$ (Revenue)** | Average Order Value (AOV in USD) | $H_{0,1}: \mu_T = \mu_C$ (No difference in mean checkout value) | $H_{1,1}: \mu_T \neq \mu_C$ (Treatment significantly alters checkout value) | Welch's Two-Sample $t$-test & Mann-Whitney U |
| **$H_2$ (Conversion)** | Conversion Status (0/1) vs Device | $H_{0,2}: P(\text{Conv} \mid \text{Device}) = P(\text{Conv})$ (Conversion is independent) | $H_{1,2}: P(\text{Conv} \mid \text{Device}) \neq P(\text{Conv})$ (Conversion is dependent) | Pearson's $\chi^2$ Test of Independence |
| **$H_3$ (Engagement)** | Session Duration (Mins) vs Channel | $H_{0,3}: \mu_{\text{Email}} = \mu_{\text{Org}} = \mu_{\text{Paid}} = \mu_{\text{Soc}}$ | $H_{1,3}: \exists i, j \text{ s.t. } \mu_i \neq \mu_j$ | One-Way ANOVA & Tukey HSD Post-Hoc |
| **$H_4$ (Retention)** | Within-Subject Loyalty Score (1–10) | $H_{0,4}: \mu_{\text{Difference}} = 0$ (Zero shift post-intervention) | $H_{1,4}: \mu_{\text{Difference}} \neq 0$ (Significant shift post-intervention) | Paired Samples $t$-test & Wilcoxon Signed-Rank |

---

## 📊 Dataset Architecture & Exploratory Analysis

The study operates on a balanced experimental dataset of $N = 3,000$ unique visitor sessions:
- **Control Group:** $n = 1,485$ ($49.5\%$), legacy checkout and recommendations.
- **Treatment Group:** $n = 1,515$ ($50.5\%$), machine-learning recommendations and one-page checkout.
- **Global Conversion Rate:** $16.47\%$ ($494$ total orders; Control $= 14.21\%$, Treatment $= 18.68\%$, an absolute uplift of $+4.47\%$).
- **Device Traffic Shares:** Mobile ($55.3\%$), Desktop ($35.1\%$), Tablet ($9.6\%$).
- **Marketing Channels:** Organic Search ($30.9\%$), Paid Search ($26.8\%$), Social Media ($23.2\%$), Email Campaign ($19.1\%$).

---

## 🔬 Statistical Methodology & Diagnostics

Before executing parametric inference, strict diagnostic assumptions were validated:
1. **Normality:** Shapiro-Wilk test, D'Agostino-Pearson omnibus test, and Q-Q plots.
2. **Homoscedasticity:** Levene's test centered at the median.
3. **Robustness:** Welch-Satterthwaite degrees of freedom correction applied where variances could diverge.
4. **Post-Hoc Multi-Comparisons:** Tukey HSD controlling family-wise error rate ($\alpha_{\text{FW}} = 0.05$).
5. **Effect Sizes:** Cohen's $d$, Cramér's $V$, and Eta-Squared ($\eta^2$).

---

## 📈 Key Inferential Findings & Visualizations

### Hypothesis 1: Revenue Impact on Average Order Value (AOV)

- **Control AOV:** Mean $= \$85.46$ (SD $= \$20.79$, Median $= \$87.84$, $n = 211$)
- **Treatment AOV:** Mean $= \$92.01$ (SD $= \$22.79$, Median $= \$92.42$, $n = 283$)
- **Mean Difference:** $+\$6.55$ USD ($\text{SE} = \$1.97$, $95\%\text{ CI}: [+\$2.68, +\$10.42]$)
- **Welch's $t$-Test:** $t(472.4) = 3.324, p = 9.56 \times 10^{-4}$ (Reject $H_0$)
- **Effect Size:** Cohen's $d = 0.298$ (Small-to-medium positive effect)
- **Mann-Whitney U:** $U = 34,620.5, p = 2.40 \times 10^{-3}$ (Reject $H_0$)

![Normality & Q-Q Plots](./visualizations/fig1_normality_qq_plots.png)
*Figure 1: Distribution checks and Q-Q plots for Control and Treatment AOV.*

![Hypothesis 1 AOV Test](./visualizations/fig2_hypothesis1_aov_ttest.png)
*Figure 2: Violin and box plot comparison of Average Order Value with statistical significance bracket.*

---

### Hypothesis 2: Device Category vs Conversion Independence

- **Desktop ($n = 1,052$):** $211$ Converted ($20.06\%$), Expected $= 173.2$, Std. Residual $= +2.87$
- **Mobile ($n = 1,659$):** $227$ Converted ($13.68\%$), Expected $= 273.2$, Std. Residual $= -2.79$
- **Tablet ($n = 289$):** $56$ Converted ($19.38\%$), Expected $= 47.6$, Std. Residual $= +1.22$
- **Pearson's $\chi^2$ Test:** $\chi^2(2) = 20.985, p = 2.77 \times 10^{-5}$ (Reject $H_0$)
- **Effect Size:** Cramér's $V = 0.084$

![Chi-Square Analysis](./visualizations/fig3_hypothesis2_chisquare.png)
*Figure 3: Conversion rates by device hardware class alongside standardized Pearson residuals heatmap.*

---

### Hypothesis 3: Marketing Channel Impact on Session Duration

- **Email Campaign ($n = 573$):** Mean $= 6.71$ mins (SD $= 2.89$, Median $= 6.22$)
- **Organic Search ($n = 927$):** Mean $= 5.54$ mins (SD $= 2.46$, Median $= 5.19$)
- **Paid Search ($n = 804$):** Mean $= 3.89$ mins (SD $= 1.93$, Median $= 3.50$)
- **Social Media ($n = 696$):** Mean $= 2.80$ mins (SD $= 1.52$, Median $= 2.50$)
- **One-Way ANOVA:** $F(3, 2996) = 402.37, p < 10^{-100}$ (Reject $H_0$)
- **Eta-Squared ($\eta^2$):** $0.287$ ($28.7\%$ of variance explained by channel)
- **Tukey HSD:** All 6 pairwise contrasts reject equality at adjusted $p < 0.001$.

![ANOVA & Tukey HSD](./visualizations/fig4_hypothesis3_anova.png)
*Figure 4: Density profiles by acquisition channel and Tukey HSD 95% confidence intervals.*

---

### Hypothesis 4: Within-Subject Customer Loyalty Intervention

- **Sample Size:** $n = 526$ repeat customers in Treatment cohort
- **Pre-Intervention Score:** Mean $= 5.70 / 10$ (SD $= 1.41$)
- **Post-Intervention Score:** Mean $= 7.05 / 10$ (SD $= 1.61$)
- **Mean Difference:** $+1.34$ points ($\text{SD}_{\text{diff}} = 0.88$, $95\%\text{ CI}: [+1.27, +1.42]$)
- **Paired $t$-Test:** $t(525) = 35.16, p = 4.26 \times 10^{-140}$ (Reject $H_0$)
- **Cohen's $d_z$:** $1.53$ (Very large within-subject effect)
- **Wilcoxon Signed-Rank:** $W = 587.5, p = 2.15 \times 10^{-77}$ (Reject $H_0$)

![Paired t-Test](./visualizations/fig5_hypothesis4_paired_ttest.png)
*Figure 5: Pre vs post customer satisfaction trajectories and empirical difference score distribution.*

---

## 🏆 Hypothesis Validation Matrix

| Hypothesis Ref. | Statistical Test Executed | Test Statistic | $p$-Value | Effect Size | Empirical Verdict | Business Action |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **$H_1$: AOV Uplift** | Welch's Two-Sample $t$-Test | $t = 3.324$ | $9.56 \times 10^{-4}$ | Cohen's $d = 0.30$ | **Reject $H_0$** | Roll out ML checkout platform-wide |
| **$H_2$: Device Independence** | Pearson $\chi^2$ Test | $\chi^2 = 20.985$ | $2.77 \times 10^{-5}$ | Cramér's $V = 0.084$ | **Reject $H_0$** | Overhaul mobile checkout UX |
| **$H_3$: Channel Duration** | One-Way ANOVA & Tukey HSD | $F = 402.37$ | $< 10^{-100}$ | $\eta^2 = 0.287$ | **Reject $H_0$** | Shift CAC budget to Email & SEO |
| **$H_4$: Loyalty Program** | Paired Samples $t$-Test | $t = 35.16$ | $4.26 \times 10^{-140}$ | Cohen's $d_z = 1.53$ | **Reject $H_0$** | Institutionalize personalized onboarding |

---

## 📂 Repository Structure

```text
week3_statistical_analysis/
├── data/
│   ├── ecommerce_ab_test_data.csv       # Curated experimental dataset (3,000 records)
│   └── statistical_test_results.json    # Full structured metrics, p-values & CIs
├── report/
│   └── Week3_Statistical_Analysis_Report.docx  # Publication-grade Word report (1.45 MB)
├── scripts/
│   ├── generate_dataset.py              # Reproducible synthetic dataset generator
│   ├── run_statistical_tests.py         # Complete inferential statistical test battery
│   └── build_word_report.py             # Formatted Word document compiler
├── visualizations/
│   ├── fig1_normality_qq_plots.png      # Normality and Q-Q distribution plots
│   ├── fig2_hypothesis1_aov_ttest.png   # AOV violin/box plot with significance
│   ├── fig3_hypothesis2_chisquare.png   # Device conversion rates & residuals heatmap
│   ├── fig4_hypothesis3_anova.png       # ANOVA density curves & Tukey HSD forest plot
│   └── fig5_hypothesis4_paired_ttest.png# Paired loyalty slopegraph & differences
├── requirements.txt                     # Scientific dependencies
├── submission_description.txt           # Portal submission description text (350+ words)
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
python scripts/generate_dataset.py

# Step 2: Run all hypothesis tests and generate figures
python scripts/run_statistical_tests.py

# Step 3: Build publication-grade Word document
python scripts/build_word_report.py
```
