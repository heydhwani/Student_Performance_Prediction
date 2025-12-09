import streamlit as st
import requests

API_URL = "https://student-performance-prediction-8s1j.onrender.com/predict"

st.set_page_config(page_title="Student Performance Prediction", layout="centered")
st.title("Student Performance Prediction App")

st.write("Select the correct options. Dropdowns show readable meanings, while the app sends dataset codes to the API.")

# -------------------------------------------------------
# Mapping readable labels to dataset codes
# -------------------------------------------------------

SCHOOL_MAP = {
    "GP — Gabriel Pereira (code: GP)": "GP",
    "MS — Mousinho da Silveira (code: MS)": "MS"
}

FAMSIZE_MAP = {
    "GT3 — more than 3 family members (code: GT3)": "GT3",
    "LE3 — 3 or fewer family members (code: LE3)": "LE3"
}

ADDRESS_MAP = {
    "U — Urban (code: U)": "U",
    "R — Rural (code: R)": "R"
}

# Job categories from dataset
JOB_MAP = {
    "at_home — stays at home (code: at_home)": "at_home",
    "health — healthcare related (code: health)": "health",
    "other — other profession (code: other)": "other",
    "services — service sector (code: services)": "services",
    "teacher — teaching profession (code: teacher)": "teacher"
}

# Reason categories from dataset
REASON_MAP = {
    "home — close to home (code: home)": "home",
    "reputation — good reputation (code: reputation)": "reputation",
    "course — liked the course (code: course)": "course",
    "other — other reason (code: other)": "other"
}

# -------------------------------------------------------
# Form Section
# -------------------------------------------------------

with st.form("prediction_form"):
    st.subheader("Student Details")

    school_label = st.selectbox("School", list(SCHOOL_MAP.keys()))
    sex = st.selectbox("Sex", ["M", "F"])
    age = st.number_input("Age", min_value=15, max_value=22, value=18)
    address_label = st.selectbox("Address Type", list(ADDRESS_MAP.keys()))

    st.subheader("Family Background")

    famsize_label = st.selectbox("Family Size", list(FAMSIZE_MAP.keys()))
    Pstatus = st.selectbox("Parent Status", ["T", "A"])
    Medu = st.number_input("Mother Education (0-4)", 0, 4, 2)
    Fedu = st.number_input("Father Education (0-4)", 0, 4, 2)

    # UPDATED ↓↓↓ (dropdowns showing labels)
    Mjob_label = st.selectbox("Mother Job", list(JOB_MAP.keys
