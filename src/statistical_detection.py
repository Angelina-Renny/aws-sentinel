
import pandas as pd
from pathlib import Path

# 1. Locate the cleaned dataset
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "weather_cleaned.csv"
OUTPUT_PATH = BASE_DIR / "reports" / "statistical_anomalies.csv"

# 2. Load the data
df = pd.read_csv(DATA_PATH)

# 3. Select measurements to analyse
columns = [
    "HourlyDryBulbTemperature",
    "HourlyRelativeHumidity",
    "HourlySeaLevelPressure",
    "HourlyWindSpeed",
]

print("Statistical anomaly detection started!")
print("Dataset shape:", df.shape)

# 4. Apply the IQR method to each measurement
for column in columns:
    values = pd.to_numeric(df[column], errors="coerce")
    valid = values.dropna()

    if valid.empty:
        df[f"{column}_iqr_anomaly"] = False
        print(f"\n{column}: no valid readings")
        continue

    q1 = valid.quantile(0.25)
    q3 = valid.quantile(0.75)
    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    df[f"{column}_iqr_anomaly"] = (
        values.notna()
        & ((values < lower_bound) | (values > upper_bound))
    )

    count = int(df[f"{column}_iqr_anomaly"].sum())

    print(f"\n{column}")
    print(f"Lower statistical boundary: {lower_bound:.2f}")
    print(f"Upper statistical boundary: {upper_bound:.2f}")
    print(f"Potential anomalies: {count}")

# 5. Flag rows with at least one unusual measurement
flag_columns = [f"{column}_iqr_anomaly" for column in columns]
df["potential_statistical_anomaly"] = df[flag_columns].any(axis=1)

anomalies = df[df["potential_statistical_anomaly"]].copy()

# 6. Save the results
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
anomalies.to_csv(OUTPUT_PATH, index=False)

print("\nTotal rows flagged:", len(anomalies))
print("Results saved to:", OUTPUT_PATH)
print("Statistical anomaly detection completed!")

# 7. Inspect the first 10 flagged observations
print("\n--- FIRST 10 POTENTIAL ANOMALIES ---")

columns_to_show = [
    "DATE",
    "HourlyDryBulbTemperature",
    "HourlyRelativeHumidity",
    "HourlySeaLevelPressure",
    "HourlyWindSpeed",
]

print(anomalies[columns_to_show].head(10).to_string(index=False))

# 8. Count how often each measurement was flagged
print("\n--- FLAG COUNTS ---")

for column in columns:
    flag_column = f"{column}_iqr_anomaly"
    print(f"{column}: {int(anomalies[flag_column].sum())}")
