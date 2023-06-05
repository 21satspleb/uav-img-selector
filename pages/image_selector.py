import streamlit as st
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

# center on Liberty Bell, add marker
m = folium.Map(location=[df['LatLon'].apply(lambda x: x[0]).mean(), 
                         df['LatLon'].apply(lambda x: x[1]).mean()], zoom_start=13)

for idx, row in df.iterrows():
    folium.Marker([row['LatLon'][0], row['LatLon'][1]], popup=row['ImageName']).add_to(m)

# Add folium draw to map 
Draw(export=True).add_to(m)
output = st_folium(m, height=700, width=700)
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
  if st.button('Save Selected Images'):
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)  # creates the directory if it doesn't exist
            for idx, row in selected_images.iterrows():
              image_path = row['ImagePath']
              # Copy the image to the output folder
              shutil.copy(image_path, output_dir)
            st.success('Images saved successfully!')
          #st.write(all_coords)

  

  