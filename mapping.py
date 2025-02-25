import folium
import pandas as pd

# Load fire data
df = pd.read_csv("fire_data.csv")
df.columns = df.columns.str.strip().str.lower()  # Standardize column names

# Ensure required columns exist
required_columns = {"latitude", "longitude", "bright_ti4"}
if not required_columns.issubset(df.columns):
    raise KeyError(f"Missing columns in CSV. Found columns: {df.columns}")

# Create a map centered at a specific location
m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

# Add fire markers using bright_ti4
for index, row in df.iterrows():
    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=f"Brightness: {row['bright_ti4']}",
        icon=folium.Icon(color="red")
    ).add_to(m)

# Save and display the map
m.save("fire_map.html")
print("Map saved as fire_map.html")
