
import pandas as pd
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = PROJECT_DIR / "data" / "weather_model_ready.csv"
ML_PATH = PROJECT_DIR / "reports" / "ml_anomalies.csv"
CONTEXT_PATH = PROJECT_DIR / "reports" / "contextual_anomalies.csv"
STAT_PATH = PROJECT_DIR / "reports" / "statistical_anomalies.csv"

OUTPUT_PATH = PROJECT_DIR / "reports" / "unified_anomaly_report.csv"


def main():
    # Start with the complete model-ready dataset
    df = pd.read_csv(DATA_PATH)
    df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce")

    # Create a report row for every observation
    df = df.dropna(subset=["DATE"]).copy()

    # Default flags: 0 means the method did not flag the observation
    df["ml_anomaly"] = 0
    df["contextual_anomaly"] = 0
    df["isolated_temperature_candidate"] = 0
    df["statistical_anomaly"] = 0

    # Merge Isolation Forest results using timestamp
    ml = pd.read_csv(ML_PATH)
    ml["DATE"] = pd.to_datetime(ml["DATE"], errors="coerce")
    ml = ml.dropna(subset=["DATE"])

    if "ml_anomaly" in ml.columns:
        ml_flags = ml[["DATE", "ml_anomaly"]].drop_duplicates("DATE")
        df = df.merge(ml_flags, on="DATE", how="left", suffixes=("", "_from_ml"))
        df["ml_anomaly"] = df["ml_anomaly_from_ml"].fillna(0).astype(int)
        df = df.drop(columns=["ml_anomaly_from_ml"])

    # Merge contextual detector results
    contextual = pd.read_csv(CONTEXT_PATH)
    contextual["DATE"] = pd.to_datetime(contextual["DATE"], errors="coerce")
    contextual = contextual.dropna(subset=["DATE"])

    context_cols = [
        "DATE",
        "contextual_anomaly",
        "isolated_temperature_candidate",
    ]
    context_flags = contextual[context_cols].drop_duplicates("DATE")

    df = df.merge(
        context_flags,
        on="DATE",
        how="left",
        suffixes=("", "_from_context"),
    )

    for col in ["contextual_anomaly", "isolated_temperature_candidate"]:
        extra_col = col + "_from_context"
        df[col] = df[extra_col].fillna(df[col]).fillna(0).astype(int)
        df = df.drop(columns=[extra_col])

    
    # Merge individual statistical anomaly flags
    stat = pd.read_csv(STAT_PATH)
    stat["DATE"] = pd.to_datetime(stat["DATE"], errors="coerce")
    stat = stat.dropna(subset=["DATE"])

    stat_flag_columns = {
        "HourlyDryBulbTemperature_iqr_anomaly": "temperature_iqr_anomaly",
        "HourlyRelativeHumidity_iqr_anomaly": "humidity_iqr_anomaly",
        "HourlySeaLevelPressure_iqr_anomaly": "pressure_iqr_anomaly",
        "HourlyWindSpeed_iqr_anomaly": "wind_iqr_anomaly",
    }

    for output_col in stat_flag_columns.values():
        df[output_col] = 0

    available_columns = {
        source: output
        for source, output in stat_flag_columns.items()
        if source in stat.columns
    }

    if available_columns:
        stat_flags = stat[["DATE"] + list(available_columns.keys())].copy()
        stat_flags = stat_flags.drop_duplicates("DATE")

        stat_flags = stat_flags.rename(columns=available_columns)

        # These columns exist only for rows selected by the IQR report.
        # Missing matches therefore mean "not flagged", not missing data.
        df = df.drop(
            columns=list(available_columns.values()),
            errors="ignore",
        )

        df = df.merge(stat_flags, on="DATE", how="left")

        for output_col in available_columns.values():
            df[output_col] = df[output_col].fillna(0).astype(int)

    df["statistical_anomaly"] = (
        df[
            [
                "temperature_iqr_anomaly",
                "humidity_iqr_anomaly",
                "pressure_iqr_anomaly",
                "wind_iqr_anomaly",
            ]
        ].max(axis=1).astype(int)
    )

    # Summarize the number of methods flagging each observation
    flag_cols = [
        "ml_anomaly",
        "contextual_anomaly",
        "isolated_temperature_candidate",
        "statistical_anomaly",
    ]

    df["detector_count"] = df[flag_cols].sum(axis=1)

    df["investigation_required"] = (
        df["detector_count"] > 0
    ).astype(int)

    df["investigation_reason"] = df.apply(
        lambda row: ", ".join(
            name
            for col, name in [
                ("ml_anomaly", "Isolation Forest"),
                ("contextual_anomaly", "Large temperature change"),
                ("isolated_temperature_candidate", "Isolated temperature"),
                ("statistical_anomaly", "Statistical detector"),
            ]
            if row[col] == 1
        ),
        axis=1,
    )

    # Preserve original measurements and sort chronologically
    df = df.sort_values("DATE").reset_index(drop=True)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print("Unified anomaly report created!")
    print(f"Observations: {len(df)}")
    print(f"Observations flagged: {df['investigation_required'].sum()}")
    print(
        "Observations flagged by multiple methods:",
        (df["detector_count"] >= 2).sum(),
    )
    print(f"Output: {OUTPUT_PATH}")

    # Display the suspicious May 28 reading for verification
    example = df[df["DATE"] == pd.Timestamp("2025-05-28 08:53:00")]

    if not example.empty:
        print("\nMay 28 event check:")
        print(
            example[
                [
                    "DATE",
                    "HourlyDryBulbTemperature",
                    "ml_anomaly",
                    "contextual_anomaly",
                    "isolated_temperature_candidate",
                    "detector_count",
                    "investigation_reason",
                ]
            ].to_string(index=False)
        )


if __name__ == "__main__":
    main()
