import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go


# --- Load Excel file ---
df = pd.read_excel('data/iras-fs-fy2324.xlsx', sheet_name='Statement of Financial Position')
clean_df = df.dropna(how='all').dropna(axis=1, how='all').reset_index(drop=True)

# Helper function that safely converts to int or returns 0
def safe_int(val):
    try:
        return int(val)
    except:
        return 0

# Extract KPI based on label search with safe handling
def extract_kpi(df, row_label, col_label='INLAND REVENUE AUTHORITY OF SINGAPORE', value_cols=('Unnamed: 4', 'Unnamed: 6')):
    row = df[df[col_label].str.contains(row_label, case=False, na=False)]
    if row.empty:
        return None, None, None
    val_new = safe_int(row[value_cols[0]].values[0])
    val_old = safe_int(row[value_cols[1]].values[0])
    pct_change = ((val_new - val_old) / val_old) * 100 if val_old != 0 else 0
    return val_new, val_old, round(pct_change, 2)

# Collect KPI results
kpi_results = {}

# Share Capital
kpi_results["Share Capital"] = extract_kpi(clean_df, "Share capital", col_label='INLAND REVENUE AUTHORITY OF SINGAPORE')

# Accumulated surplus
kpi_results["Accumulated surplus"] = extract_kpi(clean_df, "Accumulated surplus", col_label='INLAND REVENUE AUTHORITY OF SINGAPORE')

# Total Equity = Accumulated surplus + Share capital
SC_AS_2023 = df.iloc[5:7, 4].apply(safe_int).sum()  # E7 to E8 = rows 6-7
SC_AS_2022 = df.iloc[5:7, 6].apply(safe_int).sum()  # G7 to G8 = cols 6

kpi_results["Total Equity"] = (SC_AS_2023, SC_AS_2022, round((SC_AS_2023 - SC_AS_2022) / SC_AS_2022 * 100, 2))


# Non-current assets
nca_2023 = df.iloc[11:16, 4].apply(safe_int).sum()  # E13 to E17
nca_2022 = df.iloc[11:16, 6].apply(safe_int).sum()  # G13 to G17 = cols 6

kpi_results["Non-Current Assets"] = (nca_2023, nca_2022, round((nca_2023 - nca_2022) / nca_2022 * 100, 2))

# current assets
ca_2023 = df.iloc[19:23, 4].apply(safe_int).sum()  # E21 to E24 = rows 20–23
ca_2022 = df.iloc[19:23, 6].apply(safe_int).sum()  # G21 to G24 = cols 6

kpi_results["Total Current Assets"] = (ca_2023, ca_2022, round((ca_2023 - ca_2022) / ca_2022 * 100, 2))

# Current Liabilities
cl_2023 = df.iloc[28:36, 4].apply(safe_int).sum()  # E30 to E37 =
cl_2022 = df.iloc[28:36, 6].apply(safe_int).sum()  # G30 to G37 = cols 6

kpi_results["Total Current Liabilities"] = (cl_2023, cl_2022, round((cl_2023 - cl_2022) / cl_2022 * 100, 2))

# Net Current Assets
kpi_results["Net Current Assets"] = extract_kpi(clean_df, "Net current assets", col_label='INLAND REVENUE AUTHORITY OF SINGAPORE')

# Non-current liabilities
ncl_2023 = df.iloc[43:46, 4].apply(safe_int).sum()  # E45 to E47 =
ncl_2022 = df.iloc[43:46, 6].apply(safe_int).sum()  # G45 to G47 = cols 6

kpi_results["Non-Current Liabilities"] = (ncl_2023, ncl_2022, round((ncl_2023 - ncl_2022) / ncl_2022 * 100, 2))


# --- Streamlit Layout ---
st.title("📘 Statement of Financial Position")

st.caption("FY2023/24 vs FY2022/23 (Singapore IRAS)")

# METRICS/KPI

# Extract required values from kpi_results
total_equity = kpi_results["Total Equity"][0]
total_current_assets = kpi_results["Total Current Assets"][0]
non_current_assets = kpi_results["Non-Current Assets"][0]
total_current_liabilities = kpi_results["Total Current Liabilities"][0]
non_current_liabilities = kpi_results["Non-Current Liabilities"][0]

# FY2022 assets (for YoY asset growth)
total_current_assets_2022 = kpi_results["Total Current Assets"][1]
non_current_assets_2022 = kpi_results["Non-Current Assets"][1]


#  1. Equity Composition Ratio - Shows what % of assets are financed by equity (vs liabilities).
# Equity-to-Assets Ratio
equity_ratio = total_equity / (total_current_assets + non_current_assets)

st.markdown("### 🧮 Financial Health KPI")
# st.metric("Equity-to-Assets Ratio", f"{equity_ratio:.2%}")


# 2. Working Capital
# Indicates liquidity → ability to cover short-term liabilities.
working_capital = total_current_assets - total_current_liabilities


# 3. Current Ratio
# Also a liquidity ratio, useful in financial performance analysis.
current_ratio = total_current_assets / total_current_liabilities if total_current_liabilities else 0



# 4. Debt-to-Equity Ratio
# Measures financial leverage — useful for tax planning too.
total_liabilities = total_current_liabilities + non_current_liabilities
de_ratio = total_liabilities / total_equity if total_equity else 0



# 5. Year-over-Year Change in Total Assets
# Gives insight into overall growth.
assets_2023 = total_current_assets + non_current_assets
assets_2022 = total_current_assets_2022 + non_current_assets_2022
asset_growth = ((assets_2023 - assets_2022) / assets_2022 * 100) if assets_2022 else 0

# All KPI
col1, col2, col3 = st.columns(3)

with col1:
     st.markdown(f"""
<div style="padding-bottom:1rem">
    <div style="font-size:1.5rem;color:white;font-weight:800">Equity/Assets Ratio</div>
    <div style="font-size:1.5rem;font-weight:bold;color:deepskyblue">{equity_ratio:,.2%}</div>
</div>
""", unsafe_allow_html=True)

     st.markdown(f"""
<div style="padding-bottom:1rem">
    <div style="font-size:1.5rem;color:white;font-weight:800">Current Ratio</div>
    <div style="font-size:1.5rem;font-weight:bold;color:deepskyblue">{current_ratio:,.2f}</div>
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
<div style="padding-bottom:1rem">
    <div style="font-size:1.5rem;color:white;font-weight:800">Working Capital</div>
    <div style="font-size:1.5rem;font-weight:bold;color:deepskyblue">S${working_capital:,.0f}</div>
</div>
""", unsafe_allow_html=True)
    
    st.markdown(f"""
<div style="padding-bottom:1rem">
    <div style="font-size:1.5rem;color:white;font-weight:800">Debt-to-Equity Ratio</div>
    <div style="font-size:1.5rem;font-weight:bold;color:deepskyblue">{de_ratio:,.2f}</div>
</div>
""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
<div style="padding-bottom:1rem">
    <div style="font-size:1.5rem;color:white;font-weight:800">YoY Asset Growth</div>
    <div style="font-size:1.5rem;font-weight:bold;color:{'green' if asset_growth > 0 else 'red'}">{asset_growth:+.2f}%</div>
</div>
""", unsafe_allow_html=True)


# Convert KPI dictionary to DataFrame
kpi_df = pd.DataFrame.from_dict(kpi_results, orient='index', columns=["FY2023/24", "FY2022/23", "% Change"])
kpi_df.index.name = "Metric"
kpi_df = kpi_df.reset_index()
# kpi_df

def color_percent(val):
    try:
        val = float(val)
        color = "green" if val > 0 else "red" if val < 0 else "gray"
        return f"color: {color}"
    except:
        return ""

styled_df = kpi_df.style.format({
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
half = len(kpi_results) // 2

with col1:
    for label in list(kpi_results.keys())[:half]:
        v1, v2, pct = kpi_results[label]
        render_metric(label, v1, pct)

with col2:
    for label in list(kpi_results.keys())[half:]:
        v1, v2, pct = kpi_results[label]
        render_metric(label, v1, pct)


# --- KPI Bar Chart using Plotly ---
labels = list(kpi_results.keys())
values_2023 = [v[0] for v in kpi_results.values()]
values_2022 = [v[1] for v in kpi_results.values()]

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



