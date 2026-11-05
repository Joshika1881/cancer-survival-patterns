import streamlit as st
import pandas as pd
import plotly.express as px


# ---------------------------------------------------------
# LOAD DATA
# Week 9 concept: Streamlit caching
# ---------------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("data/seer_breast_cancer_cleaned.csv")


df = load_data()


# ---------------------------------------------------------
# HELPER FUNCTION
# Week 2 concept: reusable functions
# Week 3 concept: Pandas groupby and aggregation
# ---------------------------------------------------------

def create_group_summary(data, group_variable, group_order):
    summary_rows = []

    for group in group_order:
        group_df = data[data[group_variable] == group]

        patient_count = len(group_df)
        dataset_percent = (patient_count / len(data)) * 100
        alive_percent = (group_df["Status"] == "Alive").mean() * 100
        median_survival = group_df["Survival Months"].median()

        summary_rows.append(
            {
                "Group": group,
                "Patients": patient_count,
                "Dataset (%)": dataset_percent,
                "Alive (%)": alive_percent,
                "Median Survival (Months)": median_survival,
            }
        )

    return pd.DataFrame(summary_rows)


# ---------------------------------------------------------
# PAGE HEADER
# ---------------------------------------------------------

st.title("Data Overview")

st.write(
    """
    This page provides an overview of the breast cancer dataset and allows
    users to explore patient characteristics and survival patterns.
    """
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
# AGE DISTRIBUTION + SURVIVAL STATUS
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
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        )
    )

    st.plotly_chart(
        age_fig,
        width="stretch"
    )

    with st.expander("What does this show?"):

        st.write(
            """
            This chart shows the age distribution of patients in the dataset.
            Patients range from 30 to 69 years old.
            """
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
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        )
    )

    st.plotly_chart(
        status_fig,
        width="stretch"
    )

    with st.expander("What does this show?"):

        st.write(
            """
            This chart compares the number of patients recorded as Alive
            and Dead in the dataset. Most patients were alive at the end
            of their recorded follow-up period.
            """
        )


st.divider()


# ---------------------------------------------------------
# RACE + MARITAL STATUS
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
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        )
    )

    st.plotly_chart(
        race_fig,
        width="stretch"
    )

    with st.expander("What does this show?"):

        st.write(
            """
            This chart shows the racial distribution of patients represented
            in the dataset. The size of each bar represents the number of
            patients in that category.
            """
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
        xaxis_tickangle=-25,
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        )
    )

    st.plotly_chart(
        marital_fig,
        width="stretch"
    )

    with st.expander("What does this show?"):

        st.write(
            """
            This chart shows how patients are distributed across the marital
            status categories recorded in the dataset.
            """
        )


st.divider()


# ---------------------------------------------------------
# SURVIVAL MONTHS + INTERACTIVE GROUP SUMMARY
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
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        )
    )

    st.plotly_chart(
        survival_fig,
        width="stretch"
    )

    with st.expander("What does this show?"):

        st.write(
            """
            This chart shows the distribution of recorded survival or
            follow-up months across patients in the dataset.
            """
        )


with right:

    st.subheader("Interactive Group Summary")

    st.write(
        """
        Choose a patient characteristic and group to view a descriptive
        summary of patients in that category.
        """
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

    group_variable = st.selectbox(
        "Characteristic",
        list(group_orders.keys()),
        key="individual_characteristic"
    )

    selected_group = st.selectbox(
        "Group",
        group_orders[group_variable],
        key="individual_group"
    )

    filtered_df = df[
        df[group_variable] == selected_group
    ]

    patient_count = len(filtered_df)

    dataset_percent = (
        patient_count / len(df)
    ) * 100

    group_alive_percent = (
        filtered_df["Status"] == "Alive"
    ).mean() * 100

    median_group_survival = (
        filtered_df["Survival Months"]
        .median()
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
        """
        These values describe patterns within this dataset and should not
        be interpreted as predictions for individual patients.
        """
    )


# ---------------------------------------------------------
# NEW SECTION: COMPARE PATIENT GROUPS
# Week 3: Pandas groupby / aggregation
# Week 4: data transformation
# Week 5: interactive Plotly visualization
# ---------------------------------------------------------

st.divider()

st.header("Compare Patient Groups")

st.write(
    """
    Select a characteristic to compare all of its groups at the same time.
    The table summarizes patient counts, representation in the dataset,
    percentage alive, and median recorded survival months.
    """
)


comparison_variable = st.selectbox(
    "Compare groups by",
    list(group_orders.keys()),
    key="comparison_characteristic"
)


comparison_df = create_group_summary(
    df,
    comparison_variable,
    group_orders[comparison_variable]
)


# ---------------------------------------------------------
# FORMAT TABLE
# ---------------------------------------------------------

display_df = comparison_df.copy()

display_df["Dataset (%)"] = (
    display_df["Dataset (%)"]
    .map(lambda x: f"{x:.1f}%")
)

display_df["Alive (%)"] = (
    display_df["Alive (%)"]
    .map(lambda x: f"{x:.1f}%")
)

display_df["Median Survival (Months)"] = (
    display_df["Median Survival (Months)"]
    .map(lambda x: f"{x:.0f}")
)


st.dataframe(
    display_df,
    hide_index=True,
    width="stretch"
)


# ---------------------------------------------------------
# CHOOSE WHAT TO VISUALIZE
# ---------------------------------------------------------

comparison_metric = st.selectbox(
    "Select a measure to visualize",
    [
        "Patients",
        "Alive (%)",
        "Median Survival (Months)"
    ]
)


if comparison_metric == "Patients":

    y_column = "Patients"

    y_label = "Number of Patients"

    chart_title = (
        f"Patient Count by {comparison_variable}"
    )


elif comparison_metric == "Alive (%)":

    y_column = "Alive (%)"

    y_label = "Patients Alive (%)"

    chart_title = (
        f"Percentage Alive by {comparison_variable}"
    )


else:

    y_column = "Median Survival (Months)"

    y_label = "Median Survival Months"

    chart_title = (
        f"Median Survival Months by {comparison_variable}"
    )


comparison_fig = px.bar(
    comparison_df,
    x="Group",
    y=y_column,
    labels={
        "Group": comparison_variable,
        y_column: y_label
    },
    title=chart_title,
    text_auto=".1f"
)


comparison_fig.update_layout(
    height=400,
    margin=dict(
        l=20,
        r=20,
        t=60,
        b=20
    )
)


st.plotly_chart(
    comparison_fig,
    width="stretch"
)


with st.expander("How is this calculated?"):

    st.write(
        f"""
        The application groups patients by **{comparison_variable}** using
        Pandas. For each group, it calculates:
        """
    )

    st.markdown(
        """
        - **Patients:** number of records in the group
        - **Dataset (%):** percentage of all 4,023 patients in the group
        - **Alive (%):** percentage of patients whose recorded status is Alive
        - **Median Survival:** median value of the recorded Survival Months
        """
    )

    st.write(
        """
        Changing the dropdown automatically recalculates the summaries
        and updates the visualization.
        """
    )


st.caption(
    """
    Group comparisons are descriptive summaries of this dataset.
    Survival Months includes recorded follow-up time and these results
    are not individual survival predictions.
    """
)