
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from pathlib import Path

# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_DIR / "data" / "weather_model_ready.csv"
REPORT_PATH = PROJECT_DIR / "reports" / "ml_anomalies.csv"
MODEL_PATH = PROJECT_DIR / "models" / "weather_isolation_forest.joblib"

# Features used by our independent ML model
FEATURES = [
    "HourlyDryBulbTemperature",
    "HourlyRelativeHumidity",
    "HourlyWindSpeed",
]

def main():
    # Load prepared weather data
    df = pd.read_csv(DATA_PATH)
    df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce")

    # Keep rows with all required features
    valid = df.dropna(subset=FEATURES + ["DATE"]).copy()

    # Prepare feature matrix
    X = valid[FEATURES]

    # Scale features so they have comparable ranges
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train an unsupervised anomaly detector
    model = IsolationForest(
        n_estimators=200,
        contamination=0.05,
        random_state=42,
        n_jobs=-1,
    )

    predictions = model.fit_predict(X_scaled)

    # -1 means potential anomaly; 1 means normal
    valid["ml_anomaly"] = (predictions == -1).astype(int)
    valid["anomaly_score"] = -model.score_samples(X_scaled)

    # Save model and scaler for later dashboard integration
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

    valid.to_csv(REPORT_PATH, index=False)

    import joblib
    joblib.dump(
        {"model": model, "scaler": scaler, "features": FEATURES},
        MODEL_PATH,
    )

    print("ML anomaly detection completed!")
    print(f"Rows analysed: {len(valid)}")
    print(f"Potential anomalies: {valid['ml_anomaly'].sum()}")
    print(f"Normal observations: {(valid['ml_anomaly'] == 0).sum()}")
    print(f"Results saved to: {REPORT_PATH}")
    print(f"Model saved to: {MODEL_PATH}")

if __name__ == "__main__":
    main()
