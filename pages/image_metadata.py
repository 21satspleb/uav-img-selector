import streamlit as st
import pandas as pd
from datetime import datetime
import numpy as np
from PIL import Image
import folium
from streamlit_folium import folium_static


def convert_image_to_displayable_format(image_path):
    try:
        # Open the image file
        image = Image.open(image_path)        
        image_data = np.array(image)        
        #Normalize the data to 0-255
        image_data = (image_data / np.max(image_data)) * 255        
        #Convert the normalized data back to an image
        image = Image.fromarray(image_data.astype('uint8'))
        return image
    except Exception as e:
        print(f"Failed to convert image at {image_path}: {e}")
        return None


st.title("Image Metadata Explorer")

# Create two columns
col1, col2 = st.columns(2)


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


with col1:
  # Create a selectbox for the user to select an image
  selected_index = st.selectbox("Select an image", range(df.shape[0]))
  # Get the selected image
  selected_image = df.iloc[selected_index]
  # display dataframe
  st.dataframe(df.drop(columns=['ImagePath']))
with col2:
  # display selected image metadata
  image_path = selected_image['ImagePath']
  if image_path in st.session_state.uav_images.image_dict:
      image_meta = st.session_state.uav_images.image_dict[image_path]
      image = convert_image_to_displayable_format(image_path)
      # Extract latitude and longitude
      lat_lon = image_meta['lat_lon']
      
      # Create a new row of columns
      col2_1, col2_2 = col2.columns(2)

      if lat_lon is not None:
          # Create the map
          map_ = folium.Map(location=[lat_lon[0], lat_lon[1]], zoom_start=13, width=500, height=300)
          # Add the marker
          folium.Marker(location=[lat_lon[0], lat_lon[1]], popup="Selected Image").add_to(map_)
          # Display the map in Streamlit
          with col2_1:
              st.image(image, caption=image_path, width=400)
          with col2_2:
              folium_static(map_, width=300, height=300)
      
      st.write(image_meta['image_meta'].metadata)
  else:
      st.write(f"No metadata found for {image_path}")

