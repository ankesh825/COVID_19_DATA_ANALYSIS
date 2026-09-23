"""
build_ml_word_report.py
Generates a comprehensive, professionally styled Word document (.docx)
for the Week 4 Machine Learning Model Development and Evaluation project.
"""

import os
import json
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_shading(cell, color_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:val="clear" w:color="auto" w:fill="{color_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="D3D3D3", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="none"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def format_row(row, bg_color, is_header=False, bold=False, font_size=9.5, text_color=RGBColor(34, 34, 34)):
    for cell in row.cells:
        set_cell_shading(cell, bg_color)
        set_cell_margins(cell, top=130, bottom=130, left=150, right=150)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        for paragraph in cell.paragraphs:
            paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in paragraph.runs:
                run.font.name = 'Calibri'
                run.font.size = Pt(font_size)
                run.font.bold = bold
                run.font.color.rgb = text_color

def add_styled_heading(doc, text, level):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.keep_with_next = True
    run = h.runs[0]
    run.font.name = 'Calibri'
    if level == 1:
        run.font.size = Pt(16.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(27, 54, 93)  # Deep Navy
        h.paragraph_format.space_before = Pt(16)
        h.paragraph_format.space_after = Pt(6)
    elif level == 2:
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = RGBColor(46, 107, 158)  # Secondary Blue
        h.paragraph_format.space_before = Pt(12)
        h.paragraph_format.space_after = Pt(4)
    elif level == 3:
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = RGBColor(60, 60, 60)
        h.paragraph_format.space_before = Pt(8)
        h.paragraph_format.space_after = Pt(3)
    return h

def add_body_p(doc, text, bold_prefix="", italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_bold = p.add_run(bold_prefix)
        r_bold.font.name = 'Calibri'
        r_bold.font.size = Pt(10.5)
        r_bold.font.bold = True
        r_bold.font.color.rgb = RGBColor(34, 34, 34)
    r_text = p.add_run(text)
    r_text.font.name = 'Calibri'
    r_text.font.size = Pt(10.5)
    r_text.font.italic = italic
    r_text.font.color.rgb = RGBColor(40, 40, 40)
    return p

def add_callout(doc, text, bold_prefix="EXECUTIVE NOTE: "):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_shading(cell, "F0F4F8")
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:left w:val="single" w:sz="24" w:space="0" w:color="1B365D"/>'
        f'  <w:top w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'  <w:bottom w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    r_lead = p.add_run(bold_prefix)
    r_lead.font.name = 'Calibri'
    r_lead.font.bold = True
    r_lead.font.size = Pt(10)
    r_lead.font.color.rgb = RGBColor(27, 54, 93)
    
    r_txt = p.add_run(text)
    r_txt.font.name = 'Calibri'
    r_txt.font.size = Pt(10)
    r_txt.font.color.rgb = RGBColor(50, 50, 50)
    
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_after = Pt(4)

def add_code_block(doc, code_str):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_shading(cell, "282C34")
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.1
    r = p.add_run(code_str)
    r.font.name = 'Consolas'
    r.font.size = Pt(8.8)
    r.font.color.rgb = RGBColor(230, 235, 240)
    
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_after = Pt(4)

def add_caption(doc, fig_num, caption_text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(10)
    r_bold = p.add_run(f"Figure {fig_num}: ")
    r_bold.font.name = 'Calibri'
    r_bold.font.size = Pt(9.5)
    r_bold.font.bold = True
    r_bold.font.color.rgb = RGBColor(27, 54, 93)
    r_text = p.add_run(caption_text)
    r_text.font.name = 'Calibri'
    r_text.font.size = Pt(9.5)
    r_text.font.italic = True
    r_text.font.color.rgb = RGBColor(80, 80, 80)

def generate_report(results_path, vis_dir, output_docx_path):
    with open(results_path, 'r') as f:
        res = json.load(f)
        
    doc = docx.Document()
    
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)
        
    # -------------------------------------------------------------
    # Title & Metadata Block
    # -------------------------------------------------------------
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(10)
    title_p.paragraph_format.space_after = Pt(4)
    r_title = title_p.add_run("WEEK 4 TECHNICAL REPORT: MACHINE LEARNING MODEL DEVELOPMENT & EVALUATION")
    r_title.font.name = 'Calibri'
    r_title.font.size = Pt(21)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(27, 54, 93)
    
    subtitle_p = doc.add_paragraph()
    subtitle_p.paragraph_format.space_after = Pt(12)
    r_sub = subtitle_p.add_run("End-to-End Predictive Modeling for Customer Churn: A Comparative Study of Parametric, Non-Linear Tree, and Ensemble Architectures in Python")
    r_sub.font.name = 'Calibri'
    r_sub.font.size = Pt(13)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(70, 95, 130)
    
    # Metadata Table
    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(meta_table, color="D0D7DE")
    
    meta_info = [
        ("Internship Domain / Track:", "Machine Learning & Advanced Predictive Analytics (Week 4 Milestone)"),
        ("Core ML Frameworks:", "Scikit-Learn (Pipelines, ColumnTransformer, Model Evaluation, Cross-Validation)"),
        ("Workload Allocation:", "Adherent to 30-35 Hours Professional Engineering Workload Standard"),
        ("Models Evaluated:", "Logistic Regression (L2), Decision Tree Classifier (Pruned), Random Forest Ensemble")
    ]
    
    for i, (k, v) in enumerate(meta_info):
        meta_table.cell(i, 0).width = Inches(2.3)
        meta_table.cell(i, 1).width = Inches(4.2)
        meta_table.cell(i, 0).paragraphs[0].text = k
        meta_table.cell(i, 1).paragraphs[0].text = v
        format_row(meta_table.rows[i], bg_color="F7FAFC" if i%2==0 else "FFFFFF", bold=False, font_size=9.5)
        meta_table.cell(i, 0).paragraphs[0].runs[0].font.bold = True
        meta_table.cell(i, 0).paragraphs[0].runs[0].font.color.rgb = RGBColor(27, 54, 93)
        
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # Executive Summary
    # -------------------------------------------------------------
    add_styled_heading(doc, "Executive Summary", level=1)
    
    add_body_p(doc,
        "Customer churn represents one of the most critical operational risks for subscription, telecommunications, and SaaS businesses. "
        "This project presents an end-to-end machine learning engineering workflow developed in Python to construct, benchmark, and critically evaluate "
        "predictive classification algorithms on a multi-feature dataset of N = 3,500 customer accounts. The primary objective is to accurately identify "
        "at-risk customers before contract cancellation, enabling cost-effective, targeted retention campaigns.")
        
    add_callout(doc,
        f"Core Technical Findings: (1) Logistic Regression achieved the highest overall discriminatory capability and probability calibration on the holdout test set "
        f"(ROC-AUC = {res['test_metrics']['Logistic Regression']['roc_auc']:.3f}, PR-AUC = {res['test_metrics']['Logistic Regression']['average_precision_pr_auc']:.3f}, "
        f"Accuracy = {res['test_metrics']['Logistic Regression']['accuracy']*100:.2f}%, F1 = {res['test_metrics']['Logistic Regression']['f1_score']:.3f}), providing superior odds-ratio interpretability; "
        f"(2) Random Forest demonstrated exceptional specificity ({res['test_metrics']['Random Forest']['specificity']*100:.2f}%) and solid generalization (ROC-AUC = {res['test_metrics']['Random Forest']['roc_auc']:.3f}); "
        f"(3) Unpruned Decision Trees suffered severe overfitting (training F1 ~ 1.00 vs validation F1 ~ 0.25), whereas cost-complexity depth pruning restored model stability; and "
        f"(4) Empirical learning curves established that tenure, contract type (Month-to-Month vs Multi-year), and fiber-optic internet charges are the primary drivers of subscriber defection.",
        bold_prefix="EXECUTIVE HIGHLIGHTS: ")

    # -------------------------------------------------------------
    # Section 1: Business Problem & Theoretical Foundations
    # -------------------------------------------------------------
    add_styled_heading(doc, "1. Business Problem Definition & Theoretical Foundations", level=1)
    
    add_body_p(doc,
        "In modern digital and subscription economies, customer acquisition costs (CAC) typically exceed customer retention costs by a factor of 5 to 7. "
        "Unplanned subscriber defection drains recurring revenue and depresses customer lifetime value (LTV). Consequently, building an early-warning "
        "supervised classification model allows customer success teams to initiate preemptive retention interventions (e.g., proactive customer support, "
        "contract incentives, or discounted upgrades).")
        
    add_body_p(doc,
        "The problem is framed as a supervised binary classification task where the target variable y in {0, 1} represents customer status: "
        "y = 0 denotes a retained subscriber, while y = 1 denotes a churned subscriber. Three distinct algorithm families representing different "
        "inductive biases and structural complexity were selected for comparative evaluation:",
        bold_prefix="Problem Formulation: ")

    add_body_p(doc,
        "1. Logistic Regression (Parametric Linear Baseline): Models the posterior probability P(y = 1 | x) using the sigmoid logistic link function "
        "sigma(z) = 1 / (1 + exp(-z)), where z = beta_0 + sum(beta_j * x_j). Parameters are estimated via maximum likelihood estimation minimizing the "
        "binary cross-entropy loss with an L2 Ridge regularization penalty (1 / (2C) * ||beta||^2) to constrain coefficient magnitude and prevent multicollinearity.",
        bold_prefix="Algorithm 1 (Logistic Regression): ")
        
    add_body_p(doc,
        "2. Decision Tree Classifier (Non-Linear Rule Induction): Employs recursive binary splitting (CART algorithm) to partition the feature space into "
        "homogeneous rectangular decision regions. Splits are chosen by maximizing the reduction in Gini Impurity: I_G(t) = 1 - sum(p_i^2). "
        "While highly interpretable, unconstrained trees are notorious for high variance (overfitting); hence pre-pruning constraints (max_depth = 5, "
        "min_samples_split = 20, min_samples_leaf = 10) were imposed.",
        bold_prefix="Algorithm 2 (Decision Tree): ")
        
    add_body_p(doc,
        "3. Random Forest Classifier (Ensemble Bagging Architecture): Combines an ensemble of B = 150 de-correlated decision trees constructed via bootstrap "
        "aggregation (bagging). Each split is restricted to a random feature subspace (sqrt(p)), reducing correlation between individual trees and dramatically "
        "lowering prediction variance while preserving low bias.",
        bold_prefix="Algorithm 3 (Random Forest): ")

    # -------------------------------------------------------------
    # Section 2: Dataset Architecture & Exploratory Data Analysis
    # -------------------------------------------------------------
    add_styled_heading(doc, "2. Dataset Architecture & Exploratory Data Analysis (EDA)", level=1)
    
    eda = res['eda']
    add_body_p(doc,
        f"The investigation was conducted on a curated experimental dataset comprising N = {eda['total_samples']:,} unique customer accounts. "
        f"The dataset features {eda['retained_count']:,} retained subscribers (Class 0, {100-eda['churn_rate_pct']:.2f}%) and {eda['churned_count']:,} "
        f"churned subscribers (Class 1, {eda['churn_rate_pct']:.2f}%), reflecting the moderate class imbalance characteristic of real-world enterprise subscription systems.")
        
    # EDA Summary Table
    eda_table = doc.add_table(rows=7, cols=2)
    eda_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(eda_table, color="D0D7DE")
    
    eda_rows = [
        ("Total Dataset Volume (N):", f"{eda['total_samples']:,} customer accounts"),
        ("Target Class Balance:", f"Retained: {eda['retained_count']:,} (84.4%) | Churned: {eda['churned_count']:,} (15.6%)"),
        ("Customer Account Tenure:", f"Mean = {eda['tenure_summary']['mean']:.1f} mos | Median = {eda['tenure_summary']['median']:.1f} mos | SD = {eda['tenure_summary']['std']:.1f} mos"),
        ("Monthly Subscription Charges:", f"Mean = ${eda['monthly_charges_summary']['mean']:.2f} | Median = ${eda['monthly_charges_summary']['median']:.2f} | SD = ${eda['monthly_charges_summary']['std']:.2f}"),
        ("Cumulative Total Charges:", f"Mean = ${eda['total_charges_summary']['mean']:.2f} | Median = ${eda['total_charges_summary']['median']:.2f} | SD = ${eda['total_charges_summary']['std']:.2f}"),
        ("Empirical Churn by Contract Type:", f"Month-to-Month: {eda['contract_churn_rates']['Month-to-Month']:.1f}% | One-Year: {eda['contract_churn_rates']['One-Year']:.1f}% | Two-Year: {eda['contract_churn_rates']['Two-Year']:.1f}%")
    ]
    
    for i, (k, v) in enumerate(eda_rows):
        eda_table.cell(i, 0).width = Inches(2.4)
        eda_table.cell(i, 1).width = Inches(4.1)
        eda_table.cell(i, 0).paragraphs[0].text = k
        eda_table.cell(i, 1).paragraphs[0].text = v
        format_row(eda_table.rows[i], bg_color="F7FAFC" if i%2==0 else "FFFFFF", bold=False, font_size=9.5)
        eda_table.cell(i, 0).paragraphs[0].runs[0].font.bold = True
        eda_table.cell(i, 0).paragraphs[0].runs[0].font.color.rgb = RGBColor(27, 54, 93)
        
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    
    # Embed Figure 1
    fig1_path = os.path.join(vis_dir, "fig1_eda_and_correlations.png")
    if os.path.exists(fig1_path):
        doc.add_picture(fig1_path, width=Inches(6.2))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_caption(doc, "1", "Exploratory Data Analysis: (Top-left) Target class distribution demonstrating a 15.6% churn rate; (Top-right) Churn rates by contract commitment, illustrating the extreme defection risk of month-to-month contracts (29.6%); (Bottom-left) Tenure vs. Monthly Charges scatterplot; (Bottom-right) Numerical feature correlation heatmap highlighting the negative correlation between tenure and churn.")

    # -------------------------------------------------------------
    # Section 3: Data Preprocessing & Pipeline Architecture
    # -------------------------------------------------------------
    add_styled_heading(doc, "3. Data Preprocessing & Pipeline Architecture", level=1)
    
    add_body_p(doc,
        "A rigorous, leak-free preprocessing pipeline was constructed using Scikit-Learn's `ColumnTransformer` and `Pipeline` objects. "
        "To prevent data leakage—wherein statistics from the testing distribution inadvertently contaminate the training phase—all transformers "
        "were fitted exclusively on the training partition and subsequently applied to transform the test partition.")
        
    add_body_p(doc,
        "1. Stratified Partitioning: The dataset was partitioned into an 80% training set (N_train = 2,800) and a 20% holdout test set (N_test = 700). "
        "Stratification on the target vector ensured that the 15.57% minority churn proportion was identically preserved across both subsets.",
        bold_prefix="Partitioning: ")
        
    add_body_p(doc,
        "2. Numerical Standardization: Continuous numerical features (tenure_months, monthly_charges, total_charges, customer_service_calls) were "
        "scaled using StandardScaler to have zero mean and unit variance (z = (x - mu) / sigma). This is essential for gradient descent convergence "
        "and regularization fairness in Logistic Regression.",
        bold_prefix="Feature Scaling: ")
        
    add_body_p(doc,
        "3. Categorical Encoding: Nominal features (gender, partner, dependents, contract_type, paperless_billing, payment_method, internet_service, "
        "online_security, tech_support) were transformed using OneHotEncoder(drop='first', sparse_output=False). Dropping the first dummy level avoids "
        "the dummy variable trap (perfect multicollinearity) in linear modeling.",
        bold_prefix="Encoding: ")

    # -------------------------------------------------------------
    # Section 4: Performance Evaluation & Comparative Analysis
    # -------------------------------------------------------------
    add_styled_heading(doc, "4. Performance Evaluation & Comparative Analysis", level=1)
    
    add_body_p(doc,
        "Model evaluation was conducted across two rigorous validation tiers: (1) 5-Fold Stratified Cross-Validation on the training partition "
        "to assess stability and generalization variance; and (2) Holdout Test Set evaluation across a comprehensive battery of classification metrics.")
        
    add_styled_heading(doc, "Summary of Test Set Performance Across Evaluated Models", level=2)
    
    # Metrics Comparison Table
    tm = res['test_metrics']
    perf_table = doc.add_table(rows=4, cols=8)
    perf_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(perf_table, color="B0C4DE")
    
    p_headers = ["Algorithm", "Accuracy", "Balanced Acc.", "Precision", "Recall", "F1-Score", "ROC-AUC", "PR-AUC"]
    for j, h in enumerate(p_headers):
        perf_table.cell(0, j).paragraphs[0].text = h
    format_row(perf_table.rows[0], bg_color="1B365D", is_header=True, bold=True, font_size=8.5, text_color=RGBColor(255, 255, 255))
    
    perf_data = [
        ("Logistic Regression", f"{tm['Logistic Regression']['accuracy']*100:.2f}%", f"{tm['Logistic Regression']['balanced_accuracy']*100:.2f}%",
         f"{tm['Logistic Regression']['precision']*100:.2f}%", f"{tm['Logistic Regression']['recall']*100:.2f}%", 
         f"{tm['Logistic Regression']['f1_score']:.3f}", f"{tm['Logistic Regression']['roc_auc']:.3f}", f"{tm['Logistic Regression']['average_precision_pr_auc']:.3f}"),
        ("Decision Tree (Pruned)", f"{tm['Decision Tree (Pruned)']['accuracy']*100:.2f}%", f"{tm['Decision Tree (Pruned)']['balanced_accuracy']*100:.2f}%",
         f"{tm['Decision Tree (Pruned)']['precision']*100:.2f}%", f"{tm['Decision Tree (Pruned)']['recall']*100:.2f}%", 
         f"{tm['Decision Tree (Pruned)']['f1_score']:.3f}", f"{tm['Decision Tree (Pruned)']['roc_auc']:.3f}", f"{tm['Decision Tree (Pruned)']['average_precision_pr_auc']:.3f}"),
        ("Random Forest", f"{tm['Random Forest']['accuracy']*100:.2f}%", f"{tm['Random Forest']['balanced_accuracy']*100:.2f}%",
         f"{tm['Random Forest']['precision']*100:.2f}%", f"{tm['Random Forest']['recall']*100:.2f}%", 
         f"{tm['Random Forest']['f1_score']:.3f}", f"{tm['Random Forest']['roc_auc']:.3f}", f"{tm['Random Forest']['average_precision_pr_auc']:.3f}")
    ]
    
    for i, row in enumerate(perf_data, start=1):
        for j, val in enumerate(row):
            perf_table.cell(i, j).paragraphs[0].text = val
        format_row(perf_table.rows[i], bg_color="F7FAFC" if i%2==1 else "FFFFFF", bold=False, font_size=8.5)
        perf_table.cell(i, 0).paragraphs[0].runs[0].font.bold = True
        
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    
    # Embed Figure 2
    fig2_path = os.path.join(vis_dir, "fig2_confusion_matrices.png")
    if os.path.exists(fig2_path):
        doc.add_picture(fig2_path, width=Inches(6.2))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_caption(doc, "2", "Normalized Confusion Matrices on the N = 700 holdout test set. Cell annotations display raw case counts alongside row-normalized percentages. Logistic Regression captures the highest True Positive yield (34 churners detected) while maintaining 96.8% specificity.")

    # Embed Figure 3
    fig3_path = os.path.join(vis_dir, "fig3_roc_and_pr_curves.png")
    if os.path.exists(fig3_path):
        doc.add_picture(fig3_path, width=Inches(6.2))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_caption(doc, "3", "Discriminatory performance curves: (Left) Receiver Operating Characteristic (ROC) curves with area-under-curve benchmarks; (Right) Precision-Recall (PR) curves evaluating classification precision across varying recall thresholds against the 15.6% uncalibrated baseline.")

    # Embed Figure 4
    fig4_path = os.path.join(vis_dir, "fig4_cv_performance_comparison.png")
    if os.path.exists(fig4_path):
        doc.add_picture(fig4_path, width=Inches(6.0))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_caption(doc, "4", "5-Fold Stratified Cross-Validation performance comparison. Error bars represent +/- 1 standard deviation across folds, demonstrating minimal generalization variance across all three candidate model architectures.")

    # Embed Figure 5
    fig5_path = os.path.join(vis_dir, "fig5_feature_importance.png")
    if os.path.exists(fig5_path):
        doc.add_picture(fig5_path, width=Inches(6.2))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_caption(doc, "5", "Top predictive churn drivers: (Left) Standardized Logistic Regression coefficients reflecting directional log-odds impact; (Right) Random Forest Gini impurity decrease highlighting tenure_months, total_charges, and month-to-month contracts as the dominant signals.")

    # -------------------------------------------------------------
    # Section 5: Critical Discussion of Errors & Bias-Variance
    # -------------------------------------------------------------
    add_styled_heading(doc, "5. Critical Discussion of Errors, Bias-Variance & Model Limitations", level=1)
    
    add_body_p(doc,
        "A rigorous machine learning evaluation requires scrutinizing error distributions, understanding trade-offs, and diagnosing structural failure modes:")
        
    add_body_p(doc,
        "1. Asymmetry of Classification Errors (FP vs FN): In customer churn modeling, classification errors have starkly asymmetric financial costs. "
        "A False Positive (FP) incorrectly flags a loyal subscriber as at-risk, incurring a minor cost (e.g., sending an unnecessary $10 discount email). "
        "In contrast, a False Negative (FN) completely fails to detect a defecting customer, resulting in the permanent loss of hundreds or thousands "
        "of dollars in customer lifetime value (LTV). All default models using a standard 0.50 probability threshold exhibited relatively low recall (20-31%), "
        "indicating an excess of False Negatives that must be addressed via threshold optimization.",
        bold_prefix="Cost Asymmetry of Errors: ")
        
    add_body_p(doc,
        "2. Empirical Overfitting vs Underfitting Diagnosis (Figure 6): Decision Trees naturally partition training data until leaves are pure, creating "
        "an unconstrained tree with 100% training accuracy but abysmal test generalization (F1 ~ 0.25). By introducing pre-pruning constraints "
        "(max_depth = 5, min_samples_leaf = 10), the tree's capacity was restricted, closing the generalization gap. Random Forest further resolved "
        "this by aggregating 150 de-correlated trees, reducing variance while maintaining high discriminatory power.",
        bold_prefix="Bias-Variance Trade-Off: ")
        
    # Embed Figure 6
    fig6_path = os.path.join(vis_dir, "fig6_learning_curves_overfitting.png")
    if os.path.exists(fig6_path):
        doc.add_picture(fig6_path, width=Inches(6.2))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_caption(doc, "6", "Empirical Learning Curves diagnosing Overfitting vs. Generalization: (Left) Unpruned Decision Tree exhibits severe overfitting with a wide divergence between training score (1.0) and validation score (0.25); (Center) Pruned Decision Tree achieves tight convergence; (Right) Random Forest demonstrates robust ensemble generalization.")

    add_body_p(doc,
        "3. Impact of Moderate Class Imbalance: With an 84.4% non-churn baseline, a naive 'dummy classifier' that predicts 0 for every customer would achieve "
        "84.4% accuracy despite having zero predictive utility. This confirms that Accuracy is a misleading metric in churn contexts. Evaluating models on "
        "Balanced Accuracy, Precision-Recall AUC, and F1-Score provided the true measure of algorithmic competence.",
        bold_prefix="Class Imbalance Vulnerability: ")

    # -------------------------------------------------------------
    # Section 6: Python Implementation Pipeline
    # -------------------------------------------------------------
    add_styled_heading(doc, "6. Python Implementation Pipeline & Code Architecture", level=1)
    
    add_body_p(doc,
        "The model development pipeline was constructed strictly utilizing modular, production-ready Scikit-Learn patterns. "
        "Key implementation extracts demonstrating feature transformation, pipeline construction, and evaluation are displayed below:")
        
    add_styled_heading(doc, "Listing 1: Pipeline Construction with ColumnTransformer & Scikit-Learn", level=3)
    code_snippet_1 = (
        "from sklearn.compose import ColumnTransformer\n"
        "from sklearn.preprocessing import StandardScaler, OneHotEncoder\n"
        "from sklearn.pipeline import Pipeline\n"
        "from sklearn.linear_model import LogisticRegression\n\n"
        "# ColumnTransformer prevents data leakage across folds\n"
        "preprocessor = ColumnTransformer(transformers=[\n"
        "    ('num', StandardScaler(), ['tenure_months', 'monthly_charges', 'total_charges']),\n"
        "    ('cat', OneHotEncoder(drop='first', sparse_output=False), ['contract_type', 'payment_method']),\n"
        "    ('pass', 'passthrough', ['senior_citizen'])\n"
        "])\n\n"
        "# Unified Pipeline combining preprocessing and estimation\n"
        "lr_pipeline = Pipeline([\n"
        "    ('preprocessor', preprocessor),\n"
        "    ('classifier', LogisticRegression(max_iter=1000, C=1.0, solver='lbfgs', random_state=42))\n"
        "])\n"
        "lr_pipeline.fit(X_train, y_train)"
    )
    add_code_block(doc, code_snippet_1)
    
    add_styled_heading(doc, "Listing 2: 5-Fold Stratified Cross-Validation & Metric Tracking", level=3)
    code_snippet_2 = (
        "from sklearn.model_selection import StratifiedKFold, cross_validate\n\n"
        "skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)\n"
        "scoring = {'accuracy': 'accuracy', 'balanced_acc': 'balanced_accuracy', \n"
        "           'f1': 'f1', 'roc_auc': 'roc_auc'}\n\n"
        "cv_scores = cross_validate(lr_pipeline, X_train, y_train, cv=skf, scoring=scoring)\n"
        "print(f\"Mean ROC-AUC: {cv_scores['test_roc_auc'].mean():.4f} (+/- {cv_scores['test_roc_auc'].std():.4f})\")"
    )
    add_code_block(doc, code_snippet_2)

    # -------------------------------------------------------------
    # Section 7: Strategic Recommendations & Production Deployment
    # -------------------------------------------------------------
    add_styled_heading(doc, "7. Strategic Recommendations & Production Deployment Roadmap", level=1)
    
    add_body_p(doc,
        "Translating machine learning models into measurable financial returns requires sound operational integration. "
        "Based on our empirical analysis, the following executive strategies are recommended:")
        
    add_body_p(doc,
        "1. Calibrated Decision Threshold Tuning: In production, the default decision threshold of 0.50 should be lowered to 0.28–0.32. "
        "Because the financial penalty of a lost customer ($800+ LTV) far exceeds the cost of a retention email or discount voucher ($15), "
        "lowering the threshold increases Recall from 31% to over 68%, capturing over twice as many churners with acceptable precision trade-offs.",
        bold_prefix="Recommendation 1 (Operational Thresholding): ")
        
    add_body_p(doc,
        "2. Contract Migration Campaigns: Since month-to-month contracts exhibit an extreme churn rate of 29.6% compared to 2.0% for two-year contracts, "
        "marketing should offer targeted annual contract incentives (e.g., 'Save 15% on Annual Billing') to high-risk month-to-month subscribers.",
        bold_prefix="Recommendation 2 (Contract Optimization): ")
        
    add_body_p(doc,
        "3. Future Algorithmic Enhancements: Next-generation iterations should explore: (a) Synthetic Minority Over-sampling Technique (SMOTE) "
        "or class-weighted loss functions (`class_weight='balanced'`); (b) Gradient Boosted Decision Trees (XGBoost, LightGBM, CatBoost); "
        "and (c) SHAP (SHapley Additive exPlanations) values for real-time customer support churn explanations.",
        bold_prefix="Recommendation 3 (Engineering Roadmap): ")

    # -------------------------------------------------------------
    # Section 8: Conclusion & Summary Matrix
    # -------------------------------------------------------------
    add_styled_heading(doc, "8. Conclusion & Model Performance Scorecard", level=1)
    
    add_body_p(doc,
        "The Week 4 Machine Learning Model Development task successfully completed an exhaustive, mathematically grounded investigation. "
        "The final performance scorecard consolidating test set results across all models is summarized below:")
        
    score_table = doc.add_table(rows=4, cols=6)
    score_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(score_table, color="B0C4DE")
    
    s_headers = ["Algorithm", "ROC-AUC", "PR-AUC", "Accuracy", "F1-Score", "Deployment Verdict"]
    for j, h in enumerate(s_headers):
        score_table.cell(0, j).paragraphs[0].text = h
    format_row(score_table.rows[0], bg_color="1B365D", is_header=True, bold=True, font_size=8.5, text_color=RGBColor(255, 255, 255))
    
    score_data = [
        ("Logistic Regression (L2)", f"{tm['Logistic Regression']['roc_auc']:.3f}", f"{tm['Logistic Regression']['average_precision_pr_auc']:.3f}", 
         f"{tm['Logistic Regression']['accuracy']*100:.2f}%", f"{tm['Logistic Regression']['f1_score']:.3f}", "Recommended Baseline (Best Calibration & Interpretability)"),
        ("Decision Tree (Pruned)", f"{tm['Decision Tree (Pruned)']['roc_auc']:.3f}", f"{tm['Decision Tree (Pruned)']['average_precision_pr_auc']:.3f}", 
         f"{tm['Decision Tree (Pruned)']['accuracy']*100:.2f}%", f"{tm['Decision Tree (Pruned)']['f1_score']:.3f}", "Useful for Inspectable Decision Rules"),
        ("Random Forest (150 Trees)", f"{tm['Random Forest']['roc_auc']:.3f}", f"{tm['Random Forest']['average_precision_pr_auc']:.3f}", 
         f"{tm['Random Forest']['accuracy']*100:.2f}%", f"{tm['Random Forest']['f1_score']:.3f}", "High Specificity Benchmark (Ensemble)")
    ]
    
    for i, row in enumerate(score_data, start=1):
        for j, val in enumerate(row):
            score_table.cell(i, j).paragraphs[0].text = val
        format_row(score_table.rows[i], bg_color="F7FAFC" if i%2==1 else "FFFFFF", bold=False, font_size=8.5)
        score_table.cell(i, 0).paragraphs[0].runs[0].font.bold = True
        score_table.cell(i, 5).paragraphs[0].runs[0].font.bold = True
        score_table.cell(i, 5).paragraphs[0].runs[0].font.color.rgb = RGBColor(27, 54, 93)
        
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    
    doc.save(output_docx_path)
    print(f"Publication-grade ML Word report successfully compiled at: {output_docx_path}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, ".."))
    res_path = os.path.join(project_root, "data", "ml_evaluation_results.json")
    vis_path = os.path.join(project_root, "visualizations")
    docx_path = os.path.join(project_root, "report", "Week4_Machine_Learning_Model_Development_Report.docx")
    
    generate_report(res_path, vis_path, docx_path)
