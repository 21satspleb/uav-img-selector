from uav_img_toolbox.classes.ImageMetaData import ImageMetaData
from uav_img_toolbox.classes.UAVImages import UAVImages
import os 

directory = 'tests/img/'
image_dict = UAVImages(directory)
image_dict.create_image_dict()
print(image_dict)
