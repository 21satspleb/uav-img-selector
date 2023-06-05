# from uav_img_toolbox.classes.UAVImages import UAVImages
# import os 

# #Tests
# directory = "tests/xag"
# image_dict = UAVImages(directory).create_image_dict()
# #print(image_dict)
# #print(image_dict["tests/xag/XAG001_0001.JPG"]["image_meta"])
# #print(image_dict["tests/xag/XAG001_0001.JPG"]["image_meta"].metadata)
# print(image_dict["tests/xag/XAG001_0001.JPG"]["image_meta"])


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

# import os
# import glob
# import time
# from exiftool import ExifToolHelper

# # replace with your actual directory
# directory = "tests\img#2"

# # generate a list of all jpg and png images in the directory
# image_paths = glob.glob(os.path.join(directory, "*.[jJ][pP][gG]")) + glob.glob(os.path.join(directory, "*.[pP][nN][gG]"))

# start_time = time.time()  # start timing

# with ExifToolHelper() as et:
#     metadata = et.execute_json(*image_paths)

# # prints a number for every 10th entry
# for i, meta in enumerate(metadata, start=1):
#     if i % 10 == 0:
#         print(i)

# end_time = time.time()  # end timing

# print(f"\nExecution time: {end_time - start_time} seconds")

import os
import glob
import streamlit as st
#from uav_img_toolbox.classes.ImageMetaData import ImageMetaData
from exiftool import ExifToolHelper

# # class UAVImages:
#   """
#   This class is used to create a dictionary of image metadata
#   """
#   def __init__(self, directory):
#    self.directory = directory
#    self.image_dict = {} 
  
#   def create_image_dict(self, progress_bar=None):
#           filenames = [filename for filename in os.listdir(self.directory) 
#                        if filename.lower().endswith(('.jpg', '.tif'))]
#           num_files = len(filenames)
#           for i, filename in enumerate(filenames, start=1):
#               image_path = os.path.join(self.directory, filename)
#               try:
#                   image_meta = ImageMetaData(image_path)
#                   self.image_dict[image_path] = {
#                       'CaptureUUID': image_meta.CaptureUUID,
#                       'lat_lon': image_meta.lat_lon,
#                       'date': image_meta.get_metadata()["EXIF:ModifyDate"],
#                       'image_meta' : image_meta
#                   }
#               except Exception as e:
#                   print(f"Could not process file {image_path}: {e}")
#               # Update progress bar, if one was provided
#               if progress_bar is not None:
#                   progress_bar.progress(i / num_files)
#           return self.image_dict
    
#   def __str__(self):
#       output = ""
#       for image_path, meta in self.image_dict.items():
#           output += f"Image Path: {image_path}\n"
#           output += f"CaptureUUID: {meta['CaptureUUID']}\n"
#           output += f"Latitude: {meta['lat_lon'][0] if meta['lat_lon'] is not None else 'None'}\n"
#           output += f"Longitude: {meta['lat_lon'][1] if meta['lat_lon'] is not None else 'None'}\n"
#           output += "-"*50 + "\n"  # separator between images
#       return output

class UAVImages:
    """
    This class is used to create a dictionary of image metadata
    """
    def __init__(self, directory):
        self.directory = directory
        self.image_dict = {}

    def create_image_dict(self, progress_bar=None):
        image_paths = glob.glob(os.path.join(self.directory, "*.[jJ][pP][gG]")) + glob.glob(os.path.join(self.directory, "*.[tT][iI][fF]"))
        num_files = len(image_paths)
        with ExifToolHelper() as et:
            metadata_list = et.execute_json(*image_paths)

        for i, metadata in enumerate(metadata_list, start=1):
            image_path = metadata['SourceFile']
            try:
                lat_lon = (metadata['Composite:GPSLatitude'], metadata['Composite:GPSLongitude']) if 'Composite:GPSLatitude' in metadata and 'Composite:GPSLongitude' in metadata else None
                self.image_dict[image_path] = {
                    'CaptureUUID': metadata['XMP:CaptureUUID'] if 'XMP:CaptureUUID' in metadata else None,
                    'lat_lon': lat_lon,
                    'date': metadata["EXIF:ModifyDate"] if "EXIF:ModifyDate" in metadata else None,
                    'image_meta': metadata  # the complete metadata dictionary
                }
            except Exception as e:
                print(f"Could not process file {image_path}: {e}")
            # Update progress bar, if one was provided
            if progress_bar is not None:
                progress_bar.progress(i / num_files)
        return self.image_dict

    def __str__(self):
        output = ""
        for image_path, meta in self.image_dict.items():
            output += f"Image Path: {image_path}\n"
            output += f"CaptureUUID: {meta['CaptureUUID']}\n"
            output += f"Latitude: {meta['lat_lon'][0] if meta['lat_lon'] is not None else 'None'}\n"
            output += f"Longitude: {meta['lat_lon'][1] if meta['lat_lon'] is not None else 'None'}\n"
            output += "-"*50 + "\n"  # separator between images
        return output

#Test

test = UAVImages("tests\img_folder")
test.create_image_dict()
print(test)
