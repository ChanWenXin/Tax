import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# --- Load Excel file ---
df_income = pd.read_excel('data/iras-fs-fy2324.xlsx', sheet_name="Statement of Com. Income")
clean_df_income = df_income
# clean_df_income = df_income.dropna(how='all').dropna(axis=1, how='all')

# Income Statement
# Fix the issue by using a fallback method to safely extract and clean values

# Helper function that safely converts to int or returns 0
def safe_int(val):
    try:
        return int(val)
    except:
        return 0

# Re-run KPI extraction with safe handling
def extract_kpi_income(df, row_label, col_label='INLAND REVENUE AUTHORITY OF SINGAPORE', value_cols=('Unnamed: 4', 'Unnamed: 6')):
    row = df[df[col_label].str.contains(row_label, case=False, na=False)]
    if row.empty:
        return None, None, None
    val_new = safe_int(row[value_cols[0]].values[0])
    val_old = safe_int(row[value_cols[1]].values[0])
    pct_change = ((val_new - val_old) / val_old) * 100 if val_old != 0 else 0
    return val_new, val_old, round(pct_change, 2)

# Collect KPI revenue results
kpi_revenue = {}


# Operating Income
oi_2023 = clean_df_income.iloc[6:8,4].apply(safe_int).sum()  # E8 to E9
oi_2022 = clean_df_income.iloc[6:8,6].apply(safe_int).sum()  # G8 to G9 = cols 6

kpi_revenue["Operating Income"] = (oi_2023, oi_2022, round((oi_2023 - oi_2022) / oi_2022 * 100, 2))


# Operating Expenditure
oe_2023 = clean_df_income.iloc[12:23, 4].apply(safe_int).sum()  # E14 to E24
oe_2022 = clean_df_income.iloc[12:23, 6].apply(safe_int).sum()  # G14 to G24 = cols 6

kpi_revenue["Total Equity"] = (oe_2023, oe_2022, round((oe_2023 - oe_2022) / oe_2022 * 100, 2))


# Operating Surplus
kpi_revenue["Operating Surplus"] = extract_kpi_income(clean_df_income, "Operating surplus", col_label='INLAND REVENUE AUTHORITY OF SINGAPORE')

# Net Investment Income/(Loss
end_val = safe_int(clean_df_income.iloc[27, 4])  # New
begin_val = safe_int(clean_df_income.iloc[27, 6])    # Old
pct_change = round(((end_val - begin_val) / begin_val) * 100, 2) if begin_val != 0 else 0

kpi_revenue["Net Investment Income/(Loss)"] = (end_val, begin_val, pct_change)


#  Surplus Before Gov Fund
kpi_revenue["Surplus Before Gov Fund"] = extract_kpi_income(clean_df_income, "Government Consolidated Fund", col_label='INLAND REVENUE AUTHORITY OF SINGAPORE')

#  Contribution to Gov Fund
kpi_revenue["Contribution to Gov Fund"] = extract_kpi_income(clean_df_income, "Contribution to Government Consolidated Fund", col_label='INLAND REVENUE AUTHORITY OF SINGAPORE')

# Net Surplus for the Year
kpi_revenue["Net Surplus for the Year"] = extract_kpi_income(clean_df_income, "comprehensive income for the financial year", col_label='INLAND REVENUE AUTHORITY OF SINGAPORE')


# --- Streamlit Layout ---
st.title("📘 Statement of Income Statement")

st.caption("FY2023/24 vs FY2022/23 (Singapore IRAS)")

# METRICS/KPI

# Extract required values from kpi_results
# FY2023 values (latest year)
operating_income = kpi_revenue["Operating Income"][0]
operating_surplus = kpi_revenue["Operating Surplus"][0]
investment_income = kpi_revenue["Net Investment Income/(Loss)"][0]
surplus_before_gov = kpi_revenue["Surplus Before Gov Fund"][0]
gov_contribution = kpi_revenue["Contribution to Gov Fund"][0]
net_surplus = kpi_revenue["Net Surplus for the Year"][0]

# Optional: FY2022 values for YoY analysis (if needed later)
operating_income_2022 = kpi_revenue["Operating Income"][1]

# 1. Operating Surplus Margin
operating_surplus_margin = operating_surplus / operating_income if operating_income else 0

# 2. Investment Return Contribution
investment_contribution_ratio = investment_income / operating_income if operating_income else 0

# 3. Government Fund Contribution Ratio
gov_contribution_ratio = gov_contribution / surplus_before_gov if surplus_before_gov else 0

# 4. Net Surplus Margin
net_surplus_margin = net_surplus / operating_income if operating_income else 0

# 5. YoY Operating Income Growth (already shown in KPI table, but can be pulled out too)
income_growth_pct = ((operating_income - operating_income_2022) / operating_income_2022 * 100) if operating_income_2022 else 0

st.markdown("### 💼 Income Performance KPIs")

# All KPI
col1, col2, col3 = st.columns(3)

with col1:
     st.markdown(f"""
<div style="padding-bottom:1rem">
    <div style="font-size:1.5rem;color:white;font-weight:800">Operating Surplus Margin</div>
    <div style="font-size:1.5rem;font-weight:bold;color:deepskyblue">{operating_surplus_margin:,.2%}</div>
</div>
""", unsafe_allow_html=True)

     st.markdown(f"""
<div style="padding-bottom:1rem">
    <div style="font-size:1.5rem;color:white;font-weight:800">Investment Return Contribution</div>
    <div style="font-size:1.5rem;font-weight:bold;color:deepskyblue">{investment_contribution_ratio:,.2f}</div>
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
<div style="padding-bottom:1rem">
    <div style="font-size:1.5rem;color:white;font-weight:800">Gov Fund Contribution Ratio</div>
    <div style="font-size:1.5rem;font-weight:bold;color:deepskyblue">{gov_contribution_ratio:,.2f}</div>
</div>
""", unsafe_allow_html=True)
    
    st.markdown(f"""
<div style="padding-bottom:1rem">
    <div style="font-size:1.5rem;color:white;font-weight:800">Net Surplus Margin</div>
    <div style="font-size:1.5rem;font-weight:bold;color:deepskyblue">{net_surplus_margin:,.2f}</div>
</div>
""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
<div style="padding-bottom:1rem">
    <div style="font-size:1.5rem;color:white;font-weight:800">YoY Income Growth</div>
    <div style="font-size:1.5rem;font-weight:bold;color:{'green' if income_growth_pct > 0 else 'red'}">{income_growth_pct:+.2f}%</div>
</div>
""", unsafe_allow_html=True)


# Convert KPI dictionary to DataFrame - just a normal table without +/- in green/red
kpi_df_income = pd.DataFrame.from_dict(kpi_revenue, orient='index', columns=["FY2023/24", "FY2022/23", "% Change"])
kpi_df_income.index.name = "Metric"
kpi_df_income = kpi_df_income.reset_index()
# kpi_df_income

def color_percent(val):
    try:
        val = float(val)
        color = "green" if val > 0 else "red" if val < 0 else "gray"
        return f"color: {color}"
    except:
        return ""

styled_df = kpi_df_income.style.format({
    "FY2023/24": "{:,.0f}",
    "FY2022/23": "{:,.0f}",
    "% Change": "{:+.2f}%"
}).applymap(color_percent, subset=["% Change"])

st.markdown("### 📊 KPI Summary Table")
st.dataframe(styled_df)

# --- Two-column KPI layout ---
st.markdown("### 💡 Quick View")

col1, col2 = st.columns(2)

# Define render_metric format
def render_metric(label, v1, pct):
    if pct > 0:
        arrow = "🟢 ↑"
        color = "green"
    elif pct < 0:
        arrow = "🔴 ↓"
        color = "red"
    else:
        arrow = "➖"
        color = "gray"

    st.markdown(f"""
    <div style="padding-bottom:1rem">
        <div style="font-size:1.5rem;color:white;font-weight:800">{label}</div>
        <div style="font-size:1.5rem;font-weight:bold">{v1:,}</div>
        <div style="color:{color}; font-size:0.9rem">{arrow} {abs(pct):.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

col1, col2 = st.columns(2)
half = len(kpi_revenue) // 2

with col1:
    for label in list(kpi_revenue.keys())[:half]:
        v1, v2, pct = kpi_revenue[label]
        render_metric(label, v1, pct)

with col2:
    for label in list(kpi_revenue.keys())[half:]:
        v1, v2, pct = kpi_revenue[label]
        render_metric(label, v1, pct)

# --- KPI Bar Chart using Plotly ---
labels = list(kpi_revenue.keys())
values_2023 = [v[0] for v in kpi_revenue.values()]
values_2022 = [v[1] for v in kpi_revenue.values()]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=labels,
    x=values_2022,
    name="FY2022/23",
    orientation='h',
    marker_color='lightblue'
))

fig.add_trace(go.Bar(
    y=labels,
    x=values_2023,
    name="FY2023/24",
    orientation='h',
    marker_color='dodgerblue'
))

fig.update_layout(
    barmode='group',
    title="📊 Year-on-Year KPI Comparison",
    xaxis_title="Amount (SGD)",
    yaxis_title="Metric",
    height=500,
    template="plotly_dark",
    legend=dict(orientation="h", y=-0.2, x=0.3)
)

st.plotly_chart(fig, use_container_width=True)
