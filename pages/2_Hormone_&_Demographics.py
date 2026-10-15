from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


RECEPTORS = ["Estrogen Status", "Progesterone Status"]
STATUSES = ["Positive", "Negative"]
COLORS = {"Positive": "#277DA8", "Negative": "#F4A261"}
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "seer_breast_cancer_cleaned.csv"


@st.cache_data
def load_data(path):
    return pd.read_csv(path)


def show_group_comparison(df, group):
    """Compare receptor proportions within each demographic or grade group."""
    columns = st.columns(2)
    for column, receptor in zip(columns, RECEPTORS):
        counts = pd.crosstab(df[group], df[receptor]).reindex(
            columns=STATUSES, fill_value=0
        )
        totals = counts.sum(axis=1)
        percentages = counts.div(totals.replace(0, float("nan")), axis=0) * 100
        percentages.index = [f"{label} (n={total:,})" for label, total in totals.items()]
        percentages.index.name = group
        chart_data = percentages.reset_index().melt(
            id_vars=group, var_name="Receptor status", value_name="Percent"
        )
        figure = px.bar(
            chart_data, x="Percent", y=group, color="Receptor status",
            orientation="h", barmode="stack", title=f"{receptor} by {group.lower()}",
            color_discrete_map=COLORS, category_orders={"Receptor status": STATUSES},
            range_x=[0, 100], height=max(360, len(totals) * 65 + 150),
        )
        figure.update_layout(yaxis_title=None, xaxis_title="Percent within group")
        column.plotly_chart(figure, width="stretch")


def main():
    st.title("Hormone & Demographics")
    st.write(
        "Explore estrogen and progesterone receptor status and how their distributions "
        "vary with age, race, marital status, and tumor grade."
    )
    if not DATA_PATH.exists():
        st.error("Cleaned dataset not found. Add data/seer_breast_cancer_cleaned.csv to the project.")
        st.stop()
    df = load_data(DATA_PATH)
    required = RECEPTORS + ["Age", "Race", "Marital Status", "Grade"]
    missing = [name for name in required if name not in df.columns]
    if missing:
        st.error(f"The dataset is missing required columns: {', '.join(missing)}")
        st.stop()

    st.subheader("Receptor Status")
    for column, receptor in zip(st.columns(2), RECEPTORS):
        counts = df[receptor].value_counts().reindex(STATUSES, fill_value=0)
        chart_data = counts.rename_axis("Receptor status").reset_index(name="Patients")
        figure = px.bar(
            chart_data, x="Receptor status", y="Patients", color="Receptor status",
            text="Patients", title=receptor, color_discrete_map=COLORS,
            category_orders={"Receptor status": STATUSES},
        )
        column.plotly_chart(figure, width="stretch")
        valid_total = counts.sum()
        if valid_total:
            column.caption(f"{counts['Positive'] / valid_total:.1%} positive among patients with recorded positive/negative status.")

    st.subheader("Age by Receptor Status")
    for column, receptor in zip(st.columns(2), RECEPTORS):
        figure = px.box(
            df[df[receptor].isin(STATUSES)], x=receptor, y="Age", color=receptor,
            title=f"Age by {receptor.lower()}", color_discrete_map=COLORS,
            category_orders={receptor: STATUSES}, labels={"Age": "Age (years)"},
        )
        column.plotly_chart(figure, width="stretch")

    for group in ["Race", "Marital Status", "Grade"]:
        st.subheader(f"Receptor Status by {group}")
        show_group_comparison(df, group)

    st.caption(
        "Group percentages use patients with both the group value and a recorded positive/negative "
        "receptor status; n is that denominator. Age plots omit missing ages. "
        "These comparisons describe this dataset and do not establish causation or survival effects."
    )


if __name__ == "__main__":
    main()
