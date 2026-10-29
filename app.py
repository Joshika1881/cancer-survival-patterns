import streamlit as st

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Breast Cancer Survival Patterns",
    page_icon="🎗️",
    layout="wide"
)

# ---------------------------------------------------------
# HERO SECTION
# ---------------------------------------------------------
st.title("🎗️ Breast Cancer Survival Patterns")

st.markdown(
    """
    Explore patterns in breast cancer survival using the **SEER Breast Cancer dataset**.
    This interactive application summarizes patient characteristics, clinical factors,
    cancer stage, hormone receptor status, and survival patterns.
    """
)

st.info(
    "Use the navigation in the sidebar to move between the Data Overview, "
    "Stage Survival, and Hormone & Demographics sections."
)

st.divider()

# ---------------------------------------------------------
# PROJECT OVERVIEW
# ---------------------------------------------------------
st.subheader("Project Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Patients", "4,023")
    st.caption(
        "Patients included after cleaning and removing the duplicate record."
    )

with col2:
    st.metric("Age Range", "30–69")
    st.caption(
        "Patient ages represented in the SEER breast cancer dataset."
    )

with col3:
    st.metric("Cancer Stages", "IIA–IIIC")
    st.caption(
        "The dataset contains Stage II and Stage III breast cancer cases."
    )

st.divider()

# ---------------------------------------------------------
# APP SECTIONS
# ---------------------------------------------------------
st.subheader("Explore the Application")

overview_col, stage_col, hormone_col = st.columns(3)

with overview_col:
    st.markdown("### 📊 Data Overview")
    st.write(
        "Explore the overall patient population through summary metrics, "
        "demographic distributions, survival months, and an interactive "
        "group summary."
    )

    st.markdown(
        """
        **Includes:**
        - Age distribution
        - Race distribution
        - Marital status
        - Survival status
        - Interactive patient-group summaries
        """
    )

with stage_col:
    st.markdown("### 📈 Stage Survival")
    st.write(
        "Compare survival patterns across cancer stage, tumor stage, "
        "and lymph node involvement using survival analysis."
    )

    st.markdown(
        """
        **Includes:**
        - Kaplan-Meier survival curves
        - 5-year survival estimates
        - Stage II vs Stage III
        - Detailed Stage IIA–IIIC comparisons
        - Log-rank test results
        """
    )

with hormone_col:
    st.markdown("### 🧬 Hormone & Demographics")
    st.write(
        "Explore hormone receptor status and how patient and clinical "
        "characteristics are distributed across the dataset."
    )

    st.markdown(
        """
        **Includes:**
        - Hormone receptor status
        - Age groups
        - Race
        - Grade groups
        - Demographic comparisons
        """
    )

st.divider()

# ---------------------------------------------------------
# ANALYSIS DEFINITIONS
# ---------------------------------------------------------
st.subheader("Shared Analysis Definitions")

st.write(
    "To keep all sections of the application consistent, the team uses "
    "the same analysis groups throughout the project."
)

definition_col1, definition_col2 = st.columns(2)

with definition_col1:
    st.markdown(
        """
        **Age Groups**
        - Under 50
        - 50–59
        - 60–69

        **Stage Groups**
        - Stage II
        - Stage III
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
        - Positive if estrogen receptor (ER) or progesterone receptor (PR) is positive
        """
    )

st.divider()

# ---------------------------------------------------------
# HOW TO USE
# ---------------------------------------------------------
st.subheader("How to Use This App")

st.markdown(
    """
    1. Start with **Data Overview** to understand the patient population.
    2. Use the **Interactive Group Summary** to select a patient characteristic
       and view group-level results.
    3. Open **Stage Survival** to compare survival patterns across clinical stages.
    4. Explore **Hormone & Demographics** for additional patient and clinical comparisons.
    """
)

st.divider()

# ---------------------------------------------------------
# DISCLAIMER
# ---------------------------------------------------------
st.warning(
    "Educational Use Only: This application is intended for exploratory "
    "data analysis and educational purposes. The results describe patterns "
    "in this dataset and should not be interpreted as medical advice, "
    "diagnosis, or an individual survival prediction."
)