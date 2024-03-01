
from shapely import geometry, Point, Polygon
import re
import os

src_path = r"C:\Users\VSU Computer Science\Documents\UVA\Geotab Data Puller\Geotab Data Puller\trips"
file = r"C:\Users\VSU Computer Science\Documents\UVA\Geotab Data Puller\Geotab Data Puller\zone_coords\coords.txt"

coords = []

with open(file, 'r') as infile:
    for line in infile:
        #print(line)
        lon = re.search("X:-?[0-9]+.[0-9]+", line).group()[2:]
        lat = re.search("Y:-?[0-9]+.[0-9]+", line).group()[2:]
        coords.append((lon, lat))
        
coords.pop(-1)
coords = tuple(coords)
print(coords)

polygon = Polygon(coords)


folders = [f for f in os.listdir(src_path)]
for folder in folders:
    folder_path = os.path.join(src_path, folder)
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    print(folder_path)
    for file in files:
        print(file)
        event = []
        file_path = os.path.join(folder_path, file)
        with open(file_path, 'r') as infile:
            for line in infile:
                print(line)
                pass