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

st.metric("Patients", len(df))
st.metric("Deaths", int(df["event"].sum()))