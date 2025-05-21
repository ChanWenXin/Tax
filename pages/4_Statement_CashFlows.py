import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Load sheet
df_cashflow = pd.read_excel('data/iras-fs-fy2324.xlsx', sheet_name='Statement of Cash Flows')
clean_df_cashflow = df_cashflow
# df_clean = df.dropna(how='all').dropna(axis=1, how='all').reset_index(drop=True)

# Cash Flows Statement
# Fix the issue by using a fallback method to safely extract and clean values

# Helper function that safely converts to int or returns 0
def safe_int(val):
    try:
        return int(val)
    except:
        return 0

# Re-run KPI extraction with safe handling
def extract_kpi_cashflow(df, row_keyword, value_cols=('Unnamed: 5', 'Unnamed: 7')):
    label_cols = ['INLAND REVENUE AUTHORITY OF SINGAPORE', 'Unnamed: 1', 'Unnamed: 2']
    
    df['combined_label'] = df[label_cols].astype(str).agg(' '.join, axis=1)
    
    row = df[df['combined_label'].str.lower().str.contains(row_keyword.lower(), regex=False)]
    
    if row.empty:
        return None, None, None

    val_new = safe_int(row[value_cols[0]].values[0])
    val_old = safe_int(row[value_cols[1]].values[0])
    pct_change = ((val_new - val_old) / val_old) * 100 if val_old != 0 else 0
    
    return val_new, val_old, round(pct_change, 2)

# Collect KPI revenue results
kpi_cashflow = {}

# Net Cash from Operating Activities
kpi_cashflow["Net Cash from Operating Activities"] = extract_kpi_cashflow(clean_df_cashflow, "Net cash from operating activities")

# Net Cash Used in Investing Activities	
kpi_cashflow["Net Cash from Investing Activities"] = extract_kpi_cashflow(clean_df_cashflow, "Net cash used in investing activities")

# Net Cash Used in Financing Activities
kpi_cashflow["Net Cash from Financing Activities"] = extract_kpi_cashflow(clean_df_cashflow, "Net cash used in financing activities")

# Net Cash Movement
kpi_cashflow["Net Cash Movement"] = extract_kpi_cashflow(clean_df_cashflow, "Net (decrease)/increase in cash and cash equivalents")

# Beginning Cash
end_val = safe_int(clean_df_cashflow.iloc[27, 5])  # New
begin_val = safe_int(clean_df_cashflow.iloc[27, 7])    # Old
pct_change = round(((end_val - begin_val) / begin_val) * 100, 2) if begin_val != 0 else 0

kpi_cashflow["Beginning Cash"] = (end_val, begin_val, pct_change)


# Ending Cash
ending_val = safe_int(clean_df_cashflow.iloc[29, 5])  # New
starting_val = safe_int(clean_df_cashflow.iloc[29, 7])    # Old
pct_change_ending = round(((ending_val - starting_val) / starting_val) * 100, 2) if starting_val != 0 else 0

kpi_cashflow["Ending Cash"] = (ending_val, starting_val, pct_change_ending)

# kpi_cashflow


# --- Streamlit Layout ---
st.title("📘 Statement of Cash Flows")

st.caption("FY2023/24 vs FY2022/23 (Singapore IRAS)")

# Convert KPI dictionary to DataFrame - just a normal table without +/- in green/red
kpi_df_cashflow = pd.DataFrame.from_dict(kpi_cashflow, orient='index', columns=["FY2023/24", "FY2022/23", "% Change"])
kpi_df_cashflow.index.name = "Metric"
kpi_df_cashflow = kpi_df_cashflow.reset_index()
# kpi_df_cashflow


# METRICS/KPI

# Extract required values from kpi_results
# Extract values from kpi_cashflow dictionary
cf_operating = kpi_cashflow["Net Cash from Operating Activities"][0]
cf_investing = kpi_cashflow["Net Cash from Investing Activities"][0]
cf_financing = kpi_cashflow["Net Cash from Financing Activities"][0]
beginning_cash = kpi_cashflow["Beginning Cash"][0]
ending_cash = kpi_cashflow["Ending Cash"][0]
net_cash_movement = kpi_cashflow["Net Cash Movement"][0]

# Optional: Get CAPEX (as approximation)
capex = safe_int(clean_df_cashflow.iloc[15, 5]) + safe_int(clean_df_cashflow.iloc[16, 5])

# 1. Free Cash Flow (Operating - CAPEX)
free_cash_flow = cf_operating - capex

# 2. Cash Flow Coverage Ratio
cash_flow_coverage = cf_operating / abs(cf_financing) if cf_financing != 0 else 0

# 3. Net Cash Flow Margin (Relative to Beginning Cash)
net_cash_margin = net_cash_movement / beginning_cash if beginning_cash != 0 else 0

# 4. Cash Burn Rate (If Operating Cash Flow is negative)
cash_burn_rate = abs(cf_operating) / 12 if cf_operating < 0 else 0

# 5. Runway (Months company can survive using Ending Cash)
monthly_expense_estimate = abs(cf_operating) / 12  # Simplified estimate
runway_months = ending_cash / monthly_expense_estimate if monthly_expense_estimate != 0 else 0

# st.markdown("### 💸 Cash Flow KPIs")
# st.metric("Free Cash Flow", f"S${free_cash_flow:,.0f}")
# st.metric("Cash Flow Coverage Ratio", f"{cash_flow_coverage:.2f}")
# st.metric("Net Cash Margin", f"{net_cash_margin:.2%}")
# st.metric("Cash Burn Rate", f"S${cash_burn_rate:,.0f}/month")
# st.metric("Cash Runway", f"{runway_months:.1f} months")

# All KPI
col1, col2, col3 = st.columns(3)

with col1:
     st.markdown(f"""
<div style="padding-bottom:1rem">
    <div style="font-size:1.5rem;color:white;font-weight:800">Free Cash Flow</div>
    <div style="font-size:1.5rem;font-weight:bold;color:deepskyblue">S${free_cash_flow:,.0f}</div>
</div>
""", unsafe_allow_html=True)

     st.markdown(f"""
<div style="padding-bottom:1rem">
    <div style="font-size:1.5rem;color:white;font-weight:800">Cash Flow Coverage Ratio</div>
    <div style="font-size:1.5rem;font-weight:bold;color:deepskyblue">{cash_flow_coverage:,.2f}</div>
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
<div style="padding-bottom:1rem">
    <div style="font-size:1.5rem;color:white;font-weight:800">Net Cash Margin</div>
    <div style="font-size:1.5rem;font-weight:bold;color:deepskyblue">{net_cash_margin:,.2%}</div>
</div>
""", unsafe_allow_html=True)
    
if cash_burn_rate > 0:
    burn_rate_display = f"S${cash_burn_rate:,.0f} / month"
else:
    burn_rate_display = "Not applicable (positive OCF)"

st.markdown(f"""
<div style="padding-bottom:1rem">
    <div style="font-size:1.5rem;color:white;font-weight:800">Cash Burn Rate</div>
    <div style="font-size:1.5rem;font-weight:bold;color:deepskyblue">{burn_rate_display}</div>
</div>
""", unsafe_allow_html=True)


with col3:
    st.markdown(f"""
<div style="padding-bottom:1rem">
    <div style="font-size:1.5rem;color:white;font-weight:800">Cash Runway</div>
    <div style="font-size:1.5rem;font-weight:bold;color:deepskyblue">{runway_months:,.1f} months</div>
</div>
""", unsafe_allow_html=True)


# --- Streamlit Layout ---
st.title("📘 Statement of Cash Flows")

st.caption("FY2023/24 vs FY2022/23 (Singapore IRAS)")

def color_percent(val):
    try:
        val = float(val)
        color = "green" if val > 0 else "red" if val < 0 else "gray"
        return f"color: {color}"
    except:
        return ""

styled_df = kpi_df_cashflow.style.format({
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
half = len(kpi_cashflow) // 2

with col1:
    for label in list(kpi_cashflow.keys())[:half]:
        v1, v2, pct = kpi_cashflow[label]
        render_metric(label, v1, pct)

with col2:
    for label in list(kpi_cashflow.keys())[half:]:
        v1, v2, pct = kpi_cashflow[label]
        render_metric(label, v1, pct)

# --- KPI Bar Chart using Plotly ---
labels = list(kpi_cashflow.keys())
values_2023 = [v[0] for v in kpi_cashflow.values()]
values_2022 = [v[1] for v in kpi_cashflow.values()]

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