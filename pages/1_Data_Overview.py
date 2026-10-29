import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
df = pd.read_csv("data/seer_breast_cancer_cleaned.csv")

st.title("Data Overview")

st.write(
    "This page provides an overview of the SEER breast cancer dataset "
    "and allows users to interactively explore selected patient groups."
)

# ---------------------------------------------------------
# SUMMARY METRICS
# ---------------------------------------------------------
total_patients = len(df)
median_age = df["Age"].median()
alive_percent = (df["Status"] == "Alive").mean() * 100
median_survival = df["Survival Months"].median()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Patients",
    f"{total_patients:,}"
)

col2.metric(
    "Median Age",
    f"{median_age:.0f}"
)

col3.metric(
    "Alive",
    f"{alive_percent:.1f}%"
)

col4.metric(
    "Median Survival",
    f"{median_survival:.0f} months"
)

st.divider()

# ---------------------------------------------------------
# ROW 1: AGE + SURVIVAL STATUS
# ---------------------------------------------------------
left, right = st.columns(2)

with left:
    st.subheader("Age Distribution")

    age_fig = px.histogram(
        df,
        x="Age",
        nbins=20,
        labels={
            "Age": "Age (Years)"
        }
    )

    age_fig.update_layout(
        height=300,
        yaxis_title="Number of Patients",
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(
        age_fig,
        width="stretch"
    )

    with st.expander("What does this show?"):
        st.write(
            "This chart shows the distribution of patient ages in the dataset. "
            "Patients range from 30 to 69 years old."
        )


with right:
    st.subheader("Patient Survival Status")

    status_counts = (
        df["Status"]
        .value_counts()
        .reset_index()
    )

    status_counts.columns = [
        "Status",
        "Count"
    ]

    status_fig = px.bar(
        status_counts,
        x="Status",
        y="Count",
        labels={
            "Status": "Patient Status",
            "Count": "Number of Patients"
        }
    )

    status_fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(
        status_fig,
        width="stretch"
    )

    with st.expander("What does this show?"):
        st.write(
            "This chart shows the number of patients recorded as Alive or Dead "
            "at the end of follow-up."
        )

st.divider()

# ---------------------------------------------------------
# ROW 2: RACE + MARITAL STATUS
# ---------------------------------------------------------
left, right = st.columns(2)

with left:
    st.subheader("Race Distribution")

    race_counts = (
        df["Race"]
        .value_counts()
        .reset_index()
    )

    race_counts.columns = [
        "Race",
        "Count"
    ]

    race_fig = px.bar(
        race_counts,
        x="Race",
        y="Count",
        labels={
            "Race": "Race",
            "Count": "Number of Patients"
        }
    )

    race_fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(
        race_fig,
        width="stretch"
    )

    with st.expander("What does this show?"):
        st.write(
            "This chart shows how patients in the dataset are distributed "
            "across the recorded racial groups."
        )


with right:
    st.subheader("Marital Status Distribution")

    marital_counts = (
        df["Marital Status"]
        .value_counts()
        .reset_index()
    )

    marital_counts.columns = [
        "Marital Status",
        "Count"
    ]

    marital_fig = px.bar(
        marital_counts,
        x="Marital Status",
        y="Count",
        labels={
            "Marital Status": "Marital Status",
            "Count": "Number of Patients"
        }
    )

    marital_fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis_tickangle=-25
    )

    st.plotly_chart(
        marital_fig,
        width="stretch"
    )

    with st.expander("What does this show?"):
        st.write(
            "This chart summarizes the marital status categories represented "
            "in the patient population."
        )

st.divider()

# ---------------------------------------------------------
# ROW 3: SURVIVAL MONTHS + INTERACTIVE SUMMARY
# ---------------------------------------------------------
left, right = st.columns(2)

with left:
    st.subheader("Survival Months")

    survival_fig = px.histogram(
        df,
        x="Survival Months",
        nbins=30,
        labels={
            "Survival Months": "Survival Months"
        }
    )

    survival_fig.update_layout(
        height=300,
        yaxis_title="Number of Patients",
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(
        survival_fig,
        width="stretch"
    )

    with st.expander("What does this show?"):
        st.write(
            "This chart shows the distribution of observed survival or "
            "follow-up time in months."
        )


# ---------------------------------------------------------
# INTERACTIVE GROUP SUMMARY
# ---------------------------------------------------------
with right:
    st.subheader("Interactive Group Summary")

    st.write(
        "Choose a patient group to view summary information."
    )

    group_variable = st.selectbox(
        "Characteristic",
        [
            "Age Group",
            "Stage Group",
            "Grade Group",
            "Hormone Status"
        ]
    )

    group_orders = {
        "Age Group": [
            "Under 50",
            "50-59",
            "60-69"
        ],

        "Stage Group": [
            "Stage II",
            "Stage III"
        ],

        "Grade Group": [
            "Grade I",
            "Grade II",
            "Grade III-IV"
        ],

        "Hormone Status": [
            "Positive",
            "Negative"
        ]
    }

    selected_group = st.selectbox(
        "Group",
        group_orders[group_variable]
    )

    # Filter dataset using user input
    filtered_df = df[
        df[group_variable] == selected_group
    ]

    # Calculate results
    patient_count = len(filtered_df)

    dataset_percent = (
        patient_count / len(df)
    ) * 100

    group_alive_percent = (
        filtered_df["Status"] == "Alive"
    ).mean() * 100

    median_group_survival = (
        filtered_df["Survival Months"].median()
    )

    st.markdown(
        f"**Summary for {selected_group}**"
    )

    metric1, metric2 = st.columns(2)

    metric1.metric(
        "Patients",
        f"{patient_count:,}"
    )

    metric2.metric(
        "Dataset",
        f"{dataset_percent:.1f}%"
    )

    metric3, metric4 = st.columns(2)

    metric3.metric(
        "Alive",
        f"{group_alive_percent:.1f}%"
    )

    metric4.metric(
        "Median Survival",
        f"{median_group_survival:.0f} mo."
    )

    st.caption(
        "Results describe patterns in this dataset and are not "
        "predictions of an individual patient's outcome."
    )