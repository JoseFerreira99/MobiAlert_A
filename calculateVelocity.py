from Harvesine import *
def calculate_velocity(lon1, lat1, lon2, lat2, time_elapsed):
    """
    Calculate velocity given two coordinates (lon1, lat1) and (lon2, lat2)
    and the time elapsed between them.
    """
    distance = Harvesine(lon1, lat1, lon2, lat2)  # Distance between coordinates
    distance = distance.harvesine_distance()
    
    velocity = distance / time_elapsed  # Velocity in kilometers per unit of time
    return velocity