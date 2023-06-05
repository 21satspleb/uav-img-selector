from uav_img_toolbox.classes.UAVImages import UAVImages
import os 

#Tests
directory = "tests/xag"
image_dict = UAVImages(directory).create_image_dict()
#print(image_dict)
#print(image_dict["tests/xag/XAG001_0001.JPG"]["image_meta"])
#print(image_dict["tests/xag/XAG001_0001.JPG"]["image_meta"].metadata)
print(image_dict["tests/xag/XAG001_0001.JPG"]["image_meta"])


# Extract data from the dictionary
#image_name = list(image_dict.keys())
#print(image_name)


# image_aquisition_date = [data[key]['image_meta']['EXIF:ModifyDate'] for key in data]
# lat_lon = [data[key]['lat_lon'] for key in data]

# import streamlit as st
# from PIL import Image
# import numpy as np

# def convert_image_to_displayable_format(image_path):
#     try:
#         # Open the image file
#         image = Image.open(image_path)        
#         image_data = np.array(image)        
#         #Normalize the data to 0-255
#         image_data = (image_data / np.max(image_data)) * 255        
#         #Convert the normalized data back to an image
#         image = Image.fromarray(image_data.astype('uint8'))
#         return image
#     except Exception as e:
#         print(f"Failed to convert image at {image_path}: {e}")
#         return None

# # Open the image
# #image = Image.open('tests/img_folder/DJI_20230405095551_0039_MS_G.TIF')
# image = convert_image_to_displayable_format('tests/img_folder/DJI_20230405095432_0001_D.JPG')
# st.image(image, caption='Sunrise by the mountains')


# # #Convert the image data to a numpy array
# # image_data = np.array(image)

# # #Normalize the data to 0-255
# # image_data = (image_data / np.max(image_data)) * 255

# # #Convert the normalized data back to an image
# # image = Image.fromarray(image_data.astype('uint8'))

# # # Display the image
# # st.image(image, caption='Sunrise by the mountains')
