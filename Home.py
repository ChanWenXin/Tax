import streamlit as st

st.set_page_config(page_title="📊 IRAS KPI Dashboard", layout="wide")

st.title("📘 IRAS Financial KPI Dashboard")
st.markdown("""
Welcome to the **Inland Revenue Authority of Singapore (IRAS)** Financial Dashboard for **FY2023/24**.  
This dashboard summarizes and analyzes data extracted from the official *IRAS Statement of Financial Position*, providing key insights into its equity structure, asset composition, and financial stability.  
Data source: IRAS Annual Report FY2023/24 (as at 31 March 2024).
""")

st.header("📌 Business Insights (FY2023/24 vs FY2022/23)")

st.markdown("""
- **Total Equity** increased by **+7.42%**, mainly driven by a rise in **Accumulated Surplus (+7.48%)**, indicating retained earnings growth.
- **Non-Current Assets** rose **+7.04%**, led by a significant rise in *Development Projects-in-Progress* (+138% YoY).
- **Current Assets** slightly increased **+1.97%**, with *Funds with fund managers* being the largest component.
- **Net Current Assets** remained stable with a marginal increase of **+0.39%**, reflecting conservative working capital management.
- **Non-Current Liabilities** dropped by **-30.19%**, contributing to improved **Debt-to-Equity** and **Liquidity Ratios**.
""")

st.header("📈 Financial KPI Definitions and Formulas")

st.markdown("""
### 1. **Equity-to-Assets Ratio**
- **Definition**: Shows how much of the organization's assets are financed by its own funds (equity).
- **Formula**:  
  Equity-to-Assets Ratio = (Total Equity / Total Assets) × 100
---

### 2. **Working Capital**
- **Definition**: Measures the short-term liquidity position of the organization.
- **Formula**:  
  Working Capital = Total Current Assets − Total Current Liabilities

---

### 3. **Current Ratio**
- **Definition**: Indicates the organization’s ability to pay short-term obligations with short-term assets.
- **Formula**:  
  Current Ratio = Total Current Assets / Total Current Liabilities

---

### 4. **Debt-to-Equity Ratio**
- **Definition**: Shows the proportion of external liabilities relative to equity.
- **Formula**:  
  Debt-to-Equity Ratio = Total Liabilities / Total Equity

---

### 5. **YoY Asset Growth**
- **Definition**: Year-over-Year percentage change in Total Assets.
- **Formula**:  
  YoY Asset Growth (%) = [(Total Assets FY2023/24 − Total Assets FY2022/23) / Total Assets FY2022/23] × 100
""")
# Income Statement

st.title("📘 Statement of Income Statement")
st.markdown("""
This page presents the **Income Statement** analysis from the **IRAS FY2023/24 Annual Report**, highlighting year-over-year performance changes and key income-related KPIs.  
It reflects the organization’s profitability, operational efficiency, and reliance on external/government funding sources.
""")

st.header("📊 Business Insights (FY2023/24 vs FY2022/23)")

st.markdown("""
- **Operating Income** grew by **+10.26%**, signaling healthy revenue growth year-over-year.
- **Operating Surplus** rose **+19.36%**, showing improved cost control and operational efficiency.
- **Net Investment Income** swung from a loss (-11M) to a gain (+35M), a **+415% turnaround**, significantly boosting surplus before government funding.
- **Net Surplus for the Year** surged by **+61.38%**, despite higher contributions to the **Government Consolidated Fund** (+60.97%).
- These improvements result in better **surplus margins** and **reduced dependency on government contributions**.
""")

st.header("📈 Income Performance KPI Definitions and Formulas")

st.markdown("""
### 1. **Operating Surplus Margin**
- **Definition**: Indicates the percentage of income retained after deducting operating expenses.
- **Formula**:
  Operating Surplus Margin = (Operating Surplus / Operating Income) × 100

---

### 2. **Net Surplus Margin**
- **Definition**: Measures the overall profitability after accounting for all expenses, including government contributions.
- **Formula**:
  Net Surplus Margin = (Net Surplus for the Year / Operating Income) × 100


---

### 3. **Investment Return Contribution**
- **Definition**: Reflects the portion of surplus generated from investment income.
- **Formula**:
  Investment Return Contribution = Net Investment Income / Operating Income

---

### 4. **Government Fund Contribution Ratio**
- **Definition**: Indicates how much of the surplus before government fund goes back as contribution to the government.
- **Formula**:
  Gov Fund Contribution Ratio = Contribution to Gov Fund / Surplus Before Gov Fund

---

### 5. **YoY Income Growth**
- **Definition**: Tracks the year-over-year growth in total operating income.
- **Formula**:
  YoY Income Growth (%) = [(FY2023/24 − FY2022/23) / FY2022/23] × 100
""")

st.title("📘 Statement of Changes in Equity")
st.markdown("""
This page highlights key components affecting equity changes for **IRAS FY2023/24**, focusing on **total comprehensive income** and **dividends paid**.  
These values are essential in understanding how retained earnings are affected year-over-year.
""")

st.header("📊 Business Insights (FY2023/24 vs FY2022/23)")

st.markdown("""
- **Total Comprehensive Income** increased by **+61.38%**, indicating stronger financial performance and profitability in FY2023/24.
- **Dividends Paid** rose dramatically to **SGD -80,000**, a **+3789.16% increase** compared to FY2022/23, reflecting greater distribution to the Government Consolidated Fund or reserves.
- This suggests stronger confidence in the organization's fiscal position, allowing for higher returns to stakeholders.
""")

st.header("📈 Equity KPI Definitions and Formulas")

st.markdown("""
### 1. **Total Comprehensive Income**
- **Definition**: Includes both the net surplus and other gains/losses recognized in equity (such as revaluation or actuarial gains/losses).
- **Formula**:
  Total Comprehensive Income = Net Surplus for the Year + Other Comprehensive Income 
> In this dataset, it matches the reported **Net Surplus**, as no other comprehensive income was recorded.

---

### 2. **Dividends Paid**
- **Definition**: The total amount of earnings distributed to stakeholders or transferred to reserve funds during the year.
- **Formula**:
  Dividends Paid = − Amount Transferred to Government Fund or Reserves
> A higher figure reflects stronger profitability and more retained earnings being returned.

---

### 3. **YoY Change (%)**
- **Definition**: Measures year-on-year performance improvement.
- **Formula**:
  YoY Change (%) = [(FY2023/24 − FY2022/23) / FY2022/23] × 100
""")

st.title("📘 Statement of Cash Flows")
st.markdown("""
This page analyzes the **cash inflows and outflows** of IRAS for **FY2023/24**, with key KPIs for financial liquidity, sustainability, and operational efficiency.  
It gives insight into how IRAS generates and uses cash, crucial for evaluating short-term health and strategic funding.
""")

st.header("📊 Business Insights (FY2023/24 vs FY2022/23)")

st.markdown("""
- **Net Cash from Operating Activities** rose by **+48.18%**, signaling improved core operations and stronger cash generation.
- **Cash from Investing Activities** slightly decreased due to more outflows, but this may reflect strategic long-term investments.
- **Financing Cash Outflows** surged **+204.24%**, indicating a substantial increase in payouts (e.g., dividends).
- **Ending Cash** declined by **-13.21%**, though this still reflects a solid **11.1-month cash runway** and **positive free cash flow** of **S$280,417**.
- **Net Cash Margin** is **-13.21%**, suggesting that expenses still exceed cash inflows, mainly due to investment and financing activities.
""")

st.header("📈 Cash Flow KPI Definitions and Formulas")

st.markdown("""
### 1. **Free Cash Flow (FCF)**
- **Definition**: The cash left over after operational and capital expenditures — a key indicator of sustainability.
- **Formula**:
  Free Cash Flow = Net Cash from Operating Activities + Net Cash from Investing Activities

---

### 2. **Cash Flow Coverage Ratio**
- **Definition**: Assesses how well operating cash covers financing outflows.
- **Formula**:
  Coverage Ratio = Net Cash from Operating Activities / |Net Cash from Financing Activities|

---

### 3. **Cash Runway**
- **Definition**: Estimates how long the organization can continue operating at current burn rate before depleting its cash.
- **Formula**:
  Cash Runway (months) = Ending Cash / |Average Monthly Net Cash Outflow|
> For IRAS, since operating cash is **positive**, this is estimated using net monthly movement.

---

### 4. **Net Cash Margin**
- **Definition**: Shows what percentage of revenue is converted into net cash.
- **Formula**:
  Net Cash Margin = (Net Cash Movement / Operating Income) × 100

---

### 5. **Cash Burn Rate**
- **Definition**: The monthly rate of negative cash flow, typically used when operating cash is negative.
- **Formula**:  
  Cash Burn Rate = |Monthly Net Cash Movement
- **Note**: Not applicable for IRAS in FY2023/24 due to **positive operational cash flow**.
""")