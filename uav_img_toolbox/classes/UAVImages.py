import os
import glob
import streamlit as st
from exiftool import ExifToolHelper

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

