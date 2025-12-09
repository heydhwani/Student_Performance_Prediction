import streamlit as st
import requests

API_URL = "https://student-performance-prediction-8s1j.onrender.com/predict"

st.set_page_config(page_title="Student Performance Prediction", layout="centered")
st.title("Student Performance Prediction App")

st.write("Select the correct options. Dropdowns show readable meanings, while the app sends dataset codes to the API.")


# Mapping readable labels to dataset codes


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


# Form Section


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

    # dropdowns showing labels
    Mjob_label = st.selectbox("Mother Job", list(JOB_MAP.keys()))
    Fjob_label = st.selectbox("Father Job", list(JOB_MAP.keys()))

    # dropdown with all dataset options
    reason_label = st.selectbox("Reason for Choosing School", list(REASON_MAP.keys()))

    guardian = st.selectbox("Guardian", ["mother", "father", "other"])
    famsup = st.selectbox("Family Support", ["yes", "no"])

    st.subheader("Academic Status")

    traveltime = st.selectbox("Travel Time (1 = <15 min, 4 = >60 min)", [1, 2, 3, 4])
    studytime = st.selectbox("Study Time (1-4)", [1, 2, 3, 4])
    failures = st.selectbox("Past Failures", [0, 1, 2, 3, 4])
    schoolsup = st.selectbox("School Support", ["yes", "no"])
    paid = st.selectbox("Paid Classes", ["yes", "no"])
    activities = st.selectbox("Activities", ["yes", "no"])
    internet = st.selectbox("Internet Access", ["yes", "no"])
    nursery = st.selectbox("Attended Nursery?", ["yes", "no"])
    higher = st.selectbox("Wants Higher Education?", ["yes", "no"])
    absences = st.number_input("Absences", 0, 93, 2)
    G1 = st.number_input("G1 Grade (0-20)", 0, 20, 12)
    G2 = st.number_input("G2 Grade (0-20)", 0, 20, 12)

    st.subheader("Health Status")

    romantic = st.selectbox("Romantic Relationship?", ["yes", "no"])
    famrel = st.slider("Family Relationship Quality (1-5)", 1, 5, 4)
    freetime = st.slider("Free Time After School (1-5)", 1, 5, 3)
    goout = st.slider("Going Out with Friends (1-5)", 1, 5, 2)
    Dalc = st.slider("Workday Alcohol Consumption (1-5)", 1, 5, 1)
    Walc = st.slider("Weekend Alcohol Consumption (1-5)", 1, 5, 1)
    health = st.slider("Health Status (1-5)", 1, 5, 4)

    submitted = st.form_submit_button("Predict")


if submitted:
    # Convert readable label → dataset code
    school = SCHOOL_MAP[school_label]
    famsize = FAMSIZE_MAP[famsize_label]
    address = ADDRESS_MAP[address_label]
    Mjob = JOB_MAP[Mjob_label]
    Fjob = JOB_MAP[Fjob_label]
    reason = REASON_MAP[reason_label]

    payload = {
        "student": {
            "school": school,
            "sex": sex,
            "age": int(age),
            "address": address
        },
        "family": {
            "famsize": famsize,
            "Pstatus": Pstatus,
            "Medu": int(Medu),
            "Fedu": int(Fedu),
            "Mjob": Mjob,
            "Fjob": Fjob,
            "reason": reason,
            "guardian": guardian,
            "famsup": famsup
        },
        "academic": {
            "traveltime": int(traveltime),
            "studytime": int(studytime),
            "failures": int(failures),
            "schoolsup": schoolsup,
            "paid": paid,
            "activities": activities,
            "internet": internet,
            "nursery": nursery,
            "higher": higher,
            "absences": int(absences),
            "G1": int(G1),
            "G2": int(G2)
        },
        "health": {
            "romantic": romantic,
            "famrel": int(famrel),
            "freetime": int(freetime),
            "goout": int(goout),
            "Dalc": int(Dalc),
            "Walc": int(Walc),
            "health": int(health)
        }
    }

    st.info("Sending request to API...")

    try:
        response = requests.post(API_URL, json=payload, timeout=10)
    except requests.RequestException as e:
        st.error(f"Network Error: {e}")
    else:
        if response.status_code == 200:
            result = response.json()
            st.success("Prediction Successful!")
            st.metric("Predicted Final Marks", result.get("predicted_final_Marks", "—"))
            st.write("Remark:", result.get("remark", "—"))
            st.json(result)
        else:
            st.error(f"API returned status code {response.status_code}")
            try:
                st.json(response.json())
            except:
                st.text(response.text)
