import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from lifelines import KaplanMeierFitter
from lifelines.statistics import multivariate_logrank_test

COLORS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]
BANDS = ["rgba(42,120,214,0.15)", "rgba(235,104,52,0.15)", "rgba(27,175,122,0.15)",
         "rgba(237,161,0,0.15)", "rgba(232,123,164,0.15)"]

st.title("Cancer Stage and Survival")
st.write(
    "How does survival differ by cancer stage, tumor stage (T) and lymph node stage (N)? "
    "Survival here means being alive from any cause (overall survival)."
)

df = pd.read_csv("data/seer_breast_cancer_cleaned.csv")
df["event"] = (df["Status"] == "Dead").astype(int)
df["stage_group"] = df["6th Stage"].str.startswith("III").map({True: "Stage III", False: "Stage II"})

kmf_all = KaplanMeierFitter().fit(df["Survival Months"], df["event"])
five_all = kmf_all.survival_function_at_times(60).iloc[0]

col1, col2, col3 = st.columns(3)
col1.metric("Patients", f"{len(df):,}")
col2.metric("Deaths", f"{df['event'].sum():,}")
col3.metric("5-year survival (all patients)", f"{five_all:.1%}")

st.divider()

options = {
    "Stage II vs Stage III": ("stage_group", ["Stage II", "Stage III"]),
    "Stage (IIA to IIIC)": ("6th Stage", ["IIA", "IIB", "IIIA", "IIIB", "IIIC"]),
    "Tumor stage (T)": ("T Stage", ["T1", "T2", "T3", "T4"]),
    "Lymph node stage (N)": ("N Stage", ["N1", "N2", "N3"]),
}
choice = st.selectbox("Compare survival by:", list(options.keys()))
column, groups = options[choice]

fig = go.Figure()
rows = []
for group, color, band in zip(groups, COLORS, BANDS):
    data = df[df[column] == group]
    kmf = KaplanMeierFitter().fit(data["Survival Months"], data["event"], label=group)
    curve = kmf.survival_function_
    ci = kmf.confidence_interval_survival_function_
    months = curve.index

    fig.add_trace(go.Scatter(
        x=months, y=ci.iloc[:, 1], line=dict(width=0), line_shape="hv",
        hoverinfo="skip", showlegend=False,
    ))
    fig.add_trace(go.Scatter(
        x=months, y=ci.iloc[:, 0], line=dict(width=0), line_shape="hv",
        fill="tonexty", fillcolor=band,
        hoverinfo="skip", showlegend=False,
    ))
    fig.add_trace(go.Scatter(
        x=months, y=curve.iloc[:, 0], name=group,
        line=dict(color=color, width=2.5), line_shape="hv",
        hovertemplate=f"{group}<br>Month %{{x}}<br>%{{y:.1%}} alive<extra></extra>",
    ))

    five = kmf.survival_function_at_times(60).iloc[0]
    rows.append({"Group": group, "Patients": len(data), "Deaths": int(data["event"].sum()),
                 "5-year survival": f"{five:.1%}", "_five": five})

fig.add_vline(x=60, line_dash="dot", line_color="grey", annotation_text="5 years")
fig.update_layout(
    title=f"Overall survival by {choice}",
    xaxis=dict(title="Months since diagnosis", tickmode="linear", tick0=0, dtick=12),
    yaxis=dict(title="Patients alive", tickformat=".0%", range=[0, 1.02]),
    hovermode="x unified", height=480, legend=dict(title=None, traceorder="normal"),
)
st.plotly_chart(fig, width="stretch")

table = pd.DataFrame(rows)
best = table.loc[table["_five"].idxmax()]
worst = table.loc[table["_five"].idxmin()]

used = df[df[column].isin(groups)]
p = multivariate_logrank_test(used["Survival Months"], used[column], used["event"]).p_value

left, right = st.columns([3, 2])
with left:
    st.subheader("5-year survival by group")
    st.dataframe(table.drop(columns="_five"), hide_index=True, width="stretch")
with right:
    st.subheader("What this shows")
    st.markdown(
        f"After 5 years, **{best['5-year survival']}** of **{best['Group']}** patients were alive, "
        f"compared with **{worst['5-year survival']}** of **{worst['Group']}** patients."
    )
    if p < 0.05:
        st.success(f"This difference is larger than chance would explain (log-rank p = {p:.2g}).")
    else:
        st.warning(f"This difference could be due to chance (log-rank p = {p:.2g}).")

with st.expander("How to read this page"):
    st.markdown(
        "- Each line shows the share of patients still alive over time. Shaded bands show the 95% confidence range.\n"
        "- Survival counts death from **any cause**, not only breast cancer.\n"
        "- Stage is built from tumor stage (T) and node stage (N), so **Stage IIIC and N3 are the same patients**.\n"
        "- **Stage IIIB has only 67 patients**, so its curve is less certain (wider band).\n"
        "- These are patterns across groups, **not predictions** for any individual patient."
    )
