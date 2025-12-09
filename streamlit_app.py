import streamlit as st
import requests

API_URL = "https://student-performance-prediction-8s1j.onrender.com/predict"

st.title("Student Performance Prediction App")

st.write("Enter student details below and click **Predict**.")


with st.form("prediction_form"):
    st.subheader("Student Details")
    school = st.selectbox("School", ["GP", "MS"])
    sex = st.selectbox("Sex", ["M", "F"])
    age = st.number_input("Age", min_value=15, max_value=22, value=17)
    address = st.selectbox("Address", ["U", "R"])

    st.subheader("Family Background")
    famsize = st.selectbox("Family Size", ["GT3", "LE3"])
    Pstatus = st.selectbox("Parent Status", ["T", "A"])
    Medu = st.number_input("Mother Education (0-4)", 0, 4, 2)
    Fedu = st.number_input("Father Education (0-4)", 0, 4, 2)
    Mjob = st.text_input("Mother Job")
    Fjob = st.text_input("Father Job")
    reason = st.text_input("Reason for choosing school")
    guardian = st.selectbox("Guardian", ["mother", "father", "other"])
    famsup = st.selectbox("Family Support", ["yes", "no"])

    st.subheader("Academic Status")
    traveltime = st.selectbox("Travel Time", [1, 2, 3, 4])
    studytime = st.selectbox("Study Time", [1, 2, 3, 4])
    failures = st.selectbox("Failures", [0, 1, 2, 3, 4])
    schoolsup = st.selectbox("School Support", ["yes", "no"])
    paid = st.selectbox("Paid Classes", ["yes", "no"])
    activities = st.selectbox("Activities", ["yes", "no"])
    internet = st.selectbox("Internet", ["yes", "no"])
    nursery = st.selectbox("Nursery", ["yes", "no"])
    higher = st.selectbox("Higher Education", ["yes", "no"])
    absences = st.number_input("Absences", 0, 93, 2)
    G1 = st.number_input("G1 Grade (0-20)", 0, 20, 10)
    G2 = st.number_input("G2 Grade (0-20)", 0, 20, 10)

    st.subheader("Health Status")
    romantic = st.selectbox("Romantic Relationship", ["yes", "no"])
    famrel = st.slider("Family Relation", 1, 5, 3)
    freetime = st.slider("Free Time", 1, 5, 3)
    goout = st.slider("Going Out", 1, 5, 3)
    Dalc = st.slider("Workday Alcohol", 1, 5, 1)
    Walc = st.slider("Weekend Alcohol", 1, 5, 1)
    health = st.slider("Health", 1, 5, 3)

    submitted = st.form_submit_button("Predict")


if submitted:
    payload = {
        "student": {
            "school": school,
            "sex": sex,
            "age": age,
            "address": address
        },
        "family": {
            "famsize": famsize,
            "Pstatus": Pstatus,
            "Medu": Medu,
            "Fedu": Fedu,
            "Mjob": Mjob,
            "Fjob": Fjob,
            "reason": reason,
            "guardian": guardian,
            "famsup": famsup
        },
        "academic": {
            "traveltime": traveltime,
            "studytime": studytime,
            "failures": failures,
            "schoolsup": schoolsup,
            "paid": paid,
            "activities": activities,
            "internet": internet,
            "nursery": nursery,
            "higher": higher,
            "absences": absences,
            "G1": G1,
            "G2": G2
        },
        "health": {
            "romantic": romantic,
            "famrel": famrel,
            "freetime": freetime,
            "goout": goout,
            "Dalc": Dalc,
            "Walc": Walc,
            "health": health
        }
    }

    st.write("Sending request to API...")
    response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        result = response.json()
        st.success("Prediction Successful!")
        st.metric("Predicted Final Marks", result.get("predicted_final_Marks"))
        st.write("Remark:", result.get("remark"))
        
    else:
        st.error("Error: Could not get prediction from API.")
        st.write(response.text)
