# src/data_utils.py
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import LabelEncoder
import joblib

def load_datasets(data_dir: str = "../data"):
    """
    Load both student-mat.csv and student-por.csv (sep=';'),
    add 'subject' column and return merged dataframe (duplicates dropped).
    """
    data_dir = Path(data_dir)
    mat = pd.read_csv(data_dir / "student-mat.csv", sep=";")
    por = pd.read_csv(data_dir / "student-por.csv", sep=";")
    mat["subject"] = "math"
    por["subject"] = "portuguese"
    df = pd.concat([mat, por], ignore_index=True)
    df = df.drop_duplicates().reset_index(drop=True)
    return df

def get_feature_target(df, target_col="G3"):
    """
    Returns X (features) and y (target).
    """
    X = df.drop(columns=[target_col])
    y = df[target_col]
    return X, y

def label_encode_columns(df, columns, save_path="../models/encoders.joblib"):
    """
    Apply sklearn LabelEncoder for each column in `columns`.
    - Returns transformed dataframe and saves encoders dict to save_path.
    - This is intended for binary or low-cardinality categorical columns
      where label encoding is acceptable.
    """
    encoders = {}
    df = df.copy()
    for col in columns:
        le = LabelEncoder()
        # convert to string to avoid dtype issues
        df[col] = df[col].astype(str)
        df[col] = le.fit_transform(df[col])
        encoders[col] = le
    # save encoders so predictions later use same mapping
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(encoders, save_path)
    return df, encoders