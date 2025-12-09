# app.py
import streamlit as st
import requests

API_URL = "https://student-performance-prediction-8s1j.onrender.com/predict"

st.set_page_config(page_title="Student Performance Prediction", layout="centered")
st.title("Student Performance Prediction App")
st.write("Choose options and click **Predict**. Labels include short explanations to avoid confusion.")

# ----- mappings from readable label -> dataset code -----
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

JOB_MAP = {
    "at_home — stays at home (code: at_home)": "at_home",
    "health — healthcare related (code: health)": "health",
    "other — other profession (code: other)": "other",
    "services — service sector (code: services)": "services",
    "teacher — teaching profession (code: teacher)": "teacher"
}

REASON_MAP = {
    "home — close to home (code: home)": "home",
    "reputation — good reputation (code: reputation)": "reputation",
    "course — liked the course (code: course)": "course",
    "other — other reason (code: other)": "other"
}

# ----- form -----
with st.form("prediction_form"):
    st.subheader("Student Details")
    school_label = st.selectbox("School", list(SCHOOL_MAP.keys()),
                                help="Select the school (human-readable label shown; dataset code sent to API).")
    sex = st.selectbox("Sex", ["M", "F"], help="M = male, F = female")
    age = st.number_input("Age (years)", min_value=15, max_value=22, value=18,
                          help="Typical student age range in the dataset")
    address_label = st.selectbox("Address", list(ADDRESS_MAP.keys()),
                                 help="U = Urban, R = Rural")

    st.subheader("Family Background")
    famsize_label = st.selectbox("Family Size", list(FAMSIZE_MAP.keys()),
                                 help="GT3 = more than 3 members, LE3 = 3 or fewer members")
    Pstatus = st.selectbox("Parent Cohabitation Status", ["T", "A"],
                           help="T = living together, A = apart")
    Medu = st.number_input("Mother's Education (0=none .. 4=higher)", 0, 4, 2)
    Fedu = st.number_input("Father's Education (0=none .. 4=higher)", 0, 4, 2)

    # mother/father job and reason as dropdowns
    Mjob_label = st.selectbox("Mother's Job", list(JOB_MAP.keys()),
                              help="Choose the mother's job category from dataset options")
    Fjob_label = st.selectbox("Father's Job", list(JOB_MAP.keys()),
                              help="Choose the father's job category from dataset options")
    reason_label = st.selectbox("Reason for Choosing School", list(REASON_MAP.keys()),
                                help="Why the student chose this school")

    guardian = st.selectbox("Guardian", ["mother", "father", "other"])
    famsup = st.selectbox("Family Support?", ["yes", "no"], help="Does family provide educational support?")

    st.subheader("Academic Status")
    # improved travel time label + help (no confusing symbols)
    traveltime = st.selectbox(
        "Travel Time (choose one)",
        options=[1, 2, 3, 4],
        format_func=lambda x: {
            1: "1 — under 15 minutes",
            2: "2 — 15 to 30 minutes",
            3: "3 — 30 to 60 minutes",
            4: "4 — over 60 minutes"
        }[x],
        help="Travel time from home to school. Select the appropriate bucket."
    )

    studytime = st.selectbox(
        "Study Time (1-4)",
        options=[1, 2, 3, 4],
        format_func=lambda x: {
            1: "1 — <2 hours/week",
            2: "2 — 2 to 5 hours/week",
            3: "3 — 5 to 10 hours/week",
            4: "4 — >10 hours/week"
        }[x],
        help="Weekly study time categories"
    )

    failures = st.selectbox("Past Class Failures (count)", [0, 1, 2, 3, 4],
                            help="Number of past class failures (0 if none)")
    schoolsup = st.selectbox("Extra School Support?", ["yes", "no"])
    paid = st.selectbox("Took Extra Paid Classes?", ["yes", "no"])
    activities = st.selectbox("Extra-curricular Activities?", ["yes", "no"])
    internet = st.selectbox("Internet Access at Home?", ["yes", "no"])
    nursery = st.selectbox("Attended Nursery School?", ["yes", "no"])
    higher = st.selectbox("Wants Higher Education?", ["yes", "no"])

    absences = st.number_input("Absences (total)", min_value=0, max_value=93, value=2,
                               help="Total number of school absences")
    G1 = st.number_input("G1 Grade (0-20)", 0, 20, 12)
    G2 = st.number_input("G2 Grade (0-20)", 0, 20, 12)

    st.subheader("Health & Lifestyle")
    romantic = st.selectbox("In a Romantic Relationship?", ["yes", "no"])
    famrel = st.slider("Family Relationship Quality (1 = very bad .. 5 = excellent)", 1, 5, 4)
    freetime = st.slider("Free Time After School (1-5)", 1, 5, 3)
    goout = st.slider("Going Out with Friends (1-5)", 1, 5, 2)
    Dalc = st.slider("Workday Alcohol Consumption (1-5)", 1, 5, 1,
                     help="1 = very low, 5 = very high")
    Walc = st.slider("Weekend Alcohol Consumption (1-5)", 1, 5, 1,
                     help="1 = very low, 5 = very high")
    health = st.slider("Health (1 = very bad .. 5 = very good)", 1, 5, 4)

    submitted = st.form_submit_button("Predict")

# ----- when form submitted, prepare payload & call API -----
if submitted:
    school = SCHOOL_MAP[school_label]
    famsize = FAMSIZE_MAP[famsize_label]
    address = ADDRESS_MAP[address_label]
    Mjob = JOB_MAP[Mjob_label]
    Fjob = JOB_MAP[Fjob_label]
    reason = REASON_MAP[reason_label]

    payload = {
        "student": {"school": school, "sex": sex, "age": int(age), "address": address},
        "family": {
            "famsize": famsize, "Pstatus": Pstatus,
            "Medu": int(Medu), "Fedu": int(Fedu),
            "Mjob": Mjob, "Fjob": Fjob,
            "reason": reason, "guardian": guardian, "famsup": famsup
        },
        "academic": {
            "traveltime": int(traveltime), "studytime": int(studytime),
            "failures": int(failures), "schoolsup": schoolsup,
            "paid": paid, "activities": activities, "internet": internet,
            "nursery": nursery, "higher": higher,
            "absences": int(absences), "G1": int(G1), "G2": int(G2)
        },
        "health": {
            "romantic": romantic, "famrel": int(famrel),
            "freetime": int(freetime), "goout": int(goout),
            "Dalc": int(Dalc), "Walc": int(Walc), "health": int(health)
        }
    }

    st.info("Sending request to API...")
    try:
        resp = requests.post(API_URL, json=payload, timeout=10)
    except requests.RequestException as e:
        st.error(f"Network error: {e}")
    else:
        if resp.status_code == 200:
            result = resp.json()
            st.success("Prediction received!")
            st.metric("Predicted Final Marks", result.get("predicted_final_Marks", "—"))
            st.write("Remark:", result.get("remark", "—"))
            st.json(result)
        else:
            st.error(f"API error (status {resp.status_code})")
            try:
                st.json(resp.json())
            except Exception:
                st.text(resp.text)
