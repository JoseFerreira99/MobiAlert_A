from Harvesine import  Harvesine

def calculate_ref_lists_2Q(quadrant_list, Lon_Ref , Lat_Ref, Index_J, ref_points_i): 
    points = []
    ref_points_j = []  
    indx = 0
    Index_I = 0
    for lon, lat in quadrant_list: #CRIO A REF_POINTS_J PARA ADICIONAR INDEX DAS COLUNAS
        harvesine = Harvesine(Lon_Ref,Lat_Ref,lon,lat)
        angle = harvesine.harvesine_angle()
        if angle == 180:
            indx += 1   
            points.append((indx, lon,lat)) 


    points = points[::-1]
    for _,lon,lat in points:
        ref_points_j.append((Index_J,lon,lat)) 
        Index_J +=1   

    for index,_,_ in ref_points_i:
        index_I = index
        if index > index_I:
            Index_I = index
            
    gridi = create_2Q_I(quadrant_list,ref_points_i)
    gridj = create_2Q_J(quadrant_list,ref_points_j)

    grid = create_grid_ij(gridi,gridj)

    if len(grid) != len(quadrant_list):
        isnewvertex,new_ref_list_i = find_new_vertex_I(quadrant_list,ref_points_i,ref_points_j, Index_I)
        isnewvertexj, new_ref_list_j = find_new_vertex_J(quadrant_list, ref_points_i, ref_points_j, Index_J)
    
        if isnewvertex and isnewvertexj:
                new_gridi = create_2Q_I(quadrant_list, new_ref_list_i)
                new_gridj = create_2Q_J(quadrant_list,new_ref_list_j)
                gridfinal = create_grid_ij(new_gridi,new_gridj)
                return gridfinal, Index_J, new_ref_list_j
        
        elif isnewvertex and not isnewvertexj:
            new_gridi = create_2Q_I(quadrant_list, new_ref_list_i)
            gridfinal = create_grid_ij(new_gridi,gridj)
            return gridfinal, Index_J,ref_points_j
        
        elif isnewvertexj and not isnewvertex:    
            new_gridj = create_2Q_J(quadrant_list,new_ref_list_j)
            gridfinal = create_grid_ij(gridi,new_gridj)
            return gridfinal, Index_J,new_ref_list_j
        
        else: return grid,ref_points_j, Index_J
    return grid

def create_2Q_I(quadrant_list,ref_points_i):
    grid_2Q_i = []
    
    for index, lon_ref, lat_ref in ref_points_i:
        for lon,lat in quadrant_list:
            harvesine = Harvesine(lon_ref,lat_ref,lon,lat)
            angle = harvesine.harvesine_angle()   
            if angle == 180:
                if (index, lon, lat) not in grid_2Q_i:
                    grid_2Q_i.append((index,lon,lat)) 

    return grid_2Q_i

def create_2Q_J(quadrant_list,ref_points_j):
    grid_2Q_j = []

    for index, lon_ref, lat_ref in ref_points_j:
        for lon, lat in quadrant_list:
            harvesine = Harvesine(lon_ref, lat_ref, lon, lat)
            angle = harvesine.harvesine_angle()
            distance = harvesine.harvesine_distance()
            if angle == 0 and distance < 10:
                grid_2Q_j.append((index,lon,lat))
            if angle == 90:
                if (index, lon, lat) not in grid_2Q_j:
                    grid_2Q_j.append((index, lon, lat))


    return grid_2Q_j   

def create_grid_ij(grid_2Q_i,grid_2Q_j):

    grid_ij = []

    for index, lon,lat in grid_2Q_i:
        for index1, lon1, lat1 in grid_2Q_j:
            if lon == lon1 and lat == lat1:
                if not any(entry[1:] == (lon, lat) for entry in grid_ij):
                    grid_ij.append((index, index1, lon, lat))

#    gridNotCreated = False
   
    return grid_ij 

def find_new_vertex_I(quadrant_list,ref_points_i, ref_points_j, Index_I):
   #FIND NEW MAX DISTANCE
    points_in_angle = []
 
    find_new_vertex = False

    for _, lon_ref, lat_ref in ref_points_j: 
        for lon, lat in quadrant_list: #TEM DE PERTENCER AO 1Q
        #Pego em todos os pontos de ref para achar distancia maxima ao topo do nvertex
            harvesine = Harvesine(lon_ref, lat_ref, lon, lat)
            angle = harvesine.harvesine_angle()    
            if angle  == 90: #SE angulo for -90, encontra-se abaixo do ponto de ref.
                points_in_angle.append((lon,lat))
        
            
    
    for lon,lat in quadrant_list:
        for  lonref,latref in points_in_angle:
            harvesine = Harvesine(lonref, latref, lon, lat)
            angle = harvesine.harvesine_angle()
            if angle == 0:          
                points_in_angle.remove((lonref,latref))
        


    for lon, lat in points_in_angle:
        if not any((lonref, latref) == (lon, lat) for (_,lonref, latref) in ref_points_i):
            Index_I += 1
            ref_points_i.append((Index_I, lon, lat))
            find_new_vertex = True

    return find_new_vertex, ref_points_i   


def find_new_vertex_J(quadrant_list, ref_points_i, ref_points_j, Index_J):

    points_in_angle = []
    indexes_points_in_angle= []
    distances = []
    distance_index = []

    find_new_vertex = False
    indx = 0

    lonRef = ref_points_i[0][1]
    latRef = ref_points_i[0][2]
  
    for _, lon_ref, lat_ref in ref_points_i: 
        for lon, lat in quadrant_list: #TEM DE PERTENCER AO 1Q
        #Pego em todos os pontos de ref para achar distancia maxima ao topo do nvertex
            harvesine = Harvesine(lon_ref, lat_ref, lon, lat)
            angle = harvesine.harvesine_angle()
            distance = harvesine.harvesine_distance()    
            if angle  == 180: #SE angulo for -90, encontra-se abaixo do ponto de ref.
                points_in_angle.append((indx,lon,lat))
                indx+=1


    for lon,lat in quadrant_list:
        for  idx, lonref,latref in points_in_angle:
            harvesine = Harvesine(lonref, latref, lon, lat)
            angle = harvesine.harvesine_angle()
            if angle == -90:   
                points_in_angle.remove((idx,lonref,latref))
    

    points_in_angle = sorted(points_in_angle)
    indx = 0

    for idx, lon, lat in points_in_angle:
        indexes_points_in_angle.append((indx,lon,lat))
        indx+=1
    

    for idx,lon,lat in indexes_points_in_angle:
        harvesine = Harvesine(lonRef,latRef,lon,lat)
        distance = harvesine.harvesine_distance()
        distances.append((distance,idx,lon,lat))
    
    distances = sorted(distances)
    indx = 0
    for _,_,lon,lat in distances:
        distance_index.append((indx,lon,lat))
        indx+=1

    for  idx, lon, lat in distance_index:
        if not any((lonref, latref) == (lon, lat) for (_,lonref, latref) in ref_points_j):
            ref_points_j.append((idx+Index_J, lon, lat))
            
            find_new_vertex = True
    
    return find_new_vertex, ref_points_j