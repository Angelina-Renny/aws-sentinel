
import pandas as pd
from pathlib import Path

# 1. Locate the cleaned dataset
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "weather_cleaned.csv"
OUTPUT_PATH = BASE_DIR / "reports" / "temperature_change_flags.csv"

# 2. Load and prepare the observations
df = pd.read_csv(DATA_PATH, parse_dates=["DATE"])

column = "HourlyDryBulbTemperature"
df[column] = pd.to_numeric(df[column], errors="coerce")

df = (
    df.dropna(subset=["DATE"])
    .sort_values("DATE")
    .reset_index(drop=True)
)

# 3. Calculate time between consecutive observations
df["time_gap_hours"] = (
    df["DATE"].diff().dt.total_seconds() / 3600
)

# 4. Calculate the temperature change
df["temperature_change"] = df[column].diff()

# Calculate change per hour only when the gap is positive
# and no longer than two hours.
valid_gap = (
    df["time_gap_hours"].gt(0)
    & df["time_gap_hours"].le(2)
)

df["temperature_change_per_hour"] = (
    df["temperature_change"] / df["time_gap_hours"]
).where(valid_gap)

# 5. Flag unusually large changes for investigation.
# This is an initial screening threshold, not a validated fault limit.
threshold = 10.0

df["potential_change_anomaly"] = (
    df["temperature_change_per_hour"].abs() > threshold
)

# 6. Show and save the flagged observations
flags = df[df["potential_change_anomaly"]].copy()

print("Temperature change screening completed!")
print("Total observations:", len(df))
print("Valid short-interval comparisons:", int(valid_gap.sum()))
print("Potential sudden changes:", len(flags))

print("\n--- FIRST 10 FLAGGED CHANGES ---")

display_columns = [
    "DATE",
    column,
    "time_gap_hours",
    "temperature_change",
    "temperature_change_per_hour",
]

if flags.empty:
    print("No changes exceeded the initial threshold.")
else:
    print(flags[display_columns].head(10).to_string(index=False))

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
flags.to_csv(OUTPUT_PATH, index=False)

print("\nResults saved to:", OUTPUT_PATH)
print("\nResults saved to:", OUTPUT_PATH)

# 7. Inspect the largest actual temperature changes
print("\n--- LARGEST TEMPERATURE CHANGES ---")

largest_changes = (
    df.dropna(subset=["temperature_change"])
    .assign(
        absolute_change=lambda data:
        data["temperature_change"].abs()
    )
    .sort_values("absolute_change", ascending=False)
)

print(
    largest_changes[
        [
            "DATE",
            "HourlyDryBulbTemperature",
            "time_gap_hours",
            "temperature_change",
            "temperature_change_per_hour",
        ]
    ].head(10).to_string(index=False)
)

print("\n--- CHANGE SIZE SUMMARY ---")
print(df["temperature_change"].abs().describe())

# 8. Investigate the largest temperature jump
print("\n--- INVESTIGATING THE LARGEST TEMPERATURE JUMP ---")

largest_index = df["temperature_change"].abs().idxmax()

start_index = max(0, largest_index - 3)
end_index = min(len(df), largest_index + 4)

inspection_columns = [
    "DATE",
    "HourlyDryBulbTemperature",
    "time_gap_hours",
    "temperature_change",
]

print(
    df.loc[start_index:end_index - 1, inspection_columns]
    .to_string(index=False)
)

# 9. Inspect other weather measurements around the suspicious reading
print("\n--- WEATHER CONDITIONS AROUND MAY 28, 2025 ---")

raw_path = BASE_DIR / "data" / "LCD_USW00093909_2025.csv"
raw = pd.read_csv(raw_path, low_memory=False)

print("\n--- TEMPERATURE QUALITY COLUMNS ---")

quality_columns = [
    col for col in raw.columns
    if "Quality" in col
    or "quality" in col
]

print(quality_columns)

print("\n--- TEMPERATURE-RELATED COLUMNS ---")

temperature_columns = [
    col for col in raw.columns
    if "Temperature" in col
    or "temperature" in col
]

print(temperature_columns)


raw["DATE"] = pd.to_datetime(raw["DATE"], errors="coerce")

start_time = pd.Timestamp("2025-05-28 07:00:00")
end_time = pd.Timestamp("2025-05-28 11:00:00")

period = raw[
    (raw["DATE"] >= start_time)
    & (raw["DATE"] <= end_time)
].copy()

columns_to_check = [
    "DATE",
    "REPORT_TYPE",
    "HourlyDryBulbTemperature",
    "HourlyDewPointTemperature",
    "HourlyRelativeHumidity",
    "HourlySeaLevelPressure",
    "HourlyWindSpeed",
    "HourlySkyConditions",
    "REM",
]

available_columns = [
    column for column in columns_to_check
    if column in period.columns
]

print(period[available_columns].to_string(index=False))

# Investigate the suspicious temperature record
print("\n--- SUSPICIOUS RAW TEMPERATURE RECORD ---")

target_time = pd.Timestamp("2025-05-28 08:53:00")

raw_record = raw.loc[
    raw["DATE"] == target_time
].copy()


    
columns_to_check = [
    "DATE",
    "REPORT_TYPE",
    "HourlyDryBulbTemperature",
    "HourlyDryBulbTemperature_Quality",
    "HourlyDewPointTemperature",
    "HourlyDewPointTemperature_Quality",
    "HourlyRelativeHumidity",
    "HourlySeaLevelPressure",
    "HourlyWindSpeed",
    "REM",
]


available_columns = [
    col for col in columns_to_check
    if col in raw_record.columns
]

print(raw_record[available_columns].to_string(index=False))
