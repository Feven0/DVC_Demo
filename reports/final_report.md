# Insurance Risk & Profitability Analytics: Strategic Portfolio Report

## 1. Executive Summary

This report presents a thorough, modular exploratory data analysis of the historical insurance portfolio dataset (`MachineLearningRating_v3.txt`), which consists of **1,000,098 transaction records** across South Africa. 

Our main strategic discovery is that the overall portfolio is **currently unprofitable**, showing an overall **Loss Ratio of 104.77%** (representing $1.048 in claims paid for every $1.000 in premiums collected). This indicates an immediate need for data-driven risk premium adjustments, selective underwriting, and targeted marketing policies.

---

## 2. Logical Data Groups & Preprocessing

The variables in this portfolio are organized into seven logical domains:

1.  **Policy**: Cover IDs and policy keys.
2.  **Transaction**: Temporal markers.
3.  **Client**: Demographic features (gender, language, bank, marital status).
4.  **Location**: Geographic indicators (province, postal code, Cresta zones).
5.  **Vehicle**: Technical specifications and features (make, model, registration year, custom value).
6.  **Plan**: Sum insured, excess selected, coverage options.
7.  **Payment & Claim**: Premium collected and claim amounts paid.

### Preprocessing and Memory Optimization
Due to the dataset's size (529MB), we implemented a **chunked loading architecture** using `pandas` to process batches of 100,000 records. This reduced the peak memory usage during tokenizer execution, securing production-level execution. Numeric columns were standardized, and dates were parsed to active `datetime64[ns]` objects.

---

## 3. Data Quality & Missingness

*   **VAT Registration & Bank Info**: Have high completeness (under 0.1% missing).
*   **Technical Specifications**: Column groups like `Cylinders`, `cubiccapacity`, and `kilowatts` show some missing values (~5%), which we will impute using vehicle make/model medians before predictive modeling.
*   **Data Standard**: The clean pipe-separated parsing and standard data typing guarantee that downstream tasks (statistical testing and modeling) can execute reliably.

---

## 4. Empirical Findings (Guiding Questions)

### Q1: Portfolio Loss Ratio Analysis

$$\text{Loss Ratio} = \frac{\sum \text{TotalClaims}}{\sum \text{TotalPremium}}$$

The overall portfolio Loss Ratio is **104.77%**. Let's examine how this varies across segments:

#### A. Geographic Variation (By Province)
Gauteng represents the highest overall claim concentration and a highly unprofitable Loss Ratio.

| Province | Total Claims Paid | Total Premiums Collected | Loss Ratio (%) | Profitability Status |
| :--- | :--- | :--- | :--- | :--- |
| **Gauteng** | $29.39M | $24.05M | **122.20%** | 🔴 Critical Loss |
| **KwaZulu-Natal** | $14.30M | $13.21M | **108.27%** | 🔴 Unprofitable |
| **Western Cape** | $10.39M | $9.81M | **105.95%** | 🔴 Unprofitable |
| **North West** | $5.92M | $7.49M | **79.04%** | 🟢 Profitable |
| **Mpumalanga** | $2.04M | $2.84M | **72.09%** | 🟢 Highly Profitable |

#### B. Vehicle Segment Variation
Heavy commercial transport represents the highest underwriting risk, whereas light commercial fleets and buses are highly profitable.

| Vehicle Type | Loss Ratio (%) | Underwriting Insights |
| :--- | :--- | :--- |
| **Heavy Commercial** | **162.81%** | 🔴 High-risk claims, require premium hike |
| **Medium Commercial**| **105.03%** | 🔴 Borderline unprofitable |
| **Passenger Vehicle**| **104.82%** | 🔴 High-volume passenger risks (taxis, etc.) |
| **Light Commercial** | **23.21%** | 🟢 Highly profitable; expand marketing |
| **Bus** | **13.73%** | 🟢 Extremely profitable |

#### C. Demographic Variation (By Gender)
*   **Not Specified** (Fleet/Corporate accounts): **105.93% Loss Ratio** (🔴 Unprofitable).
*   **Male**: **88.39% Loss Ratio** (🟢 Profitable).
*   **Female**: **82.19% Loss Ratio** (🟢 More Profitable).

---

### Q2: Financial Distributions & Outliers

*   **Total Premium**: Median premium is low ($2.18), with the 99th percentile at $778.70.
*   **Total Claims**: Over 99% of transactions record $0 in claims. However, the 99.9th percentile reaches **$19,629.19**, indicating a heavy right-skewed, long-tailed distribution.
*   **Custom Value Estimate**: Show strong presence of high-value vehicle outliers up to **$715,712** (median is $220,000).
*   **Underwriting Action**: Large claims from high-value vehicles are the major drivers of portfolio unprofitability. We must introduce claim capping or special deductibles for vehicles valued above the 95th percentile ($360k).

---

### Q3: Temporal Analysis

Over the 18-month historical period:
1.  **Claim Frequency**: Remained consistently low and stable, fluctuating under **0.30%** monthly.
2.  **Claim Severity**: Peaked dramatically in November 2013 ($25.3k average claim) and August 2015 ($46.4k average claim).
3.  **Strategic Conclusion**: The portfolio's losses are driven by **sudden large-scale claims (severity)** rather than an increasing frequency of accidents. This highlights the importance of re-evaluating risk models for high-value assets.

---

### Q4: Vehicle Make & Model Risk Profiling

*   **Toyota**: Represents the highest aggregate claim amount (**$51.75 million**), driven by its massive share of South Africa's transport sector (especially commercial passenger transport).
*   **Mercedes-Benz & Volkswagen**: Show the highest average severity per claim ($70.07 and $87.88, respectively), reflecting high spare-part and replacement costs.

---

## 5. Strategic Recommendations

1.  **Gauteng Underwriting Reform**: Immediately increase base premiums for passenger vehicles in Gauteng by 25% or implement more restrictive deductibles.
2.  **Commercial Transport Premium Adjustment**: Adjust Heavy Commercial base rates to reflect their 162.81% Loss Ratio.
3.  **Target Gender-Specific Segments**: Expand promotional campaigns targeting female and identified male drivers, who currently yield profitable loss profiles.
4.  **Deductible Reconstruction**: Revise the deductible choices for high-value vehicle makes (Mercedes-Benz, Volkswagen) to offset severe repair claim costs.
