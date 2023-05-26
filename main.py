# Import required libraries
from PIL import Image
from PIL import ExifTags
from PIL.ExifTags import TAGS, GPSTAGS
import os
import shutil
import folium
from folium import IFrame
import streamlit as st
from streamlit_folium import folium_static
from shapely.geometry import Point, Polygon
import geojson
import base64

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
    base_path = '.' if path is None or path is '' else path
    base_path = base_path if os.path.isdir(base_path) else os.path.dirname(base_path)
    base_path = '.' if base_path is None or base_path is '' else base_path

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
        if filename.endswith(".JPG"):
            lat, lon = get_exif_gps(folder_path + "/" + filename)
            # Add tp images dict
            images[filename] = [lat, lon]
            # print(f"Latitude: {lat}")
            # print(f"Longitude: {lon}")
      st.write(f'Your images {images}')
    else:
        st.write('No directories found')
    
    m = folium.Map()
    for img_path, coords in images.items():
      # Create a marker with the image as the icon
      img_path = folder_path + "/" + img_path
      print(img_path)
      icon = folium.Icon(icon="glyphicon glyphicon-eye-open")
      marker = folium.Marker(location=coords, icon=icon)
      
      # Create a popup with the HTML for the image
      encoded = base64.b64encode(open(img_path, 'rb').read())
      svg = """
      <object data="data:image/jpg;base64,{}" width="{}" height="{} type="image/svg+xml">
      </object>""".format
      
      width, height, fat_wh = 300, 300, 1.3 # you can change these attributes as per your image requirements

      iframe = IFrame(svg(encoded.decode('UTF-8'), width, height) , width=width*fat_wh,  height=height*fat_wh)
      
      popup  = folium.Popup(iframe, parse_html=True, max_width=1500)
      # Add the popup to the marker
      marker.add_child(popup)
      # Add the marker to the map
      m.add_child(marker)
    folium_static(m)

  # path = "data/"
  # # Create dict which stores the image paths and their coordinates
  # images = {} 
  # for filename in os.listdir(path):    
  #   if filename.endswith(".JPG"):
  #       lat, lon = get_exif_gps(path + filename)
  #       # Add tp images dict
  #       images[filename] = [lat, lon]
  #       # print(f"Latitude: {lat}")
  #       # print(f"Longitude: {lon}")
  # print(images)
          

# Run the app
if __name__ == "__main__":
    main()