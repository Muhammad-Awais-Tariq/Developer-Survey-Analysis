import streamlit as st
import pandas as pd
from main import (
    get_required_info,
    replace_multiselect,
    split_multicolumn,
    convert_numeric,
    drop_incorrect,
    plot_hbar,
    plot_bar,
    plot_hist,
    plot_pie,
    plot_barh
)

st.set_page_config(page_title="Stack Overflow Survey Analysis", page_icon="📊", layout="wide")

st.title("📊 Stack Overflow Survey Analysis")
st.caption("Upload the Stack Overflow developer survey CSV to explore insights.")

uploaded_file = st.file_uploader("Upload survey CSV", type=["csv"])

if uploaded_file is None:
    st.info("Upload a CSV file to get started.")
    st.stop()

raw_df = pd.read_csv(uploaded_file)

required_columns = [
    'Country', 'Age', 'Gender', 'EdLevel', 'UndergradMajor', 'Hobbyist',
    'Age1stCode', 'YearsCode', 'YearsCodePro', 'LanguageWorkedWith',
    'LanguageDesireNextYear', 'NEWLearn', 'NEWStuck', 'Employment', 'DevType',
    'WorkWeekHrs', 'JobSat', 'JobFactors', 'NEWOvertime', 'NEWEdImpt'
]
missing_cols = [c for c in required_columns if c not in raw_df.columns]
if missing_cols:
    st.error(f"Missing required columns: {missing_cols}")
    st.stop()

survey_df = get_required_info(raw_df)
convert_numeric(survey_df, "Age1stCode")
convert_numeric(survey_df, "YearsCode")
convert_numeric(survey_df, "YearsCodePro")
convert_numeric(survey_df, "WorkWeekHrs")
convert_numeric(survey_df, "Age")
drop_incorrect(survey_df, "Age", max=100, min=10)
drop_incorrect(survey_df, "WorkWeekHrs", max=140)

tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Demographics", "Languages", "Work & Career"])

with tab1:
    st.subheader("Dataset Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Respondents", f"{len(survey_df):,}")
    c2.metric("Columns", len(survey_df.columns))
    c3.metric("Missing Values", f"{int(survey_df.isnull().sum().sum()):,}")
    c4.metric("Countries", survey_df["Country"].nunique())

    st.subheader("Data Preview")
    st.dataframe(survey_df.head(10), width='stretch')

    with st.expander("Statistical Summary"):
        st.dataframe(survey_df.describe(), width='stretch')

with tab2:
    st.subheader("Gender Distribution")
    gender_df = survey_df.copy()
    replace_multiselect(gender_df, "Gender")
    st.image(plot_hbar(gender_df, "Gender", "Gender Distribution") )

    st.subheader("Education Level")
    st.image(plot_hbar(survey_df, "EdLevel", "Education Level") )

    st.subheader("Age When They First Coded")
    st.image(plot_hist(survey_df, "Age1stCode", "Age at First Code"))

with tab3:
    st.subheader("Programming Languages")
    lang_choice = st.radio(
        "Select view:",
        ["Most Used This Year", "Most Desired Next Year", "Most Loved"],
        horizontal=True
    )

    if lang_choice == "Most Used This Year":
        pct = split_multicolumn(survey_df["LanguageWorkedWith"]).mean().sort_values(ascending=False) * 100
        title = "Most Used Languages This Year"
    elif lang_choice == "Most Desired Next Year":
        pct = split_multicolumn(survey_df["LanguageDesireNextYear"]).mean().sort_values(ascending=False) * 100
        title = "Most Desired Languages Next Year"
    else:
        worked  = split_multicolumn(survey_df["LanguageWorkedWith"])
        desired = split_multicolumn(survey_df["LanguageDesireNextYear"])
        common_langs = [c for c in worked.columns if c in desired.columns]
        pct = (worked[common_langs] & desired[common_langs]).mean().sort_values(ascending=False) * 100
        title = "Most Loved Languages"

    top5 = pct.head(5)
    st.image(plot_pie(top5.values, top5.index, title))

with tab4:
    st.subheader("Countries with Highest Avg Work Hours")
    st.caption("Only countries with 250+ responses included.")

    country_counts = survey_df["Country"].value_counts()
    valid_countries = country_counts[country_counts > 250].index
    work_hrs_df = (
        survey_df[survey_df["Country"].isin(valid_countries)]
        .groupby("Country")["WorkWeekHrs"]
        .mean()
        .sort_values(ascending=False)
        .head(15)
    )

    if work_hrs_df.empty:
        st.warning("Not enough responses per country (needs 250+).")
    else:
        st.image(plot_barh(work_hrs_df, "Avg Work Hours per Week by Country"))

    st.subheader("Top 15 Countries by Respondents")
    st.image(plot_bar(survey_df, "Country", "Top 15 Countries", total_num=15))

    st.subheader("Job Satisfaction")
    st.image(plot_hbar(survey_df, "JobSat", "Job Satisfaction"))

    st.subheader("Employment Type")
    st.image(plot_hbar(survey_df, "Employment", "Employment Type"))