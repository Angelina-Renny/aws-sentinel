
import pandas as pd
from pathlib import Path

# 1. Locate the project folders
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "LCD_USW00093909_2025.csv"
OUTPUT_PATH = BASE_DIR / "data" / "weather_cleaned.csv"

# 2. Load the original weather dataset
df = pd.read_csv(DATA_PATH, low_memory=False)

print("Original dataset shape:", df.shape)

# 3. Keep only the columns needed for our prototype
weather_columns = [
    "DATE",
    "HourlyDryBulbTemperature",
    "HourlyRelativeHumidity",
    "HourlySeaLevelPressure",
    "HourlyWindSpeed",
    "HourlyPrecipitation",
]

df = df[weather_columns].copy()

# 4. Convert date and weather measurements into usable formats
df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce")

measurement_columns = weather_columns[1:]

for column in measurement_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# 5. Sort observations by date
df = df.sort_values("DATE").reset_index(drop=True)

# 6. Display missing values before handling them
print("\nMissing values before cleaning:")
print(df.isnull().sum())

# 7. Remove rows without a valid timestamp
df = df.dropna(subset=["DATE"])

# 8. Save the cleaned dataset
df.to_csv(OUTPUT_PATH, index=False)

print("\nCleaned dataset shape:", df.shape)
print("Saved cleaned dataset to:", OUTPUT_PATH)
print("\nCleaning completed successfully!")
