
import pandas as pd
from pathlib import Path

# 1. Locate the cleaned dataset
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "weather_cleaned.csv"
OUTPUT_PATH = BASE_DIR / "reports" / "anomaly_results.csv"

# 2. Load the cleaned weather data
df = pd.read_csv(DATA_PATH)

print("Loaded dataset:", df.shape)

# 3. Define basic physical plausibility checks
# These are screening limits, not universal sensor specifications.
checks = {
    "HourlyDryBulbTemperature": (-90, 60),
    "HourlyRelativeHumidity": (0, 100),
    "HourlySeaLevelPressure": (800, 1100),
    "HourlyWindSpeed": (0, 100),
}

# 4. Create a flag for each measurement
for column, (lower, upper) in checks.items():
    values = df[column]

    df[f"{column}_anomaly"] = (
        values.notna() & ((values < lower) | (values > upper))
    )

# 5. Count potential anomalies
print("\nPotential anomalies by measurement:")

for column in checks:
    count = int(df[f"{column}_anomaly"].sum())
    print(f"{column}: {count}")

# 6. Identify rows with at least one flagged measurement
flag_columns = [f"{column}_anomaly" for column in checks]
df["potential_anomaly"] = df[flag_columns].any(axis=1)

anomalies = df[df["potential_anomaly"]].copy()

# 7. Save the results
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
anomalies.to_csv(OUTPUT_PATH, index=False)

print("\nTotal rows flagged:", len(anomalies))
print("Results saved to:", OUTPUT_PATH)
print("\nAnomaly screening completed!")
