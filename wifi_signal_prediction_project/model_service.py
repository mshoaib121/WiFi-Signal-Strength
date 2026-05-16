import joblib
import pandas as pd
import streamlit as st

from config import DEFAULT_FEATURE_COLUMNS, MODEL_PATH


@st.cache_resource
def load_model_bundle():
    if not MODEL_PATH.exists():
        st.error(f"Model file not found: {MODEL_PATH}")
        st.info("Please keep your trained model at: models/wifi_signal_model.joblib")
        st.stop()

    loaded_data = joblib.load(MODEL_PATH)

    if isinstance(loaded_data, dict) and "model" in loaded_data:
        loaded_data.setdefault("feature_columns", DEFAULT_FEATURE_COLUMNS)
        return loaded_data

    return {
        "model": loaded_data,
        "feature_columns": DEFAULT_FEATURE_COLUMNS,
        "target_column": "signal_dbm",
    }


def predict_signal(model_bundle: dict, values: dict) -> float:
    feature_columns = model_bundle.get("feature_columns", DEFAULT_FEATURE_COLUMNS)

    input_df = pd.DataFrame([values])
    input_df = input_df[feature_columns]

    prediction = model_bundle["model"].predict(input_df)[0]
    return round(float(prediction), 2)