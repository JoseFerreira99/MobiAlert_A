from Harvesine import Harvesine
import math
import time
def getCenter(Px,Py, grid, max_distance):
    Px = float(Px)
    Py = float(Py) 

    center_List = [] # center with lon, lat
    distance_List = []
  
    for i ,j ,lon ,lat ,risk in grid:
        harvesine = Harvesine(Px,Py, lon, lat)
        distance = harvesine.harvesine_distance()

        if distance < max_distance:
            center_List.append((i ,j ,lon ,lat ,risk)) 
            distance_List.append(distance)

    if len(center_List) > 1:   
        distance = min(distance_List) # Get the minimum distance 
        distance_index = getID(distance_List, distance) # Get the index of the minimum distance, equal to center index
        center_and_risk = getItem_byID(center_List, distance_index)
        return center_and_risk
    
    elif len(center_List) == 1:                
        closest_center_coord = center_List[0][0], center_List[0][1] # Get centro

        return closest_center_coord 
    


def getClosestCenter(Px, Py, centerCSV_List, max_distance): 
    # Retorna os centros e as respetivas distancias abaixo do valor max     
    Px = float(Px) # LON
    Py = float(Py) # LAT
           
    center_List = [] # center with lon, lat
    distance_List = []
                  
    for center in centerCSV_List:  
        # Percorro todos os centros e calculo a distancia para cada um deles
        Cx = float(center[0])  # Longitude from CSV
        Cy = float(center[1])  # Latitude from CSV
        
        harvesine = Harvesine(Cx, Cy, Px, Py)   
        distance_meters = harvesine.harvesine_distance()   # Calculo de Todaas as distancias
                 
        if distance_meters < max_distance:   # Se distancia menor que max_distance
            center_List.append(center) 
            distance_List.append(distance_meters)
             
    if len(center_List) > 1:   
        distance = min(distance_List) # Get the minimum distance        
        distance_index = getID(distance_List, distance) # Get the index of the minimum distance, equal to center index                
        center_and_risk = getItem_byID(center_List, distance_index) # Get the center and risk list corresponding to the minimum distance            
            
        closest_center_coord = center_and_risk[0], center_and_risk[1] # Get centro
        #risk = center_and_risk[2] # get risco
    
        return closest_center_coord # Return list with LON, LAT, RISK, DISTANCE    

    elif len(center_List) == 1:                
        closest_center_coord = center_List[0][0], center_List[0][1] # Get centro
        #risk = center_List[0][2] # get risco  

        return closest_center_coord # Return list with LON, LAT, RISK, DISTANCE  

    return None # Return list with LON, LAT, RISK, DISTANCE  


#Get ID from list                             
def getID(list, point):
    return list.index(point)

#Get Item from ID
def getItem_byID(list,index):
    return list.__getitem__(index)
   
#Use Pytagoras to calculate the distance    
def calculateMaxDistance(side):    
    max_side = math.sqrt(2)*side #Teorema de pitagoras para quadrado    
    return max_side