import math
import numpy as np
class Harvesine:
    def __init__(self,lon1, lat1, lon2, lat2):
        self.lon1 = float(lon1)
        self.lat1 = float(lat1)
        self.lon2 = float(lon2)
        self.lat2 = float(lat2)
        
        self.dy = math.radians(self.lat1 - self.lat2)  # Difference in latitudes converted to radians
        self.dx = math.radians(self.lon1 - self.lon2)  # Difference in longitudes converted to radians
        self.dx_angle = math.radians(self.lon2 - self.lon1)
        self.dy_angle = math.radians(self.lat2 - self.lat1)
      
    def harvesine_distance(self): 
        # Calulate distance between point and center #Harvesine Used
        a = math.sin(self.dy / 2) ** 2 + math.cos(math.radians(self.lat1)) * math.cos(math.radians(self.lat2)) * math.sin(self.dx / 2) ** 2 
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        R = 6371  # Earth radius in kilometers
        distance = R * c * 1000  # Convert to meters    
        return distance
    
    def harvesine_angle(self):
        angle = math.atan2(self.dy_angle, self.dx_angle) * 180 / math.pi         
        return angle
"""
def calculate_angle(lon1, lat1, lon2, lat2):

    lon1 = float(lon1)
    lat1 = float(lat1)
    lon2 = float(lon2)
    lat2 = float(lat2)       

    delta_lon = math.radians(lon2 - lon1)
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)

    y = math.sin(delta_lon) * math.cos(phi2)
    x = math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(delta_lon)

    bearing = math.atan2(y, x)
    bearing_degrees = math.degrees(bearing)
    bearing_degrees = (bearing_degrees ) 

    return bearing_degrees
"""