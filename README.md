# COVID-19 Data Analysis – Week 1 & Week 2

## Project Overview

This repository contains my COVID-19 Data Analysis work completed during Week 1 and Week 2 of the Data Science with Python Internship.

The project uses real-world COVID-19 public-health data to perform data acquisition, cleaning, exploratory analysis, advanced visualization, and data storytelling using Python.

---

# Week 1 – Data Acquisition, Cleaning and Exploratory Analysis

## Dataset

**Our World in Data (OWID) – COVID-19 Dataset**

The dataset contains COVID-19 cases, deaths, vaccination data, and socio-economic indicators for countries around the world.

## Week 1 Work

### 1. Data Acquisition
- Loaded the OWID COVID-19 dataset using Pandas.
- Selected 19 relevant columns for analysis.
- Removed continent-level aggregate rows and kept individual countries.

### 2. Data Cleaning
- Converted date values into datetime format.
- Checked and removed duplicate rows.
- Handled missing values in daily case and death data.
- Forward-filled cumulative case and death values by country.
- Forward-filled vaccination data.
- Handled missing socio-economic indicators using country-level values.
- Saved the cleaned dataset as `cleaned_covid_data.csv`.

### 3. Exploratory Data Analysis

The Week 1 analysis includes:

- Summary statistics
- Missing-value analysis
- COVID-19 case trend analysis
- Correlation analysis
- GDP per capita vs vaccination coverage

### Week 1 Visualizations

1. Missing Data by Column
2. COVID-19 New Cases Trend – Selected Countries
3. Correlation Heatmap
4. GDP per Capita vs Full Vaccination Rate

---

# Week 2 – Advanced Data Visualization and Storytelling

Week 2 builds on the data-analysis workflow and focuses on advanced visualization and storytelling.

## Week 2 Visualizations

1. Global COVID-19 Cases and Deaths
2. COVID-19 Waves Across Five Major Countries
3. Reported Primary-Series Vaccination Coverage
4. Country Vaccination Comparison
5. Reported COVID-19 Deaths by Age Group
6. Reported COVID-19 Deaths per 100,000 Population
7. Reported New COVID-19 Hospitalizations

---

# Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook

---

# Project Files

## Week 1

- Week 1 Python code
- Week 1 analysis report
- COVID-19 dataset
- Cleaned dataset
- Summary statistics
- Generated visualizations

## Week 2

- Week 2 Python code
- Week 2 analysis report
- COVID-19 datasets
- Generated visualizations

---

# Key Analysis Areas

The project analyzes:

- COVID-19 cases
- COVID-19 deaths
- Pandemic waves
- Vaccination coverage
- Age-specific mortality
- Deaths per 100,000 population
- Hospitalizations
- Missing data
- Socio-economic factors
- GDP and vaccination relationships

---

# Objective

The objective of this project is to develop practical skills in Python-based data analysis and visualization and to communicate meaningful insights from real-world COVID-19 public-health data.

---

# Data Source

The Week 1 COVID-19 dataset and analysis are available in my GitHub repository:

[ankesh825/COVID_19_DATA_ANALYSIS: COVID-19 data cleaning & EDA using Python — Week 1 of 5-week Data Science Internship](https://github.com/ankesh825/COVID_19_DATA_ANALYSIS)
