from exiftool import ExifToolHelper
import os

class ImageMetaData:
    """
    Initialize the metadata of the image.

    Uses the ExifToolHelper to extract metadata from the image file.
    If the image path is None, raises a ValueError.

    Returns:
        Adictionary containing the image metadata.
    """
    def __init__(self, image_path):
        self.image_path = image_path
        if self.image_path is None:
          raise ValueError("Image path cannot be None")
        if not os.path.isfile(self.image_path):
          raise ValueError(f"File does not exist: {self.image_path}")        
        if not self.image_path.lower().endswith(('.jpg', '.tif')):
            raise ValueError(f'Invalid image path: {self.image_path}. Must end with .JPG or .TIF.')
        self.metadata = self.init_metadata()
        
    def init_metadata(self):
      metadata = {}      
      with ExifToolHelper() as et:
          for meta in et.get_metadata(self.image_path):
              for k, v in meta.items():
                  metadata[k] = v
      return metadata      
        
    def get_metadata(self):
        return self.metadata
    
    @property
    def lat_lon(self):
        if 'Composite:GPSLatitude' in self.metadata and 'Composite:GPSLongitude' in self.metadata:
          lat = self.metadata['Composite:GPSLatitude']
          lon = self.metadata['Composite:GPSLongitude']
          return lat, lon
        else:
          return None
          
    @property
    def CaptureUUID(self):
        if 'XMP:CaptureUUID' in self.metadata:
          return self.metadata['XMP:CaptureUUID']
        else:
          return None 
        
    def __str__(self):
        output = ""
        current_category = None
        # Find the longest parameter length
        max_parameter_length = max(len(key.split(':', 1)[-1]) for key in self.metadata.keys())
        # Maximum value length
        max_value_length = 50
        for key, value in self.metadata.items():
            split_key = key.split(':', 1)        
            if len(split_key) == 2:
                category, parameter = split_key
            else:
                category, parameter = 'Misc', split_key[0]        
            if category != current_category:
                # Append the category name centered within a line of '#'
                output += '\n' + ('#' * max_value_length) + '\n'
                output += category.center(max_value_length) + '\n'
                output += '#' * max_value_length + '\n'
                current_category = category        
            # Truncate the value if it is too long
            str_value = str(value)
            truncated_value = (str_value[:max_value_length - 2] + '..') if len(str_value) > max_value_length else str_value    
            output += f'    {parameter:<{max_parameter_length}} : {truncated_value}\n'
        return output

# test1 = ImageMetaData("tests/XAG001_0001.JPG")
# print(test1)
# test2 = ImageMetaData("tests/DJI_0010.JPG")
# print(test2.get_CaptureUUID())
