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

def load_fire_data():
    """ Load and filter fire data for Delhi NCR. """
    df = pd.read_csv(DATA_PATH)
    
    # Ensure required columns exist
    required_columns = {"latitude", "longitude", "bright_ti4"}
    if not required_columns.issubset(df.columns):
        raise ValueError("CSV file must contain latitude, longitude, and bright_ti4 columns.")
    
    # Drop NaN values
    df = df.dropna(subset=["latitude", "longitude", "bright_ti4"])
    
    # Convert to correct data types
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    df["bright_ti4"] = pd.to_numeric(df["bright_ti4"], errors="coerce")
    
    # Drop remaining NaN values
    df = df.dropna()
    
    # Filter for Delhi NCR region
    delhi_lat_min, delhi_lat_max = 28.1, 28.9
    delhi_lon_min, delhi_lon_max = 76.7, 77.3
    df = df[(df["latitude"] >= delhi_lat_min) & (df["latitude"] <= delhi_lat_max) &
            (df["longitude"] >= delhi_lon_min) & (df["longitude"] <= delhi_lon_max)]
    
    return df

def create_heatmap():
    """ Generate heatmap from fire data and save as HTML. """
    df = load_fire_data()
    
    # Create folium map centered at Delhi NCR
    map_center = [28.4020, 76.8260]
    m = folium.Map(location=map_center, zoom_start=11)
    
    # Prepare heatmap data
    heat_data = df[["latitude", "longitude", "bright_ti4"]].values.tolist()
    HeatMap(heat_data, min_opacity=0.5, max_zoom=10, radius=15, blur=10).add_to(m)
    
    # Save the map in templates folder
    map_path = os.path.join(TEMPLATES_PATH, "fire_map.html")
    m.save(map_path)
    print(f"Heatmap successfully created at {map_path}")

@app.route("/")
def home():
    create_heatmap()
    return render_template("fire_map.html")

if __name__ == "__main__":
    app.run(debug=True)
