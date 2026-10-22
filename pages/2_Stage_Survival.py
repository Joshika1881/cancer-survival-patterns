import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter
from lifelines.statistics import multivariate_logrank_test

st.title("Cancer Stage and Survival")
st.write(
    "How does survival differ by cancer stage, tumor stage (T) "
    "and lymph node stage (N)? Survival here means being alive from "
    "any cause (overall survival)."
)

df = pd.read_csv("data/seer_breast_cancer_cleaned.csv")
df["event"] = (df["Status"] == "Dead").astype(int)
df["stage_group"] = df["6th Stage"].str.startswith("III").map({True: "Stage III", False: "Stage II"})

options = {
    "Stage II vs Stage III": ("stage_group", ["Stage II", "Stage III"]),
    "Stage (IIA to IIIC)": ("6th Stage", ["IIA", "IIB", "IIIA", "IIIB", "IIIC"]),
    "Tumor stage (T)": ("T Stage", ["T1", "T2", "T3", "T4"]),
    "Lymph node stage (N)": ("N Stage", ["N1", "N2", "N3"]),
}

choice = st.selectbox("Compare survival by:", list(options.keys()))
column, groups = options[choice]

fig, ax = plt.subplots(figsize=(8, 5))
rows = []
for group in groups:
    data = df[df[column] == group]
    kmf = KaplanMeierFitter()
    kmf.fit(data["Survival Months"], data["event"], label=group)
    kmf.plot_survival_function(ax=ax)
    five = kmf.survival_function_at_times(60).iloc[0]
    rows.append({"Group": group, "Patients": len(data), "5-year survival (%)": round(five * 100, 1)})

ax.set_ylim(0, 1)
ax.set_xlabel("Months since diagnosis")
ax.set_ylabel("Share of patients alive")
ax.set_title(f"Overall survival by {choice}")
st.pyplot(fig)

st.dataframe(pd.DataFrame(rows), hide_index=True)

used = df[df[column].isin(groups)]
p = multivariate_logrank_test(used["Survival Months"], used[column], used["event"]).p_value

if p < 0.05:
    st.success(f"The difference between these groups is larger than chance would explain (log-rank p = {p:.3g}).")
else:
    st.warning(f"The difference could be due to chance (log-rank p = {p:.3g}).")

st.caption(
    "Stage is built from tumor stage (T) and node stage (N), so Stage IIIC and N3 are the same patients. "
    "Stage IIIB has only 67 patients, so its curve is less certain. "
    "Survival here includes death from any cause."
)