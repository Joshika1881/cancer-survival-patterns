import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Data Overview")

df = pd.read_csv("data/seer_breast_cancer_cleaned.csv")

st.write(
    "This page provides an overview of the patients in the "
    "SEER Breast Cancer dataset."
)

# Summary metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Patients", len(df))
col2.metric("Median Age", f"{df['Age'].median():.0f}")
col3.metric(
    "Alive",
    f"{(df['Status'].eq('Alive').mean() * 100):.1f}%"
)
col4.metric(
    "Median Survival Months",
    f"{df['Survival Months'].median():.0f}"
)

# Age distribution
st.subheader("Age Distribution")

fig_age = px.histogram(
    df,
    x="Age",
    nbins=20,
    title="Age Distribution of Patients"
)

st.plotly_chart(fig_age, width="stretch")

st.write(
    "This visualization shows the distribution of patient ages "
    "represented in the dataset."
)

# Patient survival status
st.subheader("Patient Survival Status")

fig_status = px.histogram(
    df,
    x="Status",
    title="Patient Survival Status",
    text_auto=True
)

st.plotly_chart(fig_status, width="stretch")

st.write(
    "This visualization compares the number of patients recorded "
    "as Alive and Dead in the dataset."
)

# Race distribution
st.subheader("Race Distribution")

race_counts = df["Race"].value_counts().reset_index()
race_counts.columns = ["Race", "Count"]

fig_race = px.bar(
    race_counts,
    x="Race",
    y="Count",
    title="Distribution of Patients by Race",
    text="Count"
)

st.plotly_chart(fig_race, width="stretch")

st.write(
    "This visualization shows the racial composition of patients "
    "represented in the dataset."
)

# Marital status distribution
st.subheader("Marital Status Distribution")

marital_counts = df["Marital Status"].value_counts().reset_index()
marital_counts.columns = ["Marital Status", "Count"]

fig_marital = px.bar(
    marital_counts,
    x="Marital Status",
    y="Count",
    title="Distribution of Patients by Marital Status",
    text="Count"
)

st.plotly_chart(fig_marital, width="stretch")

st.write(
    "This visualization provides an overview of the marital status "
    "categories represented in the patient population."
)

# Survival months distribution
st.subheader("Survival Months Distribution")

fig_survival = px.histogram(
    df,
    x="Survival Months",
    nbins=20,
    title="Distribution of Survival Months"
)

st.plotly_chart(fig_survival, width="stretch")

st.write(
    "This distribution shows the range of recorded survival times "
    "across patients in the dataset."
)

# Interactive Group Summary
st.divider()
st.header("Interactive Group Summary")

st.write(
    "Select a patient characteristic to explore how that group is represented "
    "in the dataset."
)

group_variable = st.selectbox(
    "Choose a characteristic:",
    ["Age Group", "Stage Group", "Grade Group", "Hormone Status"]
)

# Keep group options in a logical order
group_orders = {
    "Age Group": ["Under 50", "50-59", "60-69"],
    "Stage Group": ["Stage II", "Stage III"],
    "Grade Group": ["Grade I", "Grade II", "Grade III-IV"],
    "Hormone Status": ["Positive", "Negative"]
}

selected_group = st.selectbox(
    f"Choose a {group_variable}:",
    group_orders[group_variable]
)

# Filter dataset based on user selection
filtered_df = df[df[group_variable] == selected_group]

# Calculate output
patient_count = len(filtered_df)
dataset_percent = (patient_count / len(df)) * 100
alive_percent = (filtered_df["Status"] == "Alive").mean() * 100
median_survival = filtered_df["Survival Months"].median()

# Display output
st.subheader(f"Summary for {selected_group}")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Patients", f"{patient_count:,}")
col2.metric("Percent of Dataset", f"{dataset_percent:.1f}%")
col3.metric("Alive", f"{alive_percent:.1f}%")
col4.metric("Median Survival Months", f"{median_survival:.0f}")

st.caption(
    "These results describe patterns in the dataset and are not predictions "
    "of an individual patient's outcome."
)