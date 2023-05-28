import json
from shapely.geometry import Point, Polygon

data = '''
{
  "last_clicked": {
    "lat": 52.618898050125395,
    "lng": 12.78712570680832
  },
  "last_object_clicked_tooltip": null,
  "all_drawings": [
    {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [
              12.787516,
              52.618979
            ],
            [
              12.787905,
              52.618755
            ],
            [
              12.787646,
              52.61853
            ],
            [
              12.78691,
              52.618586
            ],
            [
              12.787128,
              52.618895
            ],
            [
              12.787516,
              52.618979
            ]
          ]
        ]
      }
    }
  ],
  "last_active_drawing": {
    "type": "Feature",
    "properties": {},
    "geometry": {
      "type": "Polygon",
      "coordinates": [
        [
          [
            12.787516,
            52.618979
          ],
          [
            12.787905,
            52.618755
          ],
          [
            12.787646,
            52.61853
          ],
          [
            12.78691,
            52.618586
          ],
          [
            12.787128,
            52.618895
          ],
          [
            12.787516,
            52.618979
          ]
        ]
      ]
    }
  },
  "bounds": {
    "_southWest": {
      "lat": 52.61756273687321,
      "lng": 12.785570025444033
    },
    "_northEast": {
      "lat": 52.619842515534046,
      "lng": 12.789325118064882
    }
  },
  "zoom": 18,
  "last_circle_radius": null,
  "last_circle_polygon": null,
  "center": {
    "lat": 52.6187026410444,
    "lng": 12.787447571754457
  }
}
'''

data_dict = json.loads(data)
# # You can now access the data like this:
# print(data_dict['last_clicked']['lat']) # Output: 52.618898050125395

images = {'DJI_20230405095432_0001_D.JPG': [53.84474347222222, 12.560018], 'DJI_0010.JPG': [52.61870111111111, 12.787445916666666]}

# Extarct lat, lon from images and store in list for get_centroid(coords)
coords = []
for image in images:
    coords.append(images[image])

print(coords)

# Define polygon from dictionary
polygon_coords = data_dict['last_active_drawing']['geometry']['coordinates'][0]
polygon = Polygon(polygon_coords)

# Filter dictionary to get coordinates that intersect with polygon
all_coords = []
for coord in coords:
    point = Point(coord[1], coord[0])
    if polygon.intersects(point):
        all_coords.append(coord)
print(all_coords)