import geopandas as gpd
import folium
from folium.plugins import Search

# Load Dakshina Kannada district boundary
gdf = gpd.read_file("dakshina_kannada.geojson")

# Create map
m = folium.Map(location=[12.9, 74.85], zoom_start=9, tiles=None)

# Add multiple base map styles
folium.TileLayer("OpenStreetMap", name="Street").add_to(m)
folium.TileLayer("CartoDB positron", name="Light").add_to(m)
folium.TileLayer("Esri.WorldImagery", name="Satellite").add_to(m)
folium.TileLayer("CartoDB dark_matter", name="Dark").add_to(m)

# Add district boundary with tooltip
folium.GeoJson(
    gdf,
    name="Dakshina Kannada",
    style_function=lambda x: {
        'fillColor': "#1ED56E",
        'color': 'black',
        'weight': 2,
        'fillOpacity': 0.3
    },
    tooltip=folium.GeoJsonTooltip(fields=["district"], aliases=["District"])
).add_to(m)

# Add major towns (added Sullia)
towns = [
    {"name": "Mangalore", "aliases": [], "lat": 12.9141, "lon": 74.8560},
    {"name": "Puttur", "aliases": [], "lat": 12.7597, "lon": 75.2010},
    {"name": "Bantwal", "aliases": [], "lat": 12.8903, "lon": 75.0347},
    {"name": "Moodbidri", "aliases": [], "lat": 13.0836, "lon": 74.9950},
    {"name": "Belthangady", "aliases": [], "lat": 13.0001, "lon": 75.2953},
    {"name": "Sullia", "aliases": [], "lat": 12.5657, "lon": 75.3876},
]
marker_group = folium.FeatureGroup(name="Towns").add_to(m)
# Add markers (with aliases in tooltip for better search)
for town in towns:
    search_text = town["name"]
    if town.get("aliases"):
        search_text += " " + " ".join(town["aliases"])
    folium.Marker(
        location=[town["lat"], town["lon"]],
        popup=f"<b>{town['name']}</b>",
        tooltip=search_text,  # includes aliases
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(marker_group)

for town in towns:
    folium.Marker(
        location=[town["lat"], town["lon"]],
        popup=f"<b>{town['name']}</b>",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

Search(
    layer=marker_group,
    search_label="tooltip",
    placeholder="Search for a town",
    collapsed=False,
    zoom=12
).add_to(m)

# Add layer control
folium.LayerControl().add_to(m)

# Save map
m.save("dakshina_kannada_map.html")
print("Map saved! Open 'dakshina_kannada_map.html'.")
