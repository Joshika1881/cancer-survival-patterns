from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

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


def show_group_comparison(df, group):
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
    figure = px.bar(
        chart_data, x=group, y="Percent", color="Hormone Status",
        barmode="stack", title=f"Hormone Status by {group}",
        category_orders={"Hormone Status": STATUSES}, range_y=[0, 100],
    )
    st.plotly_chart(figure, use_container_width=True)
    st.write("This chart compares positive and negative hormone status within each group. Group sizes are shown in the labels.")
    if group == "Race":
        st.caption("Other includes American Indian/Alaska Native and Asian/Pacific Islander patients.")
    elif group == "Age Group":
        st.caption("Age groups: under 50, 50–59, and 60–69. Other ages and missing ages are excluded from this chart.")
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
    st.subheader("5-Year Outcome")
    outcome = df["5-Year Death Outcome"]
    columns = st.columns(3)
    columns[0].metric("Death by 60 months (1)", int(outcome.eq(1).sum()))
    columns[1].metric("Alive at 60 months (0)", int(outcome.eq(0).sum()))
    columns[2].metric("Unknown at 60 months", int(outcome.isna().sum()))
    st.write("Death by 60 months = 1; alive at 60 months = 0. Patients last seen alive before 60 months have an unknown outcome. These counts are not a survival-rate estimate.")
    st.subheader("Hormone Status")
    counts = df["Hormone Status"].value_counts().reindex(STATUSES, fill_value=0)
    chart_data = counts.rename_axis("Hormone Status").reset_index(name="Patients")
    figure = px.bar(
        chart_data, x="Hormone Status", y="Patients", text="Patients",
        title="Hormone Status", category_orders={"Hormone Status": STATUSES},
    )
    st.plotly_chart(figure, use_container_width=True)
    st.write("Hormone status is positive if ER or PR is positive, and negative if both are negative.")

    for group in ["Age Group", "Race", "Marital Status", "Grade Group", "Stage", "Stage Group"]:
        st.subheader(f"Hormone Status by {group}")
        show_group_comparison(df, group)
    st.caption("Comparisons describe this dataset and do not establish causes or survival effects.")


if __name__ == "__main__":
    main()
