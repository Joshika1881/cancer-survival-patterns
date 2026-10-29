import streamlit as st

st.set_page_config(
    page_title="Breast Cancer Survival Patterns",
    layout="wide"
)

st.title("Breast Cancer Survival Patterns")

st.markdown(
    """
    Explore patterns in breast cancer survival using the
    **SEER Breast Cancer dataset**.

    This application summarizes patient characteristics,
    clinical stage patterns, hormone and demographic factors,
    and survival outcomes.
    """
)

st.info(
    "Use the navigation menu in the sidebar to explore each section of the application."
)

st.divider()

st.subheader("Project Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Patients", "4,023")
    st.caption("Patients included in the cleaned dataset")

with col2:
    st.metric("Age Range", "30–69")
    st.caption("Age range represented in the dataset")

with col3:
    st.metric("Cancer Stages", "IIA–IIIC")
    st.caption("Clinical stages represented in the dataset")

st.divider()

st.subheader("Explore the Application")

overview_col, stage_col, hormone_col = st.columns(3)

with overview_col:
    st.markdown("### Data Overview")
    st.write(
        """
        Explore the overall characteristics of the dataset
        and interact with patient group summaries.
        """
    )

    st.markdown(
        """
        **Includes:**
        - Age distribution
        - Race distribution
        - Marital status
        - Survival status
        - Survival months
        - Interactive group summary
        """
    )

with stage_col:
    st.markdown("### Stage Survival")
    st.write(
        """
        Compare survival patterns across different
        breast cancer stages.
        """
    )

    st.markdown(
        """
        **Includes:**
        - Kaplan-Meier survival curves
        - Five-year survival estimates
        - Stage II vs. Stage III
        - Detailed Stage IIA–IIIC comparisons
        - Log-rank comparisons
        """
    )

with hormone_col:
    st.markdown("### Hormone & Demographics")
    st.write(
        """
        Explore how hormone status and demographic
        characteristics relate to survival patterns.
        """
    )

    st.markdown(
        """
        **Includes:**
        - Hormone receptor status
        - Age groups
        - Race
        - Tumor grade
        - Group comparisons
        """
    )

st.divider()

st.subheader("Shared Analysis Definitions")

definition_col1, definition_col2 = st.columns(2)

with definition_col1:
    st.markdown(
        """
        **Age Groups**
        - Under 50
        - 50–59
        - 60–69

        **Stage Groups**
        - Stage II: IIA and IIB
        - Stage III: IIIA, IIIB, and IIIC
        """
    )

with definition_col2:
    st.markdown(
        """
        **Grade Groups**
        - Grade I
        - Grade II
        - Grade III–IV

        **Hormone Status**
        - Positive if estrogen receptor or progesterone receptor status is positive
        - Negative if both are negative
        """
    )

st.divider()

st.subheader("How to Use This App")

st.markdown(
    """
    1. Start with **Data Overview** to understand the patient population.
    2. Use the **Interactive Group Summary** to explore selected patient groups.
    3. Visit **Stage Survival** to compare survival patterns across cancer stages.
    4. Visit **Hormone & Demographics** to explore additional patient characteristics.
    """
)

st.divider()

st.warning(
    """
    Educational Use Only

    This application is intended for educational data analysis.
    It does not provide medical advice, diagnosis, treatment recommendations,
    or individual survival predictions.
    """
)