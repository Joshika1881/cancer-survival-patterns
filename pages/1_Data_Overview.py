import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Data Overview")

df = pd.read_csv("data/seer_breast_cancer_cleaned.csv")

st.write(
    "This page provides an overview of the patients in the "
    "SEER Breast Cancer dataset."
)

st.metric("Number of Patients", len(df))

st.subheader("Age Distribution")

fig_age = px.histogram(
    df,
    x="Age",
    nbins=20,
    title="Age Distribution of Patients"
)

st.plotly_chart(fig_age, width="stretch")

st.subheader("Patient Survival Status")

fig_status = px.histogram(
    df,
    x="Status",
    title="Patient Survival Status",
    text_auto=True
)

st.plotly_chart(fig_status, width="stretch")