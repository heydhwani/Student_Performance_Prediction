import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
import pandas as pd

from data_utils import load_datasets, get_feature_target, label_encode_columns

def build_preprocessor(X):
    # numeric columns
    numeric_cols = X.select_dtypes(include=["int64","float64"]).columns.tolist()
    # categorical columns (remaining objects)
    categorical_cols = X.select_dtypes(include=["object"]).columns.tolist()

    # Imputer + scaler for numeric
    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    # For remaining categoricals using OneHot (handle_unknown='ignore')
    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse=False))
    ])

    preprocessor = ColumnTransformer([
        ("num", numeric_pipeline, numeric_cols),
        ("cat", categorical_pipeline, categorical_cols)
    ], remainder="drop")
    return preprocessor, numeric_cols, categorical_cols

def main():
    # 1) load
    df = load_datasets("/data")