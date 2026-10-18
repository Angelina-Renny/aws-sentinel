
import pandas as pd
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_DIR / "data" / "weather_model_ready.csv"
REPORT_PATH = PROJECT_DIR / "reports" / "contextual_anomalies.csv"

# Initial investigation settings — not scientifically validated thresholds
MAX_GAP_MINUTES = 120
TEMP_CHANGE_THRESHOLD = 5.0


def main():
    df = pd.read_csv(DATA_PATH)

    df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce")
    df["HourlyDryBulbTemperature"] = pd.to_numeric(
        df["HourlyDryBulbTemperature"], errors="coerce"
    )

    df = df.dropna(subset=["DATE"]).sort_values("DATE").reset_index(drop=True)

    # Identify duplicate timestamps
    df["duplicate_timestamp"] = df["DATE"].duplicated(keep=False)

    # Compare each temperature with the previous observation
    df["previous_DATE"] = df["DATE"].shift(1)
    df["previous_temperature"] = df["HourlyDryBulbTemperature"].shift(1)

    df["gap_minutes"] = (
        df["DATE"] - df["previous_DATE"]
    ).dt.total_seconds() / 60

    df["temperature_change"] = (
        df["HourlyDryBulbTemperature"] - df["previous_temperature"]
    )

    df["absolute_temperature_change"] = df["temperature_change"].abs()

    # Only compare valid temperatures across reasonable time gaps
    valid_interval = (
        (df["gap_minutes"] > 0)
        & (df["gap_minutes"] <= MAX_GAP_MINUTES)
        & df["HourlyDryBulbTemperature"].notna()
        & df["previous_temperature"].notna()
        & (~df["duplicate_timestamp"])
        & (~df["duplicate_timestamp"].shift(1, fill_value=False))
    )

    df["contextual_anomaly"] = (
        valid_interval
        & (df["absolute_temperature_change"] >= TEMP_CHANGE_THRESHOLD)
    ).astype(int)

    # Investigate unusually isolated temperature readings.
    # Compare with the closest valid temperature before and after,
    # provided both observations are within the allowed time window.
    next_date = df["DATE"].shift(-1)
    next_temp = df["HourlyDryBulbTemperature"].shift(-1)
    next_gap = (next_date - df["DATE"]).dt.total_seconds() / 60

    df["next_DATE"] = next_date
    df["next_temperature"] = next_temp
    df["next_gap_minutes"] = next_gap

    
# Find the nearest valid temperature before and after each reading
    temperature = df["HourlyDryBulbTemperature"]

    previous_valid_temp = temperature.ffill().shift(1)
    previous_valid_date = df["DATE"].where(temperature.notna()).ffill().shift(1)

    next_valid_temp = temperature.bfill().shift(-1)
    next_valid_date = df["DATE"].where(temperature.notna()).bfill().shift(-1)

    previous_valid_gap = (
        df["DATE"] - previous_valid_date
    ).dt.total_seconds() / 60

    next_valid_gap = (
        next_valid_date - df["DATE"]
    ).dt.total_seconds() / 60

    has_neighbors = (
    temperature.notna()
    & (previous_valid_gap > 0)
    & (previous_valid_gap <= MAX_GAP_MINUTES)
    & (next_valid_gap > 0)
    & (next_valid_gap <= MAX_GAP_MINUTES)
    & (~df["duplicate_timestamp"])
)


    
    df["neighbor_temperature_difference"] = (
    temperature - (previous_valid_temp + next_valid_temp) / 2
    ).abs()


    df["isolated_temperature_candidate"] = (
        has_neighbors
        & (df["neighbor_temperature_difference"] >= TEMP_CHANGE_THRESHOLD)
    ).astype(int)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(REPORT_PATH, index=False)

    print("Contextual detection completed!")
    print(f"Rows analysed: {len(df)}")
    print(f"Large temperature-change candidates: {df['contextual_anomaly'].sum()}")
    print(
        "Isolated temperature candidates:",
        df["isolated_temperature_candidate"].sum()
    )
    print(
        "Rows with missing ML features:",
        int(
            df[
                [
                    "HourlyDryBulbTemperature",
                    "HourlyRelativeHumidity",
                    "HourlyWindSpeed",
                ]
            ].isna().any(axis=1).sum()
        ),
    )
    print(f"Results saved to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
