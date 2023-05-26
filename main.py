# Import required libraries
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os
import shutil
import folium
import streamlit as st
from shapely.geometry import Point, Polygon
import geojson

def st_dir_selector(st_placeholder, path='.', label='Please, select a folder...'):
    base_path = '.' if path is None or path is '' else path
    base_path = base_path if os.path.isdir(base_path) else os.path.dirname(base_path)
    base_path = '.' if base_path is None or base_path is '' else base_path

    directories = [f.name for f in os.scandir(base_path) if f.is_dir()]
    if not directories:
        return None
    selected_directory = st_placeholder.selectbox(label, directories)
    return os.path.join(base_path, selected_directory)

# The main part of the app
def main():
    st.title('UAV Image Selector')
    placeholder = st.empty()
    folder_path = st_dir_selector(placeholder)
    if folder_path is not None:
        st.write(f'You selected {folder_path}')
    else:
        st.write('No directories found')
    

# Run the app
if __name__ == "__main__":
    main()