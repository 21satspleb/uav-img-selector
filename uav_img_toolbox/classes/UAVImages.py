import os
import streamlit as st
from uav_img_toolbox.classes.ImageMetaData import ImageMetaData

class UAVImages:
  """
  This class is used to create a dictionary of image metadata
  """
  def __init__(self, directory):
   self.directory = directory
   self.image_dict = {} 
  
  def create_image_dict(self, progress_bar=None):
          filenames = [filename for filename in os.listdir(self.directory) 
                       if filename.lower().endswith(('.jpg', '.tif'))]
          num_files = len(filenames)
          for i, filename in enumerate(filenames, start=1):
              image_path = os.path.join(self.directory, filename)
              try:
                  image_meta = ImageMetaData(image_path)
                  self.image_dict[image_path] = {
                      'CaptureUUID': image_meta.CaptureUUID,
                      'lat_lon': image_meta.lat_lon,
                      'date': image_meta.get_metadata()["EXIF:ModifyDate"],
                      'image_meta' : image_meta
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
