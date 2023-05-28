# Import required libraries
import os
import shutil
import math
import re
import streamlit as st
import folium
from folium.plugins import Draw
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from streamlit_folium import st_folium
from shapely.geometry import Point, Polygon
import cProfile
import pstats



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

@st.cache_data
def get_exif_gps(image_file_path):
    if image_file_path.lower().endswith('.jpg'):  
      exif_table = {}
      image = Image.open(image_file_path)
      info = image._getexif()      
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
    elif image_file_path.lower().endswith('.tif'):
      image = Image.open(image_file_path)
      metadata = image.tag_v2
      # Extract GPS Latitude and GPS Longitude values with regex
      latitude_pattern = r'drone-dji:GpsLatitude="([-+]?[0-9]*\.?[0-9]+)"'
      longitude_pattern = r'drone-dji:GpsLongitude="([-+]?[0-9]*\.?[0-9]+)"'
      metadata = dict(metadata)
      latitude = float(re.search(latitude_pattern, metadata[700].decode("utf-8")).group(1))
      longitude = float(re.search(longitude_pattern, metadata[700].decode("utf-8")).group(1))
      lat, lon = latitude, longitude
    return lat, lon

@st.cache_data
def get_marker_data(images):
    marker_data = []
    for img_path, coord in images.items():
        # Create marker data
        marker_data.append({"location": coord["coords"], "icon": "glyphicon glyphicon-eye-open"})
    return marker_data

  
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
        m = folium.Map(location=initLocation)
        for img_path, coord in images.items():
          # Create a marker with the image as the icon
          img_path = folder_path + "/" + img_path
          # Fit map bounds to markers
          group = folium.FeatureGroup()        
          # Create a CircleMarker
          circle_marker = folium.CircleMarker(
              location=coord["coords"],
              radius=3,  # Adjust the size of the circles here
              color="blue",
              fill=True,
              fill_color="blue",
          )
          group.add_child(circle_marker)
          # Add the CircleMarker to the map
          m.add_child(circle_marker)

        m.fit_bounds(group.get_bounds())
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


#cProfile.run('main()')

# Run the app
if __name__ == "__main__":
    main()
    