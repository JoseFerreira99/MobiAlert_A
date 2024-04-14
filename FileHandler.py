import csv 
import os
import datetime
import time



def fetch_files_in_folder(filepath):
    if os.path.exists(filepath) and os.path.isdir(filepath):
        files = [file for file in os.listdir(filepath) if os.path.isfile(os.path.join(filepath, file))]
  
        return files
    else:
        return []
    
def get_city_grid(filepath,filename):
    grids = fetch_files_in_folder(filepath)
    if len(grids) != 0:
        for city in grids:
            if city == filename:
                return city
            else:
                return None


def write_log_file_session(filepath, current_city):
    filename = os.path.join(filepath, os.path.join(filepath, current_city))
    current_time = datetime.datetime.now()
    with open(filename, 'a') as file:   #Open file
        file.write('session:')
        file.write(f"{current_time},{current_city}\n")
        
        
def write_log_file(filepath,current_city, center_info,Px,Py):
    filename =  os.path.join(filepath, os.path.join(filepath,current_city))

    current_time = datetime.datetime.now()
    current_time_UNIX = int(time.mktime(current_time.timetuple()) * 1000) #Convert timestamp to UNIX 
        
    with open(filename, 'a') as file:   #Open file
        file.write(f"{current_time_UNIX},{center_info},{Px},{Py}\n") #Write TIMESTAMP, LONGITUDE, LATITUDE, CENTER, RISKZONE
        file.flush()



def writeQuadrants(coordinates_list, filepath):
    if len(coordinates_list) !=0:
        with open(filepath, 'a') as file:
            for i, j, lon, lat in coordinates_list:
                file.write(f"{i},{j},{lon},{lat}\n")
                file.flush()

def writeFinalGrid(coordinates_list, filepath):
    if len(coordinates_list) !=0:
        with open(filepath, 'w') as file:
            for i, j, lon, lat ,risk in coordinates_list:
                file.write(f"{i},{j},{lon},{lat},{risk}\n")
                file.flush()



def read_log_file(filepath,current_city):

    filename =  os.path.join(filepath, os.path.join(filepath,current_city))
    csvList = []
    with open(filename,'r',newline='') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            i = row[0]
            j = row [1]
            lon = row[2] # Fetch Longitude 
            lat = row[3]
            risk = row[4]
            csvList.append((i,j,lon,lat,risk))
    return csvList


def read_final_grid_csv(filepath):
    csvList = []    
    with open(filepath, 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            i = row[0]
            j = row [1]
            lon = row[2] # Fetch Longitude 
            lat = row[3]
            risk = row[4]
            csvList.append((i,j,lon,lat,risk))
    return csvList


def read_grid_csv(filepath):
    csvList = []    
    with open(filepath, 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            i = row[0]
            j = row [1]
            lon = row[2] 
            lat = row[3]
            csvList.append((i,j,lon,lat))
    return csvList


def read_finalgrid_indexes(file_path):
    data = {}
    
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for row in reader:
            indexi, indexj, lon, lat, risk = map(float, row)
            data[(int(indexi), int(indexj))] = (lon, lat, risk)
    return data


def read_csv(filepath): 
    #Leitura ficheiro CSV, Retorna o centro e a  riskzone em listas diferentes
   
    csvList = [] #Center Coordinates and RISK List        
    with open(filepath, 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            lon = row[0] # Fetch Longitude 
            lat = row[1]
            risk = row[2]                            
            csvList.append((lon, lat, risk))   
    
    return csvList