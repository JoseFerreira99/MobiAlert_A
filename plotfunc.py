import csv
import matplotlib.pyplot as plt
import numpy as np
from math import radians, sin, cos, sqrt, atan2

def haversine_distance(lon1, lat1, lon2, lat2):
    # Convert latitude and longitude from degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6371 * c * 1000  # Earth radius in meters

    return distance

def plot_coordinates_with_color(csv_file):
    center_coords = []
    lon_coords = []
    lat_coords = []

    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and len(row) >= 7 and not row[0].startswith('session'):
                _, _, lon_center_str, lat_center_str, _, lon_GPS_str, lat_GPS_str = row
                lon_center = float(lon_center_str.strip("()"))
                lat_center = float(lat_center_str.strip("()"))
                center_coords.append((lon_center, lat_center))
                lon_GPS = float(lon_GPS_str)
                lat_GPS = float(lat_GPS_str)
                lon_coords.append(lon_GPS)
                lat_coords.append(lat_GPS)

    # Assign colors to centers
    center_colors = plt.cm.tab10(range(len(center_coords)))

    # Assign colors to coordinates based on nearest center
    colors = []
    for lon, lat in zip(lon_coords, lat_coords):
        min_distance = float('inf')
        nearest_color = None
        for i, (center_lon, center_lat) in enumerate(center_coords):
            distance = haversine_distance(lon, lat, center_lon, center_lat)
            if distance < min_distance:
                min_distance = distance
                nearest_color = center_colors[i]
        colors.append(nearest_color)

    # Plotting
    plt.figure(figsize=(10, 6))
    for lon, lat, color in zip(lon_coords, lat_coords, colors):
        plt.scatter(lon, lat, c=[color])
    for i, (lon, lat) in enumerate(center_coords):
        plt.scatter(lon, lat, c=[center_colors[i]], label='Center Coordinates' if i == 0 else None, marker='x')  # Set marker to 'x'
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Plot of Coordinates with Color based on Nearest Center')
    plt.legend()
    plt.grid(True)
    plt.show()

# Replace 'porto.csv' with your CSV file path
plot_coordinates_with_color('/home/jose/Documentos/GitHub/MobiAlert/MobiAlert/Sessions/porto.csv')
