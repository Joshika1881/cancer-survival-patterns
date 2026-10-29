from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
from lifelines import KaplanMeierFitter

from analysis_groups import prepare_analysis_groups


STATUSES = ["Positive", "Negative"]
LABELS = {
    "Other (American Indian/AK Native, Asian/Pacific Islander)": "Other*",
    "Married (including common law)": "Married",
    "Single (never married)": "Single",
    "Well differentiated; Grade I": "Grade I",
    "Moderately differentiated; Grade II": "Grade II",
    "Poorly differentiated; Grade III": "Grade III",
    "Undifferentiated; anaplastic; Grade IV": "Grade IV",
}
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "seer_breast_cancer_cleaned.csv"


@st.cache_data
def load_data(path):
    return pd.read_csv(path)


def show_group_comparison(df, group, status="Both"):
    counts = pd.crosstab(df[group], df["Hormone Status"]).reindex(
        columns=STATUSES, fill_value=0
    )
    totals = counts.sum(axis=1)
    percentages = counts.div(totals.replace(0, float("nan")), axis=0) * 100
    percentages.index = [
        f"{LABELS.get(label, label)} (n={total:,})"
        for label, total in totals.items()
    ]
    percentages.index.name = group
    chart_data = percentages.reset_index().melt(
        id_vars=group, var_name="Hormone Status", value_name="Percent"
    )
    if status != "Both":
        chart_data = chart_data[chart_data["Hormone Status"] == status]
    figure = px.bar(
        chart_data, x=group, y="Percent", color="Hormone Status",
        barmode="stack", title=f"Hormone Status by {group}",
        category_orders={"Hormone Status": STATUSES}, range_y=[0, 100],
    )
    st.plotly_chart(figure, use_container_width=True)
    st.write("Percentages use all patients with known hormone status in each group. Group sizes are shown in the labels.")
    if group == "Race":
        st.caption("Other includes American Indian/Alaska Native and Asian/Pacific Islander patients.")
    elif group == "Age Group":
        st.caption("Age groups: under 50, 50–59, and 60–69.")
    elif group == "Grade Group":
        st.caption("Grades III and IV are combined because Grade IV has a small sample.")



def main():
    st.title("Hormone & Demographics")
    st.write(
        "Explore combined hormone receptor status and how its distribution "
        "varies with age, race, marital status, tumor grade, and stage."
    )
    if not DATA_PATH.exists():
        st.error("Cleaned dataset not found. Add data/seer_breast_cancer_cleaned.csv to the project.")
        st.stop()
    df = load_data(DATA_PATH)
    required = ["Estrogen Status", "Progesterone Status", "Age", "Race", "Marital Status", "Grade", "6th Stage", "Status", "Survival Months"]
    missing = [name for name in required if name not in df.columns]
    if missing:
        st.error(f"The dataset is missing required columns: {', '.join(missing)}")
        st.stop()

    df = prepare_analysis_groups(df)
    st.subheader("Overall Survival")
    months = pd.to_numeric(df["Survival Months"], errors="coerce")
    valid = months.ge(0) & df["Death Event"].notna()
    columns = st.columns(3)
    columns[0].metric("Dead (1)", int(df["Death Event"].eq(1).sum()))
    columns[1].metric("Alive (0)", int(df["Death Event"].eq(0).sum()))
    if valid.any():
        kmf = KaplanMeierFitter()
        kmf.fit(months[valid], df.loc[valid, "Death Event"].astype(int))
        five_year = kmf.survival_function_at_times(60).iloc[0]
        columns[2].metric("5-year survival", f"{five_year * 100:.1f}%")
    st.write("Dead = 1 and Alive = 0 at the last follow-up. Five-year overall survival is estimated at 60 months using Kaplan–Meier, as on the Stage Survival page. Patients last seen alive are censored at their recorded follow-up time.")
    st.subheader("Hormone Status")
    counts = df["Hormone Status"].value_counts().reindex(STATUSES, fill_value=0)
    chart_data = counts.rename_axis("Hormone Status").reset_index(name="Patients")
    figure = px.bar(
        chart_data, x="Hormone Status", y="Patients", text="Patients",
        title="Hormone Status", category_orders={"Hormone Status": STATUSES},
    )
    st.plotly_chart(figure, use_container_width=True)
    st.write("Hormone status is positive if ER or PR is positive, and negative if both are negative.")

    st.subheader("Compare Hormone Status")
    group = st.selectbox(
        "Compare by:",
        ["Age Group", "Race", "Marital Status", "Grade Group", "Stage", "Stage Group"],
    )
    status = st.selectbox("Show hormone status:", ["Both", "Positive", "Negative"])
    show_group_comparison(df, group, status)
    st.caption("Comparisons describe this dataset and do not establish causes or survival effects.")


if __name__ == "__main__":
    main()
