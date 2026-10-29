import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from lifelines import KaplanMeierFitter
from lifelines.statistics import multivariate_logrank_test

COLORS = ["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A"]
BANDS = ["rgba(99,110,250,0.15)", "rgba(239,85,59,0.15)", "rgba(0,204,150,0.15)",
         "rgba(171,99,250,0.15)", "rgba(255,161,90,0.15)"]


@st.cache_data
def load_data():
    data = pd.read_csv("data/seer_breast_cancer_cleaned.csv")
    data["event"] = (data["Status"] == "Dead").astype(int)
    data["stage_group"] = data["6th Stage"].str.startswith("III").map({True: "Stage III", False: "Stage II"})
    return data

# ---------- Part 1: title, data, summary numbers ----------
st.title("Cancer Stage and Survival")
st.write(
    "How does survival differ by cancer stage, tumor stage (T) and lymph node stage (N)? "
    "Survival here means being alive from any cause (overall survival)."
)

df = load_data()

kmf_all = KaplanMeierFitter().fit(df["Survival Months"], df["event"])
five_all = kmf_all.survival_function_at_times(60).iloc[0]

col1, col2, col3 = st.columns(3)
col1.metric("Total Patients", f"{len(df):,}")
col2.metric("Deaths", f"{df['event'].sum():,}")
col3.metric("5-year survival", f"{five_all:.1%}")

st.divider()

# ---------- Part 2: dropdown ----------
options = {
    "Stage II vs Stage III": ("stage_group", ["Stage II", "Stage III"]),
    "Stage (IIA to IIIC)": ("6th Stage", ["IIA", "IIB", "IIIA", "IIIB", "IIIC"]),
    "Tumor stage (T)": ("T Stage", ["T1", "T2", "T3", "T4"]),
    "Lymph node stage (N)": ("N Stage", ["N1", "N2", "N3"]),
}
st.subheader("Survival Over Time")
choice = st.selectbox("Compare survival by:", list(options.keys()))
column, groups = options[choice]

# ---------- Part 3: interactive chart ----------
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
    xaxis=dict(title="Months since diagnosis", tickmode="linear", tick0=0, dtick=12),
    yaxis=dict(title="Patients alive", tickformat=".0%", range=[0, 1.02]),
    hovermode="x unified", height=450, legend=dict(title=None, traceorder="normal"),
    margin=dict(l=60, r=20, t=40, b=60),
)
st.plotly_chart(fig, width="stretch")

with st.expander("What does this show?"):
    st.write(
        "Each line shows the share of patients still alive over time. Shaded bands show the "
        "95% confidence range. The dotted line marks 5 years (60 months)."
    )

st.divider()

# ---------- Part 4: table, test result, headline ----------
table = pd.DataFrame(rows)
best = table.loc[table["_five"].idxmax()]
worst = table.loc[table["_five"].idxmin()]

used = df[df[column].isin(groups)]
p = multivariate_logrank_test(used["Survival Months"], used[column], used["event"]).p_value

left, right = st.columns([3, 2])
with left:
    st.subheader("5-year survival by group")
    st.dataframe(table.drop(columns="_five"), hide_index=True)
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

st.caption(
    "Survival counts death from any cause. Stage is built from tumor stage (T) and node stage (N), "
    "so Stage IIIC and N3 are the same patients. Stage IIIB has only 67 patients. "
    "Results describe patterns in this dataset and are not predictions of an individual patient's outcome."
)
