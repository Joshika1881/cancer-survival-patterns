import streamlit as st

st.set_page_config(
    page_title="Breast Cancer Survival Patterns",
    page_icon="🎗️",
    layout="wide"
)

st.title("Breast Cancer Survival Patterns")

st.write(
    """
    This application explores patterns in breast cancer survival
    using the SEER Breast Cancer dataset.

    Use the pages in the sidebar to explore patient characteristics,
    cancer stage, hormone receptor status, and clinical factors.
    """
)

st.info(
    "This application is for educational and exploratory purposes "
    "and is not intended to provide medical advice."
)