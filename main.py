from uav_img_toolbox.classes.ImageMetaData import ImageMetaData
import os 

def create_image_dict(directory):
    image_dict = {}
    for filename in os.listdir(directory):
        # Only process .jpg and .tif files
        if filename.lower().endswith(('.jpg', '.tif')):
            image_path = os.path.join(directory, filename)
            try:
                image_meta = ImageMetaData(image_path)
                image_dict[image_path] = {
                    'CaptureUUID': image_meta.CaptureUUID,
                    'lat_lon': image_meta.lat_lon,
                }
            except Exception as e:
                print(f"Could not process file {image_path}: {e}")
    return image_dict

directory = 'tests/img/'
image_dict = create_image_dict(directory)
print(image_dict)
