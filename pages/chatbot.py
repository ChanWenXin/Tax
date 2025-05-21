import pandas as pd
import streamlit as st
from openai import OpenAI
import os


st.set_page_config(page_title="📊 KPI Chatbot", layout="wide")

excel_path = "data/iras-fs-fy2324.xlsx"

# --- Utilities ---
def safe_int(val):
    try:
        return int(val)
    except:
        return 0

def build_kpi_entry(val_new, val_old):
    return {
        "FY2023/24": val_new,
        "FY2022/23": val_old,
        "Change (%)": round((val_new - val_old) / val_old * 100, 2) if val_old else 0
    }

# --- Extractor 1: Financial Position ---
def extract_kpi_financial_position(sheet_name="Statement of Financial Position"):
    df = pd.read_excel(excel_path, sheet_name=sheet_name)
    clean_df = df.dropna(how='all').dropna(axis=1, how='all').reset_index(drop=True)

    def extract_kpi(row_label, col_label='INLAND REVENUE AUTHORITY OF SINGAPORE'):
        row = clean_df[clean_df[col_label].astype(str).str.contains(row_label, case=False, na=False)]
        if row.empty:
            return None
        val_new = safe_int(row["Unnamed: 4"].values[0])
        val_old = safe_int(row["Unnamed: 6"].values[0])
        return build_kpi_entry(val_new, val_old)

    kpi = {
        "Share Capital": extract_kpi("Share capital"),
        "Accumulated Surplus": extract_kpi("Accumulated surplus"),
        "Net Current Assets": extract_kpi("Net current assets"),
        "Total Equity": build_kpi_entry(safe_int(df.iloc[6, 4]) + safe_int(df.iloc[5, 4]),
                                        safe_int(df.iloc[6, 6]) + safe_int(df.iloc[5, 6])),
        "Non-Current Assets": build_kpi_entry(df.iloc[11:16, 4].apply(safe_int).sum(),
                                              df.iloc[11:16, 6].apply(safe_int).sum()),
        "Total Current Assets": build_kpi_entry(df.iloc[19:23, 4].apply(safe_int).sum(),
                                                df.iloc[19:23, 6].apply(safe_int).sum()),
        "Total Current Liabilities": build_kpi_entry(df.iloc[28:36, 4].apply(safe_int).sum(),
                                                     df.iloc[28:36, 6].apply(safe_int).sum()),
        "Non-Current Liabilities": build_kpi_entry(df.iloc[43:46, 4].apply(safe_int).sum(),
                                                   df.iloc[43:46, 6].apply(safe_int).sum())
    }

    return kpi

# --- Extractor 2: Income Statement ---
def extract_kpi_com_income(sheet_name="Statement of Com. Income"):
    df = pd.read_excel(excel_path, sheet_name=sheet_name)
    clean_df = df

    def extract_kpi(row_label, col_label='INLAND REVENUE AUTHORITY OF SINGAPORE'):
        row = clean_df[clean_df[col_label].astype(str).str.contains(row_label, case=False, na=False)]
        if row.empty:
            return None
        val_new = safe_int(row["Unnamed: 4"].values[0])
        val_old = safe_int(row["Unnamed: 6"].values[0])
        return build_kpi_entry(val_new, val_old)

    kpi = {
        "Operating Income": build_kpi_entry(clean_df.iloc[6:8, 4].apply(safe_int).sum(),
                                            clean_df.iloc[6:8, 6].apply(safe_int).sum()),
        "Total Operating Expenditure": build_kpi_entry(clean_df.iloc[12:23, 4].apply(safe_int).sum(),
                                                       clean_df.iloc[12:23, 6].apply(safe_int).sum()),
        "Operating Surplus": extract_kpi("Operating surplus"),
        "Net Investment Income/(Loss)": build_kpi_entry(safe_int(clean_df.iloc[27, 4]),
                                                        safe_int(clean_df.iloc[27, 6])),
        "Surplus Before Gov Fund": extract_kpi("Government Consolidated Fund"),
        "Contribution to Gov Fund": extract_kpi("Contribution to Government Consolidated Fund"),
        "Net Surplus for the Year": extract_kpi("comprehensive income for the financial year")
    }

    return kpi

# --- Extractor 3: Cash Flow Statement ---
def extract_kpi_cashflow(sheet_name="Statement of Cash Flows"):
    df = pd.read_excel(excel_path, sheet_name=sheet_name)
    clean_df = df
    label_cols = ['INLAND REVENUE AUTHORITY OF SINGAPORE', 'Unnamed: 1', 'Unnamed: 2']
    clean_df['combined_label'] = clean_df[label_cols].astype(str).agg(' '.join, axis=1)

    def extract_kpi(row_label):
        row = clean_df[clean_df['combined_label'].str.lower().str.contains(row_label.lower(), regex=False)]
        if row.empty:
            return build_kpi_entry(0, 0)
        val_new = safe_int(row["Unnamed: 5"].values[0])
        val_old = safe_int(row["Unnamed: 7"].values[0])
        return build_kpi_entry(val_new, val_old)

    kpi = {
        "Net Cash from Operating Activities": extract_kpi("Net cash from operating activities"),
        "Net Cash from Investing Activities": extract_kpi("Net cash used in investing activities"),
        "Net Cash from Financing Activities": extract_kpi("Net cash used in financing activities"),
        "Net Cash Movement": extract_kpi("Net (decrease)/increase in cash and cash equivalents"),
        "Beginning Cash": build_kpi_entry(safe_int(clean_df.iloc[27, 5]), safe_int(clean_df.iloc[27, 7])),
        "Ending Cash": build_kpi_entry(safe_int(clean_df.iloc[29, 5]), safe_int(clean_df.iloc[29, 7]))
    }

    return kpi

# --- Dispatcher ---
def extract_all_kpis(selected_report):
    if selected_report == "Statement of Financial Position":
        return extract_kpi_financial_position()
    elif selected_report == "Statement of Com. Income":
        return extract_kpi_com_income()
    elif selected_report == "Statement of Cash Flows":
        return extract_kpi_cashflow()
    else:
        return {"error": "Report not recognized"}

def format_kpi_dict(kpi_dict):
    return "\n".join(
        f"{metric}: FY2023/24 = {data['FY2023/24']:,}, FY2022/23 = {data['FY2022/23']:,}, Change = {data['Change (%)']}%"
        for metric, data in kpi_dict.items()
        if isinstance(data, dict)
    )

# Checking the KPI dictionary
# st.write(extract_kpi_financial_position(sheet_name="Statement of Financial Position"))

# st.write(extract_kpi_com_income(sheet_name="Statement of Com. Income"))

# st.write(extract_kpi_cashflow(sheet_name="Statement of Cash Flows"))
# --- Streamlit UI ---
st.title("💬 Ask Me About KPIs")

# OpenAPI Key
openai.api_key = st.secrets["openai_api_key"]

# Select report
report_options = [
    "Statement of Financial Position",
    "Statement of Com. Income",
    "Statement of Cash Flows"
]
selected_report = st.selectbox("📄 Select a financial report:", report_options)
report_kpi_raw = extract_all_kpis(selected_report)
report_kpi = format_kpi_dict(report_kpi_raw)

# User question
question = st.text_input("💬 Ask a question about KPI or the financial report")

# Inject context
system_prompt = f"""
You are a financial analyst. The user selected the report: {selected_report}.

Below is the KPI summary for that report. Each line includes the metric name, the value for FY2023/24, the value for FY2022/23, and the % change.

Format:
"Metric: FY2023/24 = X, FY2022/23 = Y, Change = Z%"

Use this data to explain the user's questions correctly and clearly.

KPI Summary:
{report_kpi}
"""

# Call OpenAI
if question and openai_api_key:
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
    )
    st.markdown(f"**Answer:** {response.choices[0].message.content}")
