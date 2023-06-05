import streamlit as st
st.set_page_config(
    page_title="3_Select_Images",
    page_icon=":floppy_disk:",
    layout="wide",
    initial_sidebar_state="expanded")
import pandas as pd
import geopandas as gpd
from datetime import datetime
import folium
from folium.plugins import Draw
from streamlit_folium import st_folium
from shapely.geometry import Polygon
import shutil
import os

# Create a pandas dataframe from my images.dict 
data = []
# Iterate over your dictionary
for img_path, img_meta in st.session_state.uav_images.image_dict.items():
    # Extract the image name from the path
    img_name = img_path.split('/')[-1]
    # Extract the date and convert it to a datetime object
    date_str = img_meta['date']
    date = datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S") if date_str is not None else None
    # Add the data to the list
    data.append([img_path, img_name, img_meta['CaptureUUID'], img_meta['lat_lon'], date])

# Create the DataFrame
df = pd.DataFrame(data, columns=['ImagePath', 'ImageName', 'CaptureUUID', 'LatLon', 'Date'])
df = df.reindex(columns=['ImagePath', 'ImageName', 'Date', 'LatLon', 'CaptureUUID'])

# Drop duplicates or None in CaptureUUID
df_unique = df.drop_duplicates(subset=['CaptureUUID'])
df_unique = df_unique[df_unique['CaptureUUID'].notna()]

# Center on the mean latitude and longitude
m = folium.Map(location=[df['LatLon'].apply(lambda x: x[0]).mean(), 
                         df['LatLon'].apply(lambda x: x[1]).mean()], zoom_start=13)

# Add circle markers for unique images
for idx, row in df_unique.iterrows():
    folium.CircleMarker(location=[row['LatLon'][0], row['LatLon'][1]], radius=5, popup=row['ImageName'], color="#f70ac0", fill=True, fill_color="#3186cc").add_to(m)

# Add Esri Satellite tile
folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', 
                 attr='Esri', 
                 name='Esri Satellite', 
                 overlay=False, 
                 control=True).add_to(m)

st.title("Select images by polygon!")
st.markdown("""


##  :floppy_disk: Instructions 
- Step 1: Use the Draw a polygon tool to draw a polygon
around the images you want to select.
- Step 2: Click "Save Selected Images" to save your selection to the output folder in the working directory

Enjoy!

""")
# Add folium draw to map 
Draw(export=True, draw_options={"polyline": {"allowIntersection": False}}).add_to(m)
output = st_folium(m, height=700, width=900)
# Convert Output to dict
data_dict = output
# Define polygon from dictionary
if data_dict is not None and 'last_active_drawing' in data_dict and data_dict['last_active_drawing'] is not None:
  polygon_coords = data_dict['last_active_drawing']['geometry']['coordinates'][0]
  polygon = Polygon(polygon_coords)
  # Convert the DataFrame to a GeoDataFrame
  gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.LatLon.apply(lambda x: x[1]), df.LatLon.apply(lambda x: x[0])))
    
  # Find all points within the polygon
  within_polygon = gdf.within(polygon)
  
  # Get only the rows of the DataFrame that are within the polygon
  selected_images = gdf[within_polygon]
  if st.button('Save Selected Images :floppy_disk:'):
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)  # creates the directory if it doesn't exist
            for idx, row in selected_images.iterrows():
              image_path = row['ImagePath']
              # Copy the image to the output folder
              shutil.copy(image_path, output_dir)
            st.success('Images saved successfully!')


  

  