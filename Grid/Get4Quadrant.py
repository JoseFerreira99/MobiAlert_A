from Harvesine import  Harvesine
from functions import *


def calculate_ref_lists_4Q(quadrant_list, Lon_Ref , Lat_Ref, Index_I):
    index_i = Index_I 
    Index_J = 0

    max_index = Index_I +1

    indx = 0

    ref_points_j = []  
    ref_points_i = []  

    
    for lon,lat in quadrant_list: #CRIO A REF_POINTS_I PARA ADICIONAR INDEX DAS LINHAS
        harvesine = Harvesine(Lon_Ref,Lat_Ref,lon,lat)
        angle = harvesine.harvesine_angle()     
        if angle == -90:
            indx += 1
            ref_points_i.append((indx, lon, lat))  

    ref_points_i = ref_points_i[::-1]

    for i in range(len(ref_points_i)):
        index, lon ,lat = ref_points_i[i]
        index_i +=1
        ref_points_i[i] = (index_i,lon,lat)
    
    for index, lon_ref, lat_ref in ref_points_i: #CRIO A REF_POINTS_J PARA ADICIONAR INDEX DAS COLUNAS
        for lon,lat in quadrant_list:
            harvesine = Harvesine(lon_ref,lat_ref,lon,lat)
            angle = harvesine.harvesine_angle()
            if index == max_index:
                if angle == 0:
                    ref_points_j.append((Index_J, lon,lat))    
                    Index_J += 1                
    grid = []


    Index_I = index_i

    gridi = create_3Q_I(quadrant_list,ref_points_i)
    gridj = create_3Q_J(quadrant_list,ref_points_j)

    grid = create_grid_ij(gridi,gridj)


    if len(grid) != len(quadrant_list):
        isnewvertex,new_ref_list_i = find_new_vertex_I(quadrant_list,ref_points_i,ref_points_j, Index_I)
        isnewvertexj, new_ref_list_j = find_new_vertex_J(quadrant_list, ref_points_i, ref_points_j, Index_J)

        if isnewvertex and isnewvertexj:
            new_gridi = create_3Q_I(quadrant_list, new_ref_list_i)
            new_gridj = create_3Q_J(quadrant_list,new_ref_list_j)
            gridfinal = create_grid_ij(new_gridi,new_gridj)
            return gridfinal, new_ref_list_i
        
        elif isnewvertex and not isnewvertexj:
            new_gridi = create_3Q_I(quadrant_list, new_ref_list_i)
            gridfinal = create_grid_ij(new_gridi,gridj)
            return gridfinal, new_ref_list_i
      
        elif isnewvertexj and not isnewvertex:
            new_gridj = create_3Q_J(quadrant_list,new_ref_list_j)
            gridfinal = create_grid_ij(gridi,new_gridj)
            return gridfinal, ref_points_i
        
        else: return grid, ref_points_i

    else: return grid, ref_points_i

def create_3Q_I(quadrant_list,ref_points_i):
    grid_3Q_i = []
    
    for index, lon_ref, lat_ref in ref_points_i:
        for lon,lat in quadrant_list:
            harvesine = Harvesine(lon_ref,lat_ref,lon,lat)
            angle = harvesine.harvesine_angle()
            distance = harvesine.harvesine_distance()      
            if angle == 0:
                if (index, lon, lat) not in grid_3Q_i:
                    grid_3Q_i.append((index,lon,lat)) 
  
    return grid_3Q_i

def create_3Q_J(quadrant_list,ref_points_j):
    grid_3Q_j = []

    for index, lon_ref, lat_ref in ref_points_j:
        for lon, lat in quadrant_list:
            harvesine = Harvesine(lon_ref, lat_ref, lon, lat)
            angle = harvesine.harvesine_angle()
            distance = harvesine.harvesine_distance()
            if angle == 0 and distance < 10:
                grid_3Q_j.append((index,lon,lat))
            if angle == -90:
                if (index, lon, lat) not in grid_3Q_j:
                    grid_3Q_j.append((index, lon, lat))
    
    return grid_3Q_j   

def create_grid_ij(grid_1Q_i,grid_1Q_j):

    grid_ij = []

    for index, lon,lat in grid_1Q_i:
        for index1, lon1, lat1 in grid_1Q_j:
            if lon == lon1 and lat == lat1:
                if not any(entry[1:] == (lon, lat) for entry in grid_ij):
                    grid_ij.append((index, index1, lon, lat))

#    gridNotCreated = False
    return grid_ij 

def find_new_vertex_I(quadrant_list,ref_points_i, ref_points_j, Index_I):
   #FIND NEW MAX DISTANCE
    index = []
    points_in_angle = []
    points = []
    index_i = Index_I 
    find_new_vertex = False

    for _, lon_ref, lat_ref in ref_points_j: 
        for lon, lat in quadrant_list: #TEM DE PERTENCER AO 1Q
        #Pego em todos os pontos de ref para achar distancia maxima ao topo do nvertex
            harvesine = Harvesine(lon_ref, lat_ref, lon, lat)
            angle = harvesine.harvesine_angle()    
            if angle  == -90: #SE angulo for -90, encontra-se abaixo do ponto de ref.
                points_in_angle.append((lon,lat))
            
    for lon,lat in quadrant_list:
        for  lonref,latref in points_in_angle:
            harvesine = Harvesine(lonref, latref, lon, lat)
            angle = harvesine.harvesine_angle()
            if angle == 180:          
                points_in_angle.remove((lonref,latref))

    for lon, lat in points_in_angle:
        if not any((lonref, latref) == (lon, lat) for (_,lonref, latref) in ref_points_i):
            index_i += 1
            ref_points_i.append((index_i, lon, lat))
            find_new_vertex = True

    return find_new_vertex, ref_points_i   

def find_new_vertex_J(quadrant_list, ref_points_i, ref_points_j, Index_J):
    points_in_angle = []
    find_new_vertex = False
    
    for _, lon_ref, lat_ref in ref_points_i: 
        for lon, lat in quadrant_list: #TEM DE PERTENCER AO 1Q
        #Pego em todos os pontos de ref para achar distancia maxima ao topo do nvertex
            harvesine = Harvesine(lon_ref, lat_ref, lon, lat)
            angle = harvesine.harvesine_angle()    
            if angle  == 0: #SE angulo for -90, encontra-se abaixo do ponto de ref.
                points_in_angle.append((lon,lat))
            
    for lon,lat in quadrant_list:
        for  lonref,latref in points_in_angle:
            harvesine = Harvesine(lonref, latref, lon, lat)
            angle = harvesine.harvesine_angle()
            if angle == 90:          
                points_in_angle.remove((lonref,latref))

    for lon, lat in points_in_angle:
        if not any((lonref, latref) == (lon, lat) for (_,lonref, latref) in ref_points_j):
            Index_J += 1
            ref_points_j.append((Index_J, lon, lat))
            find_new_vertex = True
            
    return find_new_vertex, ref_points_j