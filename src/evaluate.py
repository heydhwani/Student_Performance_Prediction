import joblib
from data_utils import load_datasets, get_feature_target, label_encode_columns, apply_saved_label_encoders
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def evaluate(model_path="./models/student_pipeline.pkl"):
    # load original raw data
    df = load_datasets("./data")
    # apply saved encoders (so transformations match training)
    df_enc, _ = apply_saved_label_encoders(df, encoders_path="./models/encoders.joblib")
    X, y = get_feature_target(df_enc, "G3")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
