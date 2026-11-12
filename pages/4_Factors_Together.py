from pathlib import Path

import pandas as pd
import streamlit as st
from lifelines import CoxPHFitter

from analysis_groups import prepare_analysis_groups, GRADE_GROUPS

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "seer_breast_cancer_cleaned.csv"

LABELS = {
    "age_per_10_years": "Age (per 10 years)",
    "T2": "Tumor T2 (vs T1)",
    "T3": "Tumor T3 (vs T1)",
    "T4": "Tumor T4 (vs T1)",
    "N2": "Lymph nodes N2 (vs N1)",
    "N3": "Lymph nodes N3 (vs N1)",
    "grade_II": "Grade II (vs I)",
    "grade_III_IV": "Grade III–IV (vs I)",
    "hormone_negative": "Hormone negative (vs positive)",
    "race_black": "Race: Black (vs White)",
    "race_other": "Race: Other (vs White)",
}

@st.cache_data
def load_model_data(path):
    df = prepare_analysis_groups(pd.read_csv(path))

    model_df = pd.DataFrame()
    model_df["months"] = df["Survival Months"]
    model_df["event"] = df["Death Event"].astype(int)
    model_df["age_per_10_years"] = df["Age"] / 10

    model_df["T2"] = (df["T Stage"] == "T2").astype(int)
    model_df["T3"] = (df["T Stage"] == "T3").astype(int)
    model_df["T4"] = (df["T Stage"] == "T4").astype(int)

    model_df["N2"] = (df["N Stage"] == "N2").astype(int)
    model_df["N3"] = (df["N Stage"] == "N3").astype(int)

    model_df["grade_II"] = (df["Grade Group"] == GRADE_GROUPS[1]).astype(int)
    model_df["grade_III_IV"] = (df["Grade Group"] == GRADE_GROUPS[2]).astype(int)

    model_df["hormone_negative"] = (df["Hormone Status"] == "Negative").astype(int)

    model_df["race_black"] = (df["Race"] == "Black").astype(int)
    model_df["race_other"] = df["Race"].str.startswith("Other").astype(int)

    is_distant = df["A Stage"] == "Distant"
    return model_df, is_distant

@st.cache_data
def fit_cox(model_df):
    cph = CoxPHFitter()
    cph.fit(model_df, duration_col="months", event_col="event")
    results = cph.summary[["exp(coef)", "exp(coef) lower 95%", "exp(coef) upper 95%", "p"]]
    results.columns = ["Hazard ratio", "Lower 95%", "Upper 95%", "p-value"]
    results.index = [LABELS[name] for name in results.index]
    return results

st.title("Factors Together")
st.write(
    "The other pages look at one factor at a time. This page uses a Cox model "
    "to look at all factors together and shows how much each one changes the risk of death."
)

model_df, is_distant = load_model_data(DATA_PATH)
results = fit_cox(model_df)

st.subheader("Hazard Ratios")
st.dataframe(results.round(2))
