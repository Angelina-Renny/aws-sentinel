
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Locate project files
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "weather_cleaned.csv"
RESULTS_PATH = BASE_DIR / "reports" / "statistical_anomalies.csv"
OUTPUT_PATH = BASE_DIR / "reports" / "weather_anomalies.png"

# Load datasets
df = pd.read_csv(DATA_PATH, parse_dates=["DATE"])
anomalies = pd.read_csv(RESULTS_PATH, parse_dates=["DATE"])

# Select one day to make the graph easier to read
start = pd.Timestamp("2025-01-03")
end = start + pd.Timedelta(days=1)

daily = df[(df["DATE"] >= start) & (df["DATE"] < end)]

daily_anomalies = anomalies[
    (anomalies["DATE"] >= start)
    & (anomalies["DATE"] < end)
    & anomalies["HourlySeaLevelPressure_iqr_anomaly"].fillna(False).astype(bool)
].copy()

#Convert pressure readings to numbers
daily["HourlySeaLevelPressure"] = pd.to_numeric(
    daily["HourlySeaLevelPressure"], errors="coerce"
)
daily_anomalies["HourlySeaLevelPressure"] = pd.to_numeric(
    daily_anomalies["HourlySeaLevelPressure"], errors="coerce"
)

# Plot pressure over time
plt.figure(figsize=(12, 6))

plt.plot(
    daily["DATE"],
    daily["HourlySeaLevelPressure"],
    label="Observed pressure",
    marker=".",
    linewidth=1
)

plt.scatter(
    daily_anomalies["DATE"],
    daily_anomalies["HourlySeaLevelPressure"],
    label="Potential anomalies",
    marker="x",
    s=80
)

plt.title("AWS Sentinel: Weather Pressure Anomaly Screening")
plt.xlabel("Date and time")
plt.ylabel("Sea-level pressure (dataset units)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()

# Save the graph
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(OUTPUT_PATH, dpi=150)
print("Graph saved to:", OUTPUT_PATH)

plt.show()
