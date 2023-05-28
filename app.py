# Import required libraries
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os
import folium
from folium.plugins import Draw
import streamlit as st
from streamlit_folium import folium_static, st_folium 
import math
import json
import rasterio
from shapely.geometry import Point, Polygon
import shutil

def get_centroid(coords):
    x, y, z = 0, 0, 0
    for lat, lon in coords:
        lat, lon = math.radians(lat), math.radians(lon)
        x += math.cos(lat) * math.cos(lon)
        y += math.cos(lat) * math.sin(lon)
        z += math.sin(lat)

    x /= len(coords)
    y /= len(coords)
    z /= len(coords)

    lon = math.atan2(y, x)
    lat = math.atan2(z, math.sqrt(x ** 2 + y ** 2))
    return (math.degrees(lat), math.degrees(lon))
  
def st_dir_selector(st_placeholder, path='.', label='Please, select a folder...'):
    """
    A function to select a directory in a Streamlit app.
  
    Parameters
    ----------
    st_placeholder : Streamlit placeholder
        Streamlit placeholder to be used for the directory selection.
    path : str
        Path to the directory to be used as the base for the selection.
    label : str
        Label to be used in the selection box.
  
    Returns
    -------
    str
        Path to the selected directory.
    """
    base_path = '.' if path is None or path == '' else path
    base_path = base_path if os.path.isdir(base_path) else os.path.dirname(base_path)
    base_path = '.' if base_path is None or base_path == '' else base_path

    directories = [f.name for f in os.scandir(base_path) if f.is_dir()]
    if not directories:
        return None
    selected_directory = st_placeholder.selectbox(label, directories)
    return os.path.join(base_path, selected_directory)
def get_exif_gps(image_file_path):
    exif_table = {}
    image = Image.open(image_file_path)
    info = image._getexif()
    #print(info)
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        exif_table[decoded] = value
    gps_info = {}
    for key in exif_table['GPSInfo'].keys():
        decode = GPSTAGS.get(key,key)
        gps_info[decode] = exif_table['GPSInfo'][key]
    # Extract GPS coordinates
    latitude = gps_info['GPSLatitude']
    longitude = gps_info['GPSLongitude']
    lat = latitude[0] + latitude[1]/60 + latitude[2]/3600
    lon = longitude[0] + longitude[1]/60 + longitude[2]/3600
    if gps_info['GPSLatitudeRef'] == 'S':
      lat = -lat
    if gps_info['GPSLongitudeRef'] == 'W':
      lon = -lon
    lat = lat.numerator / lat.denominator
    lon = lon.numerator / lon.denominator
    return lat, lon
  
# The main part of the app
def main():
    st.title('UAV Image Selector')
    placeholder = st.empty()
    folder_path = st_dir_selector(placeholder)
  
    if folder_path is not None:
      images = {} 
      for filename in os.listdir(folder_path):    
        if filename.lower().endswith(('.jpg', '.tif')):
            lat, lon = get_exif_gps(folder_path + "/" + filename)
            # Add tp images dict
            images[filename] = {"coords": [lat, lon], "path": folder_path + "/" + filename}

      # Get centroid lcoation of all images to set location of folium map
      coords = [data["coords"] for data in images.values()]
      if coords:  # check if coords is not empty
        initLocation = get_centroid(coords)
        # Generate the Map     
        m = folium.Map(location = initLocation)    
        for img_path, coord in images.items():
          # Create a marker with the image as the icon
          img_path = folder_path + "/" + img_path
          # Fit map bounds to markers
          group = folium.FeatureGroup()        
          icon = folium.Icon(icon="glyphicon glyphicon-eye-open")
          marker = folium.Marker(location=coord["coords"], icon=icon)
          group.add_child(marker)
          # Add the marker to the map
          m.add_child(marker)      
        # Adjust Zoomlevel of the app
        m.fit_bounds(group.get_bounds())
        # Add interactive drawing tools to the map
        Draw(export=True).add_to(m)
        output = st_folium(m, height=700, width=700)
        # Convert Output to dict
        data_dict = output
        # Define polygon from dictionary
        if data_dict is not None and 'last_active_drawing' in data_dict and data_dict['last_active_drawing'] is not None:
          polygon_coords = data_dict['last_active_drawing']['geometry']['coordinates'][0]
          polygon = Polygon(polygon_coords)
          # Filter dictionary to get coordinates that intersect with polygon
          all_coords = {}
          for filename, data in images.items():
            point = Point(data["coords"][1], data["coords"][0])
            if polygon.intersects(point):
                all_coords[filename] = data["coords"]          
          if st.button('Save Selected Images'):
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)  # creates the directory if it doesn't exist
            for filename in all_coords.keys():
                shutil.copy2(images[filename]["path"], output_dir)
            st.success('Images saved successfully!')
          st.write(all_coords)
        else:
          st.write("No active drawing.")      
    else:
        st.write('No JPG or TIF images found in the selected directory.')

# Run the app
if __name__ == "__main__":
    main()