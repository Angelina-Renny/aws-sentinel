
import pandas as pd

# Load our weather dataset
file_path = "data/LCD_USW00093909_2025.csv"
df = pd.read_csv(file_path)

# Display basic information
print("\n--- FIRST 5 ROWS ---")
print(df.head())

print("\n--- DATASET SIZE ---")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

print("\n--- COLUMN NAMES ---")
print(df.columns.tolist())

print("\n--- DATA TYPES AND MISSING VALUES ---")
df.info()

print("\n--- MISSING VALUES PER COLUMN ---")
print(df.isnull().sum().sort_values(ascending=False).head(15))

print("\n--- DATE RANGE ---")
df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce")
print("First date:", df["DATE"].min())
print("Last date:", df["DATE"].max())

print("\n--- KEY WEATHER COLUMNS ---")
key_columns = [
    "HourlyDryBulbTemperature",
    "HourlyRelativeHumidity",
    "HourlySeaLevelPressure",
    "HourlyWindSpeed",
    "HourlyPrecipitation",
]

for column in key_columns:
    if column in df.columns:
        missing = df[column].isna().sum()
        print(
            f"{column}: "
            f"{df[column].notna().sum()} available, "
            f"{missing} missing"
        )

print("\n--- WEATHER VALUE EXAMPLES ---")

for column in [
    "HourlyDryBulbTemperature",
    "HourlyRelativeHumidity",
    "HourlyWindSpeed",
]:
    print(f"\n{column}")
    print(df[column].dropna().head(10).to_list())

print("\n--- SUMMARY STATISTICS ---")

for column in [
    "HourlyDryBulbTemperature",
    "HourlyRelativeHumidity",
    "HourlyWindSpeed",
]:
    values = pd.to_numeric(df[column], errors="coerce")
    print(f"\n{column}")
    print(values.describe())
