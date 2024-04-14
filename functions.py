
import os
from calculateClosestCenter import getClosestCenter
from FileHandler import fetch_files_in_folder, read_csv

from Grid.calculateGrid import calculat_quadrant_lists


from FileHandler import*

def get_current_city(filepath,Px,Py,maxdistance):
    
    cities = fetch_files_in_folder(filepath)

    if len(cities) != 0:
            for city in cities:
                centerCSV_List = read_csv(os.path.join(filepath,city))
                center = getClosestCenter(Px, Py, centerCSV_List, maxdistance)
                if  center is not None:
                    current_city = city
                    
                    return current_city
                else: return None 

def merge_risk_with_grid(centerList, grid):
    merged_list = []
    for lon,lat,risk in centerList:
        for i,j,lon1,lat1 in grid:
            if lon == lon1 and lat == lat1:
                merged_list.append((i,j,lon,lat,risk))
    return merged_list


def getFinalGrid_notorganized(current_city, filepath, filepath_grid):
    start_time = time.time
    if current_city is not None:      
        grids = get_city_grid(filepath_grid, current_city)   
        if grids is not None:
            if(grids == current_city): #SE grid da cidade já existir
                final_grid = read_final_grid_csv(os.path.join(filepath_grid,os.path.join(filepath_grid,current_city)))
         
                return final_grid
            elif (grids != current_city):
                centerCSV_List = read_csv(os.path.join(filepath_grid,os.path.join(filepath,current_city)))     ##
                q1,q2,q3,q4 = calculat_quadrant_lists(centerCSV_List) #q2

                writeQuadrants(q1, os.path.join(filepath_grid,current_city))
                writeQuadrants(q2, os.path.join(filepath_grid,current_city))
                writeQuadrants(q3, os.path.join(filepath_grid,current_city))
                writeQuadrants(q4, os.path.join(filepath_grid,current_city))
                    
                grid_list = read_grid_csv(os.path.join(filepath_grid, os.path.join(filepath_grid,current_city)))


                final_grid = merge_risk_with_grid(centerCSV_List, grid_list)
                writeFinalGrid(final_grid, os.path.join(filepath_grid,os.path.join(filepath_grid,current_city)))
                final_grid = read_final_grid_csv(os.path.join(filepath_grid,os.path.join(filepath_grid,current_city)))
                 
                return final_grid

        elif grids is None:
            centerCSV_List = read_csv(os.path.join(filepath_grid,os.path.join(filepath,current_city))) ##
            q1,q2,q3,q4 = calculat_quadrant_lists(centerCSV_List) #q2
   
            writeQuadrants(q1, os.path.join(filepath_grid,current_city))
            writeQuadrants(q2, os.path.join(filepath_grid,current_city))
            writeQuadrants(q3, os.path.join(filepath_grid,current_city))
            writeQuadrants(q4, os.path.join(filepath_grid,current_city))


            grid_list = read_grid_csv(os.path.join(filepath_grid,os.path.join(filepath_grid,current_city)))


            final_grid = merge_risk_with_grid(centerCSV_List, grid_list)
            writeFinalGrid(final_grid, os.path.join(filepath_grid,os.path.join(filepath_grid,current_city)))
            final_grid = read_final_grid_csv(os.path.join(filepath_grid,os.path.join(filepath_grid,current_city)))
        return final_grid
            
    else: return None
    
