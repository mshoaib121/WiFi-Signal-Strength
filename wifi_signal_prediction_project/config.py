from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR / "data" / "simulated_wifi_dataset.csv"
MODEL_PATH = BASE_DIR / "models" / "wifi_signal_model.joblib"

DEFAULT_FEATURE_COLUMNS = [
    "distance_m",
    "walls",
    "obstacles",
    "frequency_ghz",
    "bandwidth_mhz",
    "congestion_percent",
]

TARGET_COLUMN = "signal_dbm"