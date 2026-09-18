# 📊 Data Science with Python — YuvaIntern Internship

A practical **Data Science and Advanced Python Analytics** project completed as part of my **YuvaIntern / NSDC Virtual Data Science with Python Apprentice Internship**.

This repository contains my work across multiple internship milestones, covering:

* Data Acquisition & Cleaning
* Exploratory Data Analysis (EDA)
* Advanced Data Visualization
* Statistical Analysis
* Hypothesis Testing
* Data Interpretation
* Python-based Reproducible Analysis

The project demonstrates how raw datasets can be converted into meaningful insights using Python and statistical techniques.

---

## 👨‍💻 About the Project

**Student:** Ankesh
**Internship Track:** Virtual Data Science with Python Apprentice Intern
**Domain:** Data Science & Advanced Python Analytics
**Tools:** Python, Pandas, NumPy, Matplotlib, Seaborn, SciPy, Statsmodels
**Repository:** `COVID_19_DATA_ANALYSIS`

---

# 📌 Internship Work Overview

The repository contains work from different internship weeks.

| Week       | Task                                       | Main Focus                                                         | Dataset / Domain                |
| ---------- | ------------------------------------------ | ------------------------------------------------------------------ | ------------------------------- |
| **Week 1** | Data Acquisition, Cleaning & EDA           | Data cleaning, missing values, statistics and exploratory analysis | OWID COVID-19 / Public Health   |
| **Week 2** | Advanced Data Visualization & Storytelling | Trends, comparisons, patterns and visual storytelling              | WHO COVID-19 / Public Health    |
| **Week 3** | Statistical Analysis & Hypothesis Testing  | t-tests, Chi-Square, ANOVA, paired testing and effect sizes        | E-commerce Experimental Dataset |

> **Important:** Week 1–2 focus on COVID-19 public-health data, while Week 3 uses a separate curated e-commerce experimental dataset specifically designed for statistical hypothesis testing.

---

# 🦠 Week 1 — Data Acquisition, Cleaning and Exploratory Analysis

## Objective

The first task focused on working with a large real-world dataset and performing a complete **Exploratory Data Analysis (EDA)** workflow.

The **Our World in Data (OWID) COVID-19 dataset** was selected because it contains country-level information about:

* COVID-19 cases
* COVID-19 deaths
* Vaccination
* Population
* GDP per capita
* Median age
* Life expectancy
* Human Development Index
* Healthcare indicators

The original dataset contained:

**429,435 rows × 67 columns**

For analysis, relevant columns were selected and the dataset was cleaned.

### Data Cleaning Performed

The following preprocessing steps were applied using Pandas:

1. Converted the `date` column into datetime format.
2. Checked for duplicate records.
3. Removed aggregate entries such as continent-level records.
4. Filled missing daily case/death flow values appropriately.
5. Forward-filled cumulative metrics within each country.
6. Forward-filled/backward-filled static country attributes.
7. Handled vaccination-related missing values.
8. Prepared the cleaned dataset for further analysis.

Final cleaned dataset:

**402,910 rows × 19 columns**

### Exploratory Analysis

The analysis included:

* Missing-value analysis
* Summary statistics
* COVID-19 case trends
* Correlation analysis
* GDP vs vaccination coverage analysis

### Main Insights

Some important patterns identified during EDA included:

* Median age showed a strong relationship with reported COVID-19 mortality.
* HDI showed moderate relationships with mortality and vaccination coverage.
* Higher-income countries generally showed higher reported vaccination coverage.
* Major COVID-19 waves occurred at different times across countries.
* Vaccination and healthcare-related variables contained substantial missing data.

---

# 📈 Week 2 — Advanced Data Visualization & Storytelling

## Objective

The second task focused on transforming COVID-19 data into a **visual story** rather than only presenting numerical statistics.

The analysis used WHO COVID-19 datasets covering cases, deaths, vaccination, age-specific deaths, mortality and hospitalization.

The Week 2 report contains seven main visual analyses.

### Visualizations Created

#### 1. Global COVID-19 Cases and Deaths

A time-series visualization was created to study the global pattern of reported COVID-19 cases and deaths.

#### 2. COVID-19 Waves Across Countries

Five major countries were compared:

* India
* United States
* Brazil
* United Kingdom
* Germany

A rolling average was used to make major waves easier to observe.

#### 3. Vaccination Progress

The vaccination dataset was analyzed to understand how reported primary-series vaccination coverage changed during the rollout period.

#### 4. Country Vaccination Comparison

The latest available vaccination coverage of selected countries was compared using a horizontal bar chart.

#### 5. Age-Specific Deaths

Reported COVID-19 deaths were grouped by age to understand which age categories contributed the largest number of reported deaths.

#### 6. Mortality Comparison

Countries with comparatively high reported COVID-19 deaths per 100,000 population were identified.

#### 7. Healthcare Pressure

Reported COVID-19 hospitalizations were analyzed over time for selected countries.

The Week 2 Python workflow generates these seven visualization outputs from the WHO datasets.

### Key Story

The visual analysis showed that the pandemic did not follow exactly the same pattern in every country. Different countries experienced major reported waves at different times, while vaccination progress and healthcare pressure also varied across regions.

---

# 🧪 Week 3 — Statistical Analysis & Hypothesis Testing

## Objective

Week 3 moved from **descriptive analysis to inferential statistics**.

Instead of only asking:

> "What does the data look like?"

the analysis asks:

> **"Is the observed difference or relationship statistically significant?"**

A curated experimental dataset containing **3,000 user sessions** was used for this task. The dataset contains control/treatment information, conversion status, device category, marketing channel, session duration and customer loyalty scores.

### Statistical Significance

All hypothesis tests used:

**Significance level (α) = 0.05**

and a

**95% Confidence Interval**

framework.

---

# 🎯 Hypotheses Tested

Four hypotheses were formulated.

| Hypothesis          | Question                                                           | Statistical Test                |
| ------------------- | ------------------------------------------------------------------ | ------------------------------- |
| **H1 — Revenue**    | Does the treatment checkout experience change Average Order Value? | Welch's t-test + Mann-Whitney U |
| **H2 — Conversion** | Is conversion dependent on device category?                        | Pearson Chi-Square              |
| **H3 — Engagement** | Does marketing channel affect session duration?                    | One-Way ANOVA + Tukey HSD       |
| **H4 — Retention**  | Does personalized onboarding change loyalty scores?                | Paired t-test + Wilcoxon        |

The formal null and alternative hypotheses are documented in the Week 3 report.

---

# 🔬 Statistical Methodology

Before interpreting the statistical tests, several diagnostic procedures were applied.

### 1. Normality Testing

Used:

* Shapiro-Wilk test
* D'Agostino-Pearson test
* Q-Q plots

### 2. Variance Testing

**Levene's test** was used to examine variance homogeneity.

### 3. Robust Testing

Where appropriate, **Welch's t-test** was used instead of assuming equal variances.

### 4. Non-Parametric Validation

Non-parametric alternatives were also used:

* Mann-Whitney U
* Wilcoxon Signed-Rank

### 5. Multiple Comparisons

**Tukey's HSD** was used after ANOVA to compare individual marketing-channel pairs.

### 6. Effect Sizes

Statistical significance was supported with practical effect-size measures:

* Cohen's d
* Cohen's dz
* Cramér's V
* Eta-Squared (η²)

These diagnostic and effect-size procedures are part of the Week 3 methodology.

---

# 📊 Week 3 Results

## H1 — Average Order Value

The Treatment group had a higher mean AOV than the Control group.

| Group     | Mean AOV |
| --------- | -------: |
| Control   |   $85.46 |
| Treatment |   $92.01 |

Mean difference:

**+$6.55**

Welch's t-test:

**t(472.4) = 3.324**

**p = 9.56 × 10⁻⁴**

Cohen's d:

**0.298**

95% Confidence Interval:

**[$2.68, $10.42]**

Since the p-value is below 0.05, the null hypothesis was rejected. The Mann-Whitney U test also supported the result.

### Interpretation

The Treatment group showed a statistically significant increase in Average Order Value compared with the Control group.

---

## H2 — Device Category and Conversion

Conversion rates were compared across:

* Desktop
* Mobile
* Tablet

| Device  | Conversion Rate |
| ------- | --------------: |
| Desktop |          20.06% |
| Mobile  |          13.68% |
| Tablet  |          19.38% |

Pearson Chi-Square:

**χ²(2) = 20.985**

**p = 2.77 × 10⁻⁵**

Cramér's V:

**0.084**

The null hypothesis of independence was rejected.

### Interpretation

The analysis indicates that conversion behavior was statistically associated with device category, with mobile users showing a lower observed conversion rate than desktop users.

---

## H3 — Marketing Channel and Session Duration

Four acquisition channels were compared:

| Channel        | Mean Session Duration |
| -------------- | --------------------: |
| Email          |              6.71 min |
| Organic Search |              5.54 min |
| Paid Search    |              3.89 min |
| Social Media   |              2.80 min |

One-Way ANOVA:

**F(3, 2996) = 402.37**

**p < 10⁻¹⁰⁰**

Eta-Squared:

**η² = 0.287**

Tukey's HSD found all six pairwise channel comparisons statistically significant at adjusted p < 0.001.

### Interpretation

Session duration differed significantly across acquisition channels, with Email and Organic Search showing the highest average session durations.

---

## H4 — Customer Loyalty Before and After Intervention

A paired analysis was conducted on **526 repeat customers**.

| Measurement         | Mean Score |
| ------------------- | ---------: |
| Before Intervention |  5.70 / 10 |
| After Intervention  |  7.05 / 10 |

Mean improvement:

**+1.34 points**

95% CI:

**[+1.27, +1.42]**

Paired t-test:

**t(525) = 35.16**

**p = 4.26 × 10⁻¹⁴⁰**

Cohen's dz:

**1.53**

The Wilcoxon Signed-Rank test also supported the result.

### Interpretation

The post-intervention loyalty scores were significantly higher than the pre-intervention scores in this sample.

---

# 🏆 Hypothesis Validation Summary

| Hypothesis       | Test           |   p-value | Effect Size | Decision      |
| ---------------- | -------------- | --------: | ----------: | ------------- |
| **H1 — AOV**     | Welch's t-test |  9.56e-04 |    d = 0.30 | **Reject H₀** |
| **H2 — Device**  | Chi-Square     |  2.77e-05 |   V = 0.084 | **Reject H₀** |
| **H3 — Channel** | ANOVA          |  < 1e-100 |  η² = 0.287 | **Reject H₀** |
| **H4 — Loyalty** | Paired t-test  | 4.26e-140 |   dz = 1.53 | **Reject H₀** |

All four hypotheses produced statistically significant results at **α = 0.05**.

---

# 🖼️ Week 3 Visualizations

The statistical analysis is supported by five major visualizations:

1. **Normality and Q-Q plots**
2. **AOV Control vs Treatment**
3. **Device Conversion and Chi-Square Analysis**
4. **ANOVA and Tukey HSD**
5. **Pre vs Post Loyalty Analysis**

These visualizations help connect the numerical test results with the underlying distributions and group differences.

---

# 🛠️ Technologies Used

### Programming

* Python 3
* Pandas
* NumPy

### Visualization

* Matplotlib
* Seaborn

### Statistical Analysis

* SciPy
* Statsmodels

### Documentation

* Microsoft Word
* Markdown
* GitHub

---

# 📂 Repository Structure

```text
COVID_19_DATA_ANALYSIS/
│
├── README.md
├── requirements.txt
│
├── Week_1_Data Acquisition, Cleaning, and Exploratory Analysis.python
├── Week2 Python code .py
│
├── Week1_Data_Analysis_Report_humanized.docx
├── Week2_Advanced_COVID_Data_Storytelling_Report_FINAL.docx
│
├── Week3_Statistical_Analysis_Report.docx
├── run_statistical_tests.py
├── generate_dataset.py
├── build_word_report.py
├── ecommerce_ab_test_data.csv
├── statistical_test_results.json
├── submission_description.txt
│
├── fig1_normality_qq_plots.png
├── fig2_hypothesis1_aov_ttest.png
├── fig3_hypothesis2_chisquare.png
├── fig4_hypothesis3_anova.png
└── fig5_hypothesis4_paired_ttest.png
```

The repository currently contains the Week 1/2 COVID analysis material along with the Week 3 statistical-analysis files and generated visualizations.

---

# ▶️ How to Run the Project

## 1. Clone the Repository

```bash
git clone https://github.com/ankesh825/COVID_19_DATA_ANALYSIS.git
cd COVID_19_DATA_ANALYSIS
```

## 2. Install Required Libraries

```bash
pip install -r requirements.txt
```

## 3. Run Week 1

```bash
python "Week_1_Data Acquisition, Cleaning, and Exploratory Analysis.python"
```

## 4. Run Week 2

```bash
python "Week2 Python code .py"
```

## 5. Run Week 3 Statistical Analysis

```bash
python run_statistical_tests.py
```

If the dataset needs to be regenerated:

```bash
python generate_dataset.py
```

The Week 3 workflow also includes a script for building the Word report:

```bash
python build_word_report.py
```

---

# 📚 Key Statistical Concepts Used

### Hypothesis Testing

A statistical method used to determine whether the observed evidence is strong enough to reject a null hypothesis.

### Null Hypothesis (H₀)

The default assumption that there is no statistically significant difference or relationship.

### Alternative Hypothesis (H₁)

The hypothesis that a statistically significant difference or relationship exists.

### p-value

The probability of observing results at least as extreme as those found, assuming the null hypothesis is true.

### Confidence Interval

A range used to estimate the plausible values of a population parameter.

### Effect Size

Measures the practical magnitude of an observed difference or relationship.

### Type I Error

Rejecting a true null hypothesis.

### Type II Error

Failing to reject a false null hypothesis.

---

# ⚠️ Limitations

The analysis should be interpreted within the limitations of the datasets and study design.

### Week 1–2

COVID-19 reporting differs between countries because of differences in:

* Testing capacity
* Reporting systems
* Healthcare infrastructure
* Vaccination reporting
* Data completeness

Therefore, reported values should not automatically be interpreted as the exact true number of infections or deaths.

### Week 3

The Week 3 dataset is a curated experimental dataset used for statistical-analysis practice.

Statistical significance does not automatically mean that an effect is large or practically important. This is why effect sizes and confidence intervals were included.

---

# 🎓 Learning Outcomes

Through these tasks, I developed practical experience in:

* Collecting real-world datasets
* Cleaning large datasets with Pandas
* Handling missing values
* Performing EDA
* Creating meaningful visualizations
* Finding trends and patterns
* Formulating statistical hypotheses
* Selecting appropriate statistical tests
* Understanding p-values
* Calculating confidence intervals
* Measuring effect sizes
* Performing post-hoc analysis
* Interpreting statistical results
* Creating reproducible Python workflows
* Documenting Data Science projects professionally

---

# 📌 Internship Progress

```text
Week 1
Data Acquisition
       ↓
Data Cleaning
       ↓
Exploratory Data Analysis
       ↓
Week 2
Advanced Visualization
       ↓
Data Storytelling
       ↓
Public-Health Insights
       ↓
Week 3
Hypothesis Formulation
       ↓
Statistical Testing
       ↓
p-values + Confidence Intervals
       ↓
Effect Size Analysis
       ↓
Statistical Conclusions
```

---

# 📖 References

### Week 1

**Our World in Data — COVID-19 Dataset**

https://github.com/owid/covid-19-data

**COVID-19 Pandemic Background**

https://en.wikipedia.org/wiki/COVID-19_pandemic

### Week 2

WHO COVID-19 global datasets were used for reported cases, deaths, vaccination, age-specific mortality and hospitalization analysis.

### Week 3

Python scientific computing ecosystem:

* Pandas
* NumPy
* SciPy
* Statsmodels
* Matplotlib
* Seaborn

---

# 👨‍💻 Author

**Ankesh**

Data Science & Python Analytics Intern

GitHub:
https://github.com/ankesh825

---

## ⭐ Project Summary

This repository represents my progression from **raw data to statistical evidence**.

The first stage focused on acquiring and cleaning data, the second stage focused on communicating patterns through visualization, and the third stage focused on determining whether observed differences were statistically significant.

Together, these tasks demonstrate an end-to-end Data Science workflow:

**Data → Cleaning → EDA → Visualization → Hypothesis → Statistical Testing → Interpretation → Insights**

---
