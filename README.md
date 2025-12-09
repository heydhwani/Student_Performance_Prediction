# 📚 Student Performance Prediction 

A machine learning-powered web API using **FastAPI** to predict the **final grade (G3)** of students based on demographic, academic, family, and personal data. This project is based on the [UCI Student Performance Dataset](https://archive.ics.uci.edu/dataset/320/student+performance).

---

## 🚀 Features

- Predicts final student grade on a 0–20 scale.
- Organized input via four intuitive sections:
  - Student Details
  - Family Background
  - Academic Status
  - Health Status
- Categorical label encoding with automatic casing normalization.
- Grading remark generation (A+, B, C, etc.).
- Easy Flutter/mobile app integration.

---

## 📂 Project Structure

```
student_performance_prediction/
├── app.py                                            # FastAPI backend logic
├── Student_Performance_model.py                      # Model training script
├── student_performance_portuguese_dataset.csv        # Cleaned Portuguese dataset used for training
├── student_performance_model.joblib                  # Trained RandomForest model
├── label_encoders.joblib                             # Encoders for categorical columns
├── requirements.txt                                  # Python package dependencies
└── README.md                                         # Project documentation
```

---

## 🛠️ Installation

### Prerequisites:
- Python 3.14.0

### Setup:
```bash
# Repository Name
Student_Performance_Prediction

# Create virtual environment
python -m venv venv
venv\Scripts\activate 

# Install dependencies
pip install -r requirements.txt
```

---

## 🏋️‍♂️ Model Training

To train or retrain the model using the dataset:

```bash
python Student_Performance_model.py
```

This will generate the model and encoder files:
- `student_performance_model.joblib`
- `label_encoders.joblib`

---

## 🚦 Running the API

Start the FastAPI server:
```bash
uvicorn app:app --reload
```

Navigate to:
- Swagger Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Root: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Render: [https://student-performance-prediction-8s1j.onrender.com](https://student-performance-prediction-8s1j.onrender.com)

---

## 📥 API Usage

### Endpoint:
```
POST /predict
```

### Request Body Example:
```json
{
  "student": {
    "school": "GP",
    "sex": "M",
    "age": 17,
    "address": "U"
  },
  "family": {
    "famsize": "GT3",
    "Pstatus": "T",
    "Medu": 4,
    "Fedu": 2,
    "Mjob": "teacher",
    "Fjob": "services",
    "reason": "reputation",
    "guardian": "mother",
    "famsup": "yes"
  },
  "academic": {
    "traveltime": 1,
    "studytime": 3,
    "failures": 0,
    "schoolsup": "no",
    "paid": "yes",
    "activities": "yes",
    "internet": "yes",
    "nursery": "yes",
    "higher": "yes",
    "absences": 4,
    "G1": 16,
    "G2": 18
  },
  "health": {
    "romantic": "no",
    "famrel": 4,
    "freetime": 3,
    "goout": 2,
    "Dalc": 1,
    "Walc": 1,
    "health": 4
  }
}
```

### Sample Response:
```json
{
  "predicted_final_Marks": 17.3,
  "remark": "A (Very Good)"
}
```

---

## 🧠 Model Overview

- Algorithm: `RandomForestRegressor`
- Input Features: 31
- Target: `G3` (final grade)
- Evaluation: R² Score ~ 0.84

---

## 📊 Student Performance Dataset — Exploratory Data Analysis (EDA)

This project performs Exploratory Data Analysis (EDA) on the Portuguese Student Performance Dataset to understand data patterns, distributions, correlations, and important features for building machine-learning models.

### 📁 Dataset Path
```bash
Dataset/student_performance_portuguese_dataset.csv
```
### 🛠️Libraries Used
```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
```

## 🚀 EDA Script Overview
The script performs the following tasks:

###  1. Load Dataset & Show Basic Information
This displays:
- `First 5 rows`
- `Column data types`
- `Summary statistics`
- `Missing values in each column`

---

### 2. Histogram for Numeric Columns
Purpose:
- `Understand the distribution of numeric features`
- `Detect skewness`
- `Visualize spread`

---

### 3. Boxplots for Numeric Columns
Purpose:
- `Detect outliers`
- `Compare ranges of numeric variables`

---

### 4. Correlation Heatmap (Numeric Only)
Purpose:
- `Reveal relationships between features`
- `Identify highly correlated variables`
- `Understand influence on final grades`
---

## ▶️ How to Run the EDA Script
1.Install dependencies
```bash
pip install pandas matplotlib seaborn
```
2.Run the script
```bash
python eda.py
```

---

# 🎨 Student Performance Prediction — Streamlit App

This is a **simple Streamlit web application** that allows users to input student details and get a predicted final score using a Machine Learning model hosted on a **FastAPI backend**.

The Streamlit app collects user inputs through a clean UI, sends them as JSON to the FastAPI `/predict` endpoint, and displays the predicted marks and remark.

---

## 🚀 Features

- Clean and simple user interface  
- Form-based inputs for:
  - Student details  
  - Family background  
  - Academic performance  
  - Health and lifestyle  
- Sends POST request to FastAPI backend  
- Displays:
  - Predicted marks  
  - Remark (A+, A, B, C, etc.)  
  - Full JSON response  
- Dropdowns ensure valid categorical inputs (no API errors)

---

## 🌐 API Endpoint Used

The Streamlit app communicates with your deployed FastAPI API:

```
https://student-performance-prediction-8s1j.onrender.com/predict
```
This endpoint accepts a nested JSON body and returns predicted marks + remark.

---

## 📦 How to Run the Streamlit App

### 1️⃣ Install required libraries
```bash
pip install streamlit requests
```
### 2️⃣ Run the app
```bash
streamlit run app.py

```
---

### 📊App Output
The API returns values like:
```json
{
  "predicted_final_Marks": 17.3,
  "remark": "A (Very Good)"
}
```
These results are displayed beautifully inside the Streamlit interface using:

- `st.metric for final marks`
- `A styled remark`
- `Full API JSON response for debugging`

---


## 🖼️ Enhancement Ideas

- Show emoji/photo based on grade in frontend.
- Implement history tracking per student.
- Deploy via Render, Vercel, or Docker.

---

## 📘 Dataset Info

- Source: UCI Portuguese Student Dataset
- [https://archive.ics.uci.edu/dataset/320/student+performance](https://archive.ics.uci.edu/dataset/320/student+performance)

---

