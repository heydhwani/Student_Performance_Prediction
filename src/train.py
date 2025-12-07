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

    binary_like = [
        "school","sex","address","famsize","Pstatus","schoolsup","famsup",
        "paid","activities","nursery","higher","internet","romantic","subject"
    ]
    # Ensure only columns present are used
    binary_like = [c for c in binary_like if c in df.columns]

    # 3) apply label encoding (this also saves encoders to models/encoders.joblib)
    df_enc, encoders = label_encode_columns(df, binary_like, save_path="/models/encoders.joblib")
    print("Saved label encoders for columns:", list(encoders.keys()))

    # 3) apply label encoding (this also saves encoders to models/encoders.joblib)
    df_enc, encoders = label_encode_columns(df, binary_like, save_path="/models/encoders.joblib")
    print("Saved label encoders for columns:", list(encoders.keys()))

    # 4) features & target
    X, y = get_feature_target(df_enc, target_col="G3")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    preprocessor, numeric_cols, categorical_cols = build_preprocessor(X_train)
    print("Numeric cols:", numeric_cols)
    print("Categorical cols (to OneHot):", categorical_cols)

    pipeline = Pipeline([
        ("preproc", preprocessor),
        ("model", RandomForestRegressor(random_state=42))
    ])

    param_distributions = {
        "model": [RandomForestRegressor(random_state=42), XGBRegressor(objective="reg:squarederror", random_state=42)],
        "model__n_estimators": [50, 100, 200],
        "model__max_depth": [None, 5, 10, 15]
    }

    search = RandomizedSearchCV(
        pipeline,
        param_distributions,
        n_iter=10,
        cv=5,
        scoring="neg_mean_absolute_error",
        n_jobs=-1,
        random_state=42,
        verbose=1
    )

    search.fit(X_train, y_train)
    print("Best params:", search.best_params_)

    best_model = search.best_estimator_
    preds = best_model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    mse = mean_squared_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    print(f"Test MAE: {mae:.3f}, MSE: {mse:.3f}, R2: {r2:.3f}")

    Path("/models").mkdir(parents=True, exist_ok=True)
    joblib.dump(best_model, "/models/student_pipeline.pkl")
    print("Saved pipeline to /models/student_pipeline.pkl")