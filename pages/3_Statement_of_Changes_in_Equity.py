import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Load sheet
df_equity = pd.read_excel('data/iras-fs-fy2324.xlsx', sheet_name='Statement of Changes in Equity')
df_clean_equity = df_equity
# df_clean = df.dropna(how='all').dropna(axis=1, how='all').reset_index(drop=True)

# Changes in Equity
# Helper function that safely converts to int or returns 0
def safe_int(val):
    try:
        return int(val)
    except:
        return 0

# Collect KPI changes in equity results
kpi_equity = {}

# Total Comprehensive Income FY22/23

end_val = safe_int(df_clean_equity.iloc[15, 7])  # FY23/24
begin_val = safe_int(df_clean_equity.iloc[8, 7])    # FY22/23
pct_change = round(((end_val - begin_val) / begin_val) * 100, 2) if begin_val != 0 else 0

kpi_equity["Total Comprehensive Income"] = (end_val, begin_val, pct_change)


# Dividends Paid
end_val_div = safe_int(df_clean_equity.iloc[18, 7])  # FY23/24
begin_val_div = safe_int(df_clean_equity.iloc[11, 7])    # FY22/23
pct_change = round(((end_val_div - begin_val_div) / begin_val_div) * 100, 2) if begin_val_div != 0 else 0

kpi_equity["Dividends Paid"] = (end_val_div, begin_val_div, pct_change)

# kpi_equity

# # METRICS/KPI

# # Extract required values from kpi_results
# # Extract total comprehensive income
# total_comprehensive_income_2024 = kpi_equity["Total Comprehensive Income"][0]
# total_comprehensive_income_2023 = kpi_equity["Total Comprehensive Income"][1]

# # Extract dividends paid (usually negative)
# dividends_paid_2024 = kpi_equity["Dividends Paid"][0]
# dividends_paid_2023 = kpi_equity["Dividends Paid"][1]

# # These should come from `kpi_results` (statement of financial position)
# acc_surplus_2024 = kpi_equity["Accumulated surplus"][0]
# acc_surplus_2023 = kpi_equity["Accumulated surplus"][1]

# total_equity_2024 = kpi_equity["Total Equity"][0]
# total_equity_2023 = kpi_equity["Total Equity"][1]

# # 1. Total Comprehensive Income Growth
# # Already in your code as:
# total_comprehensive_income_growth = kpi_equity["Total Comprehensive Income"]

# # 2. Dividend Payout Ratio
# # Shows what % of income is paid out to stakeholders.
# # dividend_payout_ratio = abs(dividends_paid) / total_comprehensive_income
# dpr_2023 = round(abs(begin_val_div) / begin_val * 100, 2)
# dpr_2024 = round(abs(end_val_div) / end_val * 100, 2)


# # 3. Retained Earnings Growth
# # Accumulated Surplus (FY24) = Acc. Surplus (FY23) + Comprehensive Income - Dividends
# retained_earnings_growth = (acc_surplus_2024 - acc_surplus_2023) / acc_surplus_2023 * 100

# # 4. Dividends Growth
# # Show how dividend policy changed YoY:
# div_growth = (abs(end_val_div) - abs(begin_val_div)) / abs(begin_val_div) * 100

# # 5. Equity Growth from Internal Sources
# # Compare Equity increase vs. Share Capital (which remains constant). So, the increase is due to retained profit:
# internal_equity_growth = (total_equity_2024 - total_equity_2023) / total_equity_2023 * 100

# st.markdown("### 💼 Changes in Equity KPIs")

# # All KPI
# col1, col2, col3 = st.columns(3)

# with col1:
#      st.markdown(f"""
# <div style="padding-bottom:1rem">
#     <div style="font-size:1.5rem;color:white;font-weight:800">Income Growth</div>
#     <div style="font-size:1.5rem;font-weight:bold;color:deepskyblue">{total_comprehensive_income_growth:,.2%}</div>
# </div>
# """, unsafe_allow_html=True)

#      st.markdown(f"""
# <div style="padding-bottom:1rem">
#     <div style="font-size:1.5rem;color:white;font-weight:800">Dividend Payout Ratio</div>
#     <div style="font-size:1.5rem;font-weight:bold;color:deepskyblue">{dpr_2023:,.2f}</div>
# </div>
# """, unsafe_allow_html=True)

# with col2:
#     st.markdown(f"""
# <div style="padding-bottom:1rem">
#     <div style="font-size:1.5rem;color:white;font-weight:800">Dividend Payout Ratio</div>
#     <div style="font-size:1.5rem;font-weight:bold;color:deepskyblue">{dpr_2024:,.2f}</div>
# </div>
# """, unsafe_allow_html=True)
    
#     st.markdown(f"""
# <div style="padding-bottom:1rem">
#     <div style="font-size:1.5rem;color:white;font-weight:800">Retained Earnings Growth</div>
#     <div style="font-size:1.5rem;font-weight:bold;color:deepskyblue">{retained_earnings_growth:,.2f}</div>
# </div>
# """, unsafe_allow_html=True)

# with col3:
#     st.markdown(f"""
# <div style="padding-bottom:1rem">
#     <div style="font-size:1.5rem;color:white;font-weight:800">Dividends Growth</div>
#     <div style="font-size:1.5rem;font-weight:bold;color:deepskyblue">{div_growth:,.2f}</div>
# </div>
# """, unsafe_allow_html=True)
    
#     st.markdown(f"""
# <div style="padding-bottom:1rem">
#     <div style="font-size:1.5rem;color:white;font-weight:800">Equity Growth from Internal Sources</div>
#     <div style="font-size:1.5rem;font-weight:bold;color:{'green' if internal_equity_growth > 0 else 'red'}">{internal_equity_growth:+.2f}%</div>
# </div>
# """, unsafe_allow_html=True)



# --- Streamlit Layout ---
st.title("📘 Statement of Changes in Equity")

st.caption("FY2023/24 vs FY2022/23 (Singapore IRAS)")

# Convert KPI dictionary to DataFrame - just a normal table without +/- in green/red
kpi_df_equity = pd.DataFrame.from_dict(kpi_equity, orient='index', columns=["FY2023/24", "FY2022/23", "% Change"])
kpi_df_equity.index.name = "Metric"
kpi_df_equity = kpi_df_equity.reset_index()
# kpi_df_equity

def color_percent(val):
    try:
        val = float(val)
        color = "green" if val > 0 else "red" if val < 0 else "gray"
        return f"color: {color}"
    except:
        return ""

styled_df = kpi_df_equity.style.format({
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
half = len(kpi_equity) // 2

with col1:
    for label in list(kpi_equity.keys())[:half]:
        v1, v2, pct = kpi_equity[label]
        render_metric(label, v1, pct)

with col2:
    for label in list(kpi_equity.keys())[half:]:
        v1, v2, pct = kpi_equity[label]
        render_metric(label, v1, pct)

# --- KPI Bar Chart using Plotly ---
labels = list(kpi_equity.keys())
values_2023 = [v[0] for v in kpi_equity.values()]
values_2022 = [v[1] for v in kpi_equity.values()]

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
