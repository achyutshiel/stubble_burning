import os
import pandas as pd
import folium
from folium.plugins import HeatMap
from flask import Flask, render_template

app = Flask(__name__)

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "fire_data.csv")
TEMPLATES_PATH = os.path.join(BASE_DIR, "templates")

# Ensure templates folder exists
os.makedirs(TEMPLATES_PATH, exist_ok=True)

def create_heatmap():
    try:
        # Load fire data
        df = pd.read_csv(DATA_PATH)

        # Ensure necessary columns exist
        if not {'latitude', 'longitude'}.issubset(df.columns):
            raise ValueError("CSV file must contain 'latitude' and 'longitude' columns.")

        # Drop NaN values
        df = df.dropna(subset=['latitude', 'longitude'])

        # Convert to correct data type
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')

        # Drop any remaining NaNs
        df = df.dropna(subset=['latitude', 'longitude'])

        # Filter data for Delhi/NCR
        delhi_lat_min, delhi_lat_max = 28.1, 28.9
        delhi_lon_min, delhi_lon_max = 76.7, 77.3
        df = df[(df['latitude'] >= delhi_lat_min) & (df['latitude'] <= delhi_lat_max) & 
                (df['longitude'] >= delhi_lon_min) & (df['longitude'] <= delhi_lon_max)]

        # Ensure no non-float values are being passed
        heat_data = df[['latitude', 'longitude']].values.tolist()

        # Create a folium map centered in Delhi/NCR
        map_center = [28.4020, 76.8260]  # Delhi NCR
        m = folium.Map(location=map_center, zoom_start=11)

        # Add heatmap layer
        HeatMap(heat_data).add_to(m)

        # Save the map in the templates folder
        map_path = os.path.join(TEMPLATES_PATH, "fire_map.html")
        m.save(map_path)
        print(f"Heatmap successfully created at {map_path}")

    except Exception as e:
        print(f"Error creating heatmap: {e}")

@app.route("/")
def home():
    create_heatmap()
    return render_template("fire_map.html")

if __name__ == "__main__":
    app.run(debug=True)
