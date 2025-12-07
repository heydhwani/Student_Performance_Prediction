# src/data_utils.py
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import LabelEncoder
import joblib

def load_datasets(data_dir: str = "../data"):
    
    data_dir = Path(data_dir)
    mat = pd.read_csv(data_dir / "student-mat.csv", sep=";")
    por = pd.read_csv(data_dir / "student-por.csv", sep=";")
    mat["subject"] = "math"
    por["subject"] = "portuguese"
    df = pd.concat([mat, por], ignore_index=True)
    df = df.drop_duplicates().reset_index(drop=True)
    return df

def get_feature_target(df, target_col="G3"):
    
    X = df.drop(columns=[target_col])
    y = df[target_col]
    return X, y

def label_encode_columns(df, columns, save_path="../models/encoders.joblib"):
    
    encoders = {}
    df = df.copy()
    for col in columns:
        le = LabelEncoder()
        
        df[col] = df[col].astype(str)
        df[col] = le.fit_transform(df[col])
        encoders[col] = le
    
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(encoders, save_path)
    return df, encoders

def apply_saved_label_encoders(df, encoders_path="../models/encoders.joblib"):
    
    encoders = joblib.load(encoders_path)
    df = df.copy()
    for col, le in encoders.items():
        # If column missing in new sample, skip or raise
        if col in df.columns:
            df[col] = df[col].astype(str)  # ensure consistent dtype
            # handle unseen labels: map unseen to -1 (or a safe value)
            mapped = []
            for v in df[col].tolist():
                if v in le.classes_:
                    mapped.append(int(le.transform([v])[0]))
                else:
                    mapped.append(-1)
            df[col] = mapped
    return df, encoders