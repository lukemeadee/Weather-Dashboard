import requests
import pandas as pd

# Base URL for API
url = "https://api.open-meteo.com/v1/forecast"

# Add parameters in as a dictionary
params = {
    "latitude": -37.9918,
    "longitude": 145.0813,
    "hourly": "temperature_2m,wind_speed_10m,precipitation,relative_humidity_2m",
    "timezone": "auto",
    "forecast_days": 7,
    "current_weather": True
}

# Request weather data from Open Meteo API 
try:
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

except requests.exceptions.RequestException as e:
    print(f"Error retrieving weather data: {e}")
    exit()

# Assign and extract current weather params 
weather = data["current_weather"]["time"]
current_temp = data["current_weather"]["temperature"]

print("=" * 90)
print("WEATHER DASHBOARD".center(90))
print("=" * 90)
print("Location: Parkdale")
print(f"Time updated: {weather}")
print(f"Current temperature: {current_temp}°C")

# Extract hourly data
hourly = data["hourly"]

# Convert hourly weather data into a DataFrame to filter by time
df = pd.DataFrame(hourly)

df["time"] = pd.to_datetime(df["time"])

current_time = pd.to_datetime(
    data["current_weather"]["time"]
).floor("h")

current_forecast = df[df["time"] == current_time]

current_index = df[df["time"] == current_time].index[0]
next_12_hours = df.iloc[current_index : current_index + 12]

print("=" * 90)
print("CURRENT HOUR FORECAST".center(90))
print("=" * 90)

print(current_forecast.to_string(index=False))

print("=" * 90)
print("NEXT 12 HOURS".center(90))
print("=" * 90)

print(next_12_hours.to_string(index=False))

print("=" * 90)
print("Data by Open Meteo".center(90))
print("=" * 90)