"""
run_statistical_tests.py
Executes rigorous hypothesis testing battery, assumption tests, effect size calculations,
and generates publication-quality figures for the statistical report.
"""

import os
import json
import numpy as np
import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib.pyplot as plt
import seaborn as sns

# Set visual styling for publication-grade charts
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

def run_analysis(data_path, vis_dir, results_json_path):
    os.makedirs(vis_dir, exist_ok=True)
    df = pd.read_csv(data_path)
    results = {}
    
    # -------------------------------------------------------------
    # 0. Dataset Overview & EDA
    # -------------------------------------------------------------
    eda = {
        'total_records': len(df),
        'control_n': int((df['group'] == 'Control').sum()),
        'treatment_n': int((df['group'] == 'Treatment').sum()),
        'overall_conversion_rate': float(df['converted'].mean()),
        'control_conversion_rate': float(df[df['group'] == 'Control']['converted'].mean()),
        'treatment_conversion_rate': float(df[df['group'] == 'Treatment']['converted'].mean()),
        'device_breakdown': df['device_category'].value_counts().to_dict(),
        'channel_breakdown': df['marketing_channel'].value_counts().to_dict()
    }
    results['eda'] = eda
    
    # -------------------------------------------------------------
    # 1. HYPOTHESIS 1: Two-Sample t-Test on Average Order Value (AOV)
    # -------------------------------------------------------------
    conv_df = df[df['converted'] == 1].dropna(subset=['order_value_usd'])
    ctrl_aov = conv_df[conv_df['group'] == 'Control']['order_value_usd']
    trt_aov = conv_df[conv_df['group'] == 'Treatment']['order_value_usd']
    
    # Descriptive stats
    h1_desc = {
        'control_n': len(ctrl_aov),
        'control_mean': float(np.mean(ctrl_aov)),
        'control_std': float(np.std(ctrl_aov, ddof=1)),
        'control_median': float(np.median(ctrl_aov)),
        'control_iqr': float(stats.iqr(ctrl_aov)),
        'treatment_n': len(trt_aov),
        'treatment_mean': float(np.mean(trt_aov)),
        'treatment_std': float(np.std(trt_aov, ddof=1)),
        'treatment_median': float(np.median(trt_aov)),
        'treatment_iqr': float(stats.iqr(trt_aov)),
    }
    
    # Assumption 1: Normality (Shapiro-Wilk)
    shapiro_ctrl_stat, shapiro_ctrl_p = stats.shapiro(ctrl_aov)
    shapiro_trt_stat, shapiro_trt_p = stats.shapiro(trt_aov)
    
    # Assumption 2: Homoscedasticity (Levene's test)
    levene_stat, levene_p = stats.levene(ctrl_aov, trt_aov, center='median')
    
    # Inferential Tests: Independent Student's and Welch's t-test
    t_stat_welch, p_val_welch = stats.ttest_ind(trt_aov, ctrl_aov, equal_var=False)
    t_stat_stud, p_val_stud = stats.ttest_ind(trt_aov, ctrl_aov, equal_var=True)
    
    # Welch-Satterthwaite degrees of freedom
    s1, s2 = np.var(trt_aov, ddof=1), np.var(ctrl_aov, ddof=1)
    n1, n2 = len(trt_aov), len(ctrl_aov)
    df_welch = ((s1/n1 + s2/n2)**2) / (((s1/n1)**2)/(n1 - 1) + ((s2/n2)**2)/(n2 - 1))
    
    # 95% Confidence Interval for Difference in Means (Treatment - Control)
    mean_diff = h1_desc['treatment_mean'] - h1_desc['control_mean']
    se_diff = np.sqrt(s1/n1 + s2/n2)
    t_crit = stats.t.ppf(0.975, df=df_welch)
    ci_lower = mean_diff - t_crit * se_diff
    ci_upper = mean_diff + t_crit * se_diff
    
    # Effect Size: Cohen's d
    pooled_sd = np.sqrt(((n1 - 1) * s1 + (n2 - 1) * s2) / (n1 + n2 - 2))
    cohen_d = mean_diff / pooled_sd
    
    # Non-parametric check: Mann-Whitney U test
    mwu_stat, mwu_p = stats.mannwhitneyu(trt_aov, ctrl_aov, alternative='two-sided')
    
    results['hypothesis_1'] = {
        'descriptives': h1_desc,
        'diagnostics': {
            'shapiro_control': {'stat': float(shapiro_ctrl_stat), 'p_value': float(shapiro_ctrl_p)},
            'shapiro_treatment': {'stat': float(shapiro_trt_stat), 'p_value': float(shapiro_trt_p)},
            'levene_test': {'stat': float(levene_stat), 'p_value': float(levene_p)}
        },
        'welch_ttest': {
            't_stat': float(t_stat_welch),
            'df': float(df_welch),
            'p_value_twotailed': float(p_val_welch),
            'p_value_onetailed': float(p_val_welch / 2 if t_stat_welch > 0 else 1 - p_val_welch / 2),
            'mean_diff': float(mean_diff),
            'se_diff': float(se_diff),
            'ci_95': [float(ci_lower), float(ci_upper)],
            'cohen_d': float(cohen_d)
        },
        'mann_whitney': {
            'u_stat': float(mwu_stat),
            'p_value': float(mwu_p)
        }
    }
    
    # Visualizations for Hypothesis 1
    # Figure 1: Q-Q Plots and Normality Histograms
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    sns.histplot(ctrl_aov, kde=True, ax=axes[0, 0], color="#2b5c8f", bins=20)
    axes[0, 0].set_title("Control AOV Distribution (Histogram & KDE)", fontsize=12, fontweight='bold')
    axes[0, 0].set_xlabel("Order Value ($)")
    axes[0, 0].set_ylabel("Frequency")
    
    sm.qqplot(ctrl_aov, line='s', ax=axes[0, 1])
    axes[0, 1].set_title("Control Group Q-Q Plot", fontsize=12, fontweight='bold')
    axes[0, 1].get_lines()[0].set_color("#2b5c8f")
    axes[0, 1].get_lines()[1].set_color("#d9534f")
    
    sns.histplot(trt_aov, kde=True, ax=axes[1, 0], color="#2ca02c", bins=20)
    axes[1, 0].set_title("Treatment AOV Distribution (Histogram & KDE)", fontsize=12, fontweight='bold')
    axes[1, 0].set_xlabel("Order Value ($)")
    axes[1, 0].set_ylabel("Frequency")
    
    sm.qqplot(trt_aov, line='s', ax=axes[1, 1])
    axes[1, 1].set_title("Treatment Group Q-Q Plot", fontsize=12, fontweight='bold')
    axes[1, 1].get_lines()[0].set_color("#2ca02c")
    axes[1, 1].get_lines()[1].set_color("#d9534f")
    
    plt.tight_layout()
    fig1_path = os.path.join(vis_dir, "fig1_normality_qq_plots.png")
    plt.savefig(fig1_path, dpi=300)
    plt.close()
    
    # Figure 2: Hypothesis 1 Comparison (Violin & Box Plot with Statistical Annotations)
    fig, ax = plt.subplots(figsize=(8, 6))
    palette = {"Control": "#4A90E2", "Treatment": "#50E3C2"}
    sns.violinplot(x="group", y="order_value_usd", data=conv_df, ax=ax, palette=palette, inner=None, alpha=0.3)
    sns.boxplot(x="group", y="order_value_usd", data=conv_df, ax=ax, width=0.25, boxprops=dict(alpha=0.9), 
                palette=palette, showmeans=True, meanprops={"marker":"o", "markerfacecolor":"white", "markeredgecolor":"black"})
    
    # Statistical significance bracket
    y_max = max(conv_df['order_value_usd']) + 5
    ax.plot([0, 0, 1, 1], [y_max, y_max + 3, y_max + 3, y_max], lw=1.5, c='black')
    sig_text = f"t = {t_stat_welch:.3f}, p = {p_val_welch:.2e} (Cohen's d = {cohen_d:.2f}) ***"
    ax.text(0.5, y_max + 4.5, sig_text, ha='center', va='bottom', fontsize=11, fontweight='bold', color='#B22222')
    
    ax.set_title("Average Order Value (AOV): Control vs Treatment\nWelch's Two-Sample t-Test Validation", fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel("Experiment Cohort", fontsize=11, fontweight='bold')
    ax.set_ylabel("Order Value ($ USD)", fontsize=11, fontweight='bold')
    ax.set_ylim(0, y_max + 15)
    plt.tight_layout()
    fig2_path = os.path.join(vis_dir, "fig2_hypothesis1_aov_ttest.png")
    plt.savefig(fig2_path, dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # 2. HYPOTHESIS 2: Chi-Square Test of Independence (Device vs Conversion)
    # -------------------------------------------------------------
    contingency = pd.crosstab(df['device_category'], df['converted'])
    contingency.columns = ['Abandoned', 'Converted']
    
    chi2, chi_p, dof, expected = stats.chi2_contingency(contingency)
    
    # Cramér's V
    n_obs = contingency.to_numpy().sum()
    min_dim = min(contingency.shape) - 1
    cramers_v = np.sqrt(chi2 / (n_obs * min_dim))
    
    # Standardized residuals: (Observed - Expected) / sqrt(Expected)
    std_residuals = (contingency.to_numpy() - expected) / np.sqrt(expected)
    res_df = pd.DataFrame(std_residuals, index=contingency.index, columns=contingency.columns)
    
    # Conversion rates by device
    rates_by_device = df.groupby('device_category')['converted'].agg(['count', 'mean']).reset_index()
    rates_by_device['conversion_pct'] = rates_by_device['mean'] * 100
    
    results['hypothesis_2'] = {
        'contingency_observed': contingency.to_dict(),
        'contingency_expected': pd.DataFrame(expected, index=contingency.index, columns=contingency.columns).round(2).to_dict(),
        'chi2_stat': float(chi2),
        'dof': int(dof),
        'p_value': float(chi_p),
        'cramers_v': float(cramers_v),
        'std_residuals': res_df.round(3).to_dict(),
        'device_rates': rates_by_device.to_dict(orient='records')
    }
    
    # Figure 3: Conversion Rates by Device & Residuals Heatmap
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Barplot of rates
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    sns.barplot(data=rates_by_device, x='device_category', y='conversion_pct', ax=ax1, palette='Blues_r', edgecolor='black')
    for p in ax1.patches:
        ax1.annotate(f"{p.get_height():.2f}%", 
                     (p.get_x() + p.get_width() / 2., p.get_height() / 2),
                     ha='center', va='center', fontsize=11, color='white', fontweight='bold')
    ax1.set_title("Conversion Rate (%) by Device Category", fontsize=12, fontweight='bold')
    ax1.set_xlabel("Device Category", fontsize=11)
    ax1.set_ylabel("Conversion Rate (%)", fontsize=11)
    ax1.set_ylim(0, max(rates_by_device['conversion_pct']) * 1.3)
    
    # Heatmap of standardized residuals
    sns.heatmap(res_df, annot=True, fmt=".2f", cmap="vlag", center=0, cbar=True, ax=ax2, linewidths=1)
    ax2.set_title(f"Standardized Pearson Residuals (χ² = {chi2:.2f}, p = {chi_p:.2e})", fontsize=12, fontweight='bold')
    ax2.set_ylabel("Device Category", fontsize=11)
    
    plt.tight_layout()
    fig3_path = os.path.join(vis_dir, "fig3_hypothesis2_chisquare.png")
    plt.savefig(fig3_path, dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # 3. HYPOTHESIS 3: One-Way ANOVA & Tukey HSD (Channel vs Session Duration)
    # -------------------------------------------------------------
    channels = df['marketing_channel'].unique()
    channel_groups = [df[df['marketing_channel'] == ch]['session_duration_mins'] for ch in channels]
    
    # Levene's test for homoscedasticity
    levene_ch_stat, levene_ch_p = stats.levene(*channel_groups)
    
    # One-Way ANOVA F-test
    f_stat, anova_p = stats.f_oneway(*channel_groups)
    
    # OLS Model summary for Sum of Squares and Eta-squared
    model = ols('session_duration_mins ~ C(marketing_channel)', data=df).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    ss_treatment = anova_table.loc['C(marketing_channel)', 'sum_sq']
    ss_residual = anova_table.loc['Residual', 'sum_sq']
    ss_total = ss_treatment + ss_residual
    eta_squared = ss_treatment / ss_total
    
    # Tukey's HSD Post-Hoc Test
    tukey = pairwise_tukeyhsd(endog=df['session_duration_mins'], groups=df['marketing_channel'], alpha=0.05)
    tukey_summary = []
    for row in tukey.summary().data[1:]:
        tukey_summary.append({
            'group1': str(row[0]),
            'group2': str(row[1]),
            'meandiff': float(row[2]),
            'p_adj': float(row[3]),
            'lower': float(row[4]),
            'upper': float(row[5]),
            'reject': bool(row[6])
        })
        
    results['hypothesis_3'] = {
        'levene_homoscedasticity': {'stat': float(levene_ch_stat), 'p_value': float(levene_ch_p)},
        'f_statistic': float(f_stat),
        'df_between': int(anova_table.loc['C(marketing_channel)', 'df']),
        'df_within': int(anova_table.loc['Residual', 'df']),
        'p_value': float(anova_p),
        'eta_squared': float(eta_squared),
        'channel_descriptives': df.groupby('marketing_channel')['session_duration_mins'].agg(
            ['count', 'mean', 'std', 'median', lambda x: stats.iqr(x)]
        ).rename(columns={'<lambda_0>': 'iqr'}).round(3).to_dict(orient='index'),
        'tukey_hsd': tukey_summary
    }
    
    # Figure 4: ANOVA Density & Tukey HSD Forest Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # KDE distribution plot
    palette_ch = {'Organic Search': '#2ca02c', 'Paid Search': '#ff7f0e', 
                  'Social Media': '#1f77b4', 'Email Campaign': '#d62728'}
    sns.kdeplot(data=df, x='session_duration_mins', hue='marketing_channel', common_norm=False, 
                fill=True, alpha=0.25, palette=palette_ch, ax=ax1, lw=2)
    ax1.set_title("Session Duration Distribution by Marketing Channel", fontsize=12, fontweight='bold')
    ax1.set_xlabel("Session Duration (Minutes)", fontsize=11)
    ax1.set_ylabel("Density", fontsize=11)
    
    # Tukey HSD Confidence Intervals Plot
    comparisons = [f"{t['group1']} vs {t['group2']}" for t in tukey_summary]
    diffs = [t['meandiff'] for t in tukey_summary]
    ci_lows = [t['lower'] for t in tukey_summary]
    ci_highs = [t['upper'] for t in tukey_summary]
    rejects = [t['reject'] for t in tukey_summary]
    
    y_pos = np.arange(len(comparisons))
    for idx in range(len(comparisons)):
        color = '#d9534f' if rejects[idx] else '#2b5c8f'
        ax2.errorbar(diffs[idx], idx, xerr=[[diffs[idx] - ci_lows[idx]], [ci_highs[idx] - diffs[idx]]],
                     fmt='o', color=color, ecolor=color, elinewidth=2, capsize=5, capthick=1.5, markersize=7)
    ax2.axvline(0, color='gray', linestyle='--', lw=1.2)
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(comparisons, fontsize=10)
    ax2.set_title(f"Tukey's HSD 95% CIs (ANOVA F = {f_stat:.2f}, p = {anova_p:.2e}, η² = {eta_squared:.2f})", 
                  fontsize=12, fontweight='bold')
    ax2.set_xlabel("Difference in Mean Duration (Minutes)", fontsize=11)
    
    plt.tight_layout()
    fig4_path = os.path.join(vis_dir, "fig4_hypothesis3_anova.png")
    plt.savefig(fig4_path, dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # 4. HYPOTHESIS 4: Paired Samples t-Test (Pre vs Post Loyalty Score)
    # -------------------------------------------------------------
    # Evaluate Treatment repeat customers
    paired_df = df[(df['group'] == 'Treatment') & (df['pre_loyalty_score'].notna())].copy()
    pre_scores = paired_df['pre_loyalty_score']
    post_scores = paired_df['post_loyalty_score']
    diff_scores = post_scores - pre_scores
    
    # Normality of differences
    shapiro_diff_stat, shapiro_diff_p = stats.shapiro(diff_scores)
    
    # Paired t-test
    paired_t_stat, paired_p_val = stats.ttest_rel(post_scores, pre_scores)
    
    # Confidence Interval for paired difference
    n_paired = len(diff_scores)
    mean_paired_diff = float(np.mean(diff_scores))
    std_paired_diff = float(np.std(diff_scores, ddof=1))
    se_paired_diff = std_paired_diff / np.sqrt(n_paired)
    t_crit_paired = stats.t.ppf(0.975, df=n_paired - 1)
    paired_ci_lower = mean_paired_diff - t_crit_paired * se_paired_diff
    paired_ci_upper = mean_paired_diff + t_crit_paired * se_paired_diff
    
    # Cohen's d_z for paired samples
    cohen_dz = mean_paired_diff / std_paired_diff
    
    # Wilcoxon Signed-Rank Test (Non-parametric)
    wilcoxon_stat, wilcoxon_p = stats.wilcoxon(post_scores, pre_scores, alternative='two-sided')
    
    results['hypothesis_4'] = {
        'sample_size_n': int(n_paired),
        'pre_score_mean': float(np.mean(pre_scores)),
        'pre_score_std': float(np.std(pre_scores, ddof=1)),
        'post_score_mean': float(np.mean(post_scores)),
        'post_score_std': float(np.std(post_scores, ddof=1)),
        'mean_difference': float(mean_paired_diff),
        'std_difference': float(std_paired_diff),
        'se_difference': float(se_paired_diff),
        'shapiro_normality_diff': {'stat': float(shapiro_diff_stat), 'p_value': float(shapiro_diff_p)},
        'paired_ttest': {
            't_stat': float(paired_t_stat),
            'df': int(n_paired - 1),
            'p_value': float(paired_p_val),
            'ci_95': [float(paired_ci_lower), float(paired_ci_upper)],
            'cohen_dz': float(cohen_dz)
        },
        'wilcoxon_test': {
            'w_stat': float(wilcoxon_stat),
            'p_value': float(wilcoxon_p)
        }
    }
    
    # Figure 5: Paired Loyalty Scores Pre vs Post
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    
    # Pre vs Post Score Means with Error Bars and Individual Trajectories (subsample of 40)
    sample_sub = paired_df.sample(min(45, len(paired_df)), random_state=42)
    for _, row in sample_sub.iterrows():
        ax1.plot([0, 1], [row['pre_loyalty_score'], row['post_loyalty_score']], color='#999999', alpha=0.35, lw=1)
    
    means = [np.mean(pre_scores), np.mean(post_scores)]
    stds = [np.std(pre_scores, ddof=1) / np.sqrt(n_paired), np.std(post_scores, ddof=1) / np.sqrt(n_paired)]
    ax1.errorbar([0, 1], means, yerr=stds, fmt='o-', color='#e74c3c', lw=3, markersize=9, capsize=6, label='Cohort Mean ± SE')
    ax1.set_xticks([0, 1])
    ax1.set_xticklabels(['Pre-Intervention', 'Post-Intervention'], fontsize=11, fontweight='bold')
    ax1.set_ylabel("Loyalty / Satisfaction Score (1-10)", fontsize=11)
    ax1.set_title("Customer Loyalty Scores Before vs After Intervention", fontsize=12, fontweight='bold')
    ax1.set_ylim(1, 10.5)
    ax1.legend(loc='upper left')
    
    # Histogram of Pairwise Differences
    sns.histplot(diff_scores, kde=True, discrete=True, color='#3498db', ax=ax2, edgecolor='black')
    ax2.axvline(0, color='red', linestyle='--', lw=1.5, label='Null Mean (0)')
    ax2.axvline(mean_paired_diff, color='green', linestyle='-', lw=2, label=f'Sample Mean ({mean_paired_diff:+.2f})')
    ax2.set_title(f"Distribution of Within-Subject Differences\n(t = {paired_t_stat:.2f}, p = {paired_p_val:.2e}, Cohen's dz = {cohen_dz:.2f})", 
                  fontsize=12, fontweight='bold')
    ax2.set_xlabel("Difference Score (Post - Pre)", fontsize=11)
    ax2.set_ylabel("Count of Repeat Customers", fontsize=11)
    ax2.legend(loc='upper right')
    
    plt.tight_layout()
    fig5_path = os.path.join(vis_dir, "fig5_hypothesis4_paired_ttest.png")
    plt.savefig(fig5_path, dpi=300)
    plt.close()
    
    # Save structured results to JSON
    with open(results_json_path, 'w') as f:
        json.dump(results, f, indent=4)
        
    print(f"Statistical tests completed successfully! Results written to {results_json_path}")
    print(f"Figures saved in: {vis_dir}")
    return results

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, ".."))
    data_file = os.path.join(project_root, "data", "ecommerce_ab_test_data.csv")
    vis_folder = os.path.join(project_root, "visualizations")
    res_file = os.path.join(project_root, "data", "statistical_test_results.json")
    
    res = run_analysis(data_file, vis_folder, res_file)
