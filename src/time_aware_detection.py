
import pandas as pd
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = PROJECT_DIR / "data" / "weather_model_ready.csv"
REPORT_PATH = PROJECT_DIR / "reports" / "time_aware_anomalies.csv"

MAX_GAP_MINUTES = 120
TEMP_CHANGE_THRESHOLD = 5.0  # Initial investigation threshold in °C


def main():
    df = pd.read_csv(DATA_PATH)
    df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce")

    df = df.dropna(subset=["DATE"])
    df = df.sort_values("DATE").reset_index(drop=True)

    # Identify duplicate timestamps before calculating changes.
    df["duplicate_timestamp"] = df["DATE"].duplicated(keep=False)

    # Calculate elapsed time and temperature change.
    df["gap_minutes"] = (
        df["DATE"].diff().dt.total_seconds() / 60
    )

    previous_temp = df["HourlyDryBulbTemperature"].shift(1)

    df["previous_temperature"] = previous_temp
    df["temp_change"] = (
    df["HourlyDryBulbTemperature"] - previous_temp
    )
    df["temp_abs_change"] = df["temp_change"].abs()


    # Only compare readings with a positive, sufficiently short gap.
    valid_interval = (
        (df["gap_minutes"] > 0)
        & (df["gap_minutes"] <= MAX_GAP_MINUTES)
        & df["HourlyDryBulbTemperature"].notna()
        & df["HourlyDryBulbTemperature"].shift(1).notna()
        & (~df["duplicate_timestamp"])
        & (~df["duplicate_timestamp"].shift(1, fill_value=False))
    )

    df["previous_DATE"] = df["DATE"].shift(1)

    # Initial candidate flags, not confirmed sensor failures.
    df["change_anomaly"] = (
        valid_interval
        & (df["temp_abs_change"] >= TEMP_CHANGE_THRESHOLD)
    ).astype(int)

    df["long_gap"] = (
        df["gap_minutes"] > MAX_GAP_MINUTES
    ).astype(int)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(REPORT_PATH, index=False)

    print("Time-aware detection completed!")
    print(f"Rows analysed: {len(df)}")
    print(f"Candidate temperature changes: {df['change_anomaly'].sum()}")
    print(f"Long gaps: {df['long_gap'].sum()}")
    print(f"Rows with duplicate timestamps: {df['duplicate_timestamp'].sum()}")
    print(f"Results saved to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
