from Harvesine import  Harvesine


def calculate1Q(quadrant_list ,Lon_Ref, Lat_Ref):
    ref_listi = []
    ref_listj = []

    Index_I = 0
    Index_J = 0

    for lon, lat in quadrant_list: 
        harversine = Harvesine(Lon_Ref,Lat_Ref,lon,lat)
        
        angle = harversine.harvesine_angle()
        distance = harversine.harvesine_distance()
        if angle == 0: 
            ref_listj.append((Index_J, lon, lat))
            Index_J += 1

        if angle == 0 and distance < 10:
            ref_listi.append((Index_I,lon,lat))
            Index_I += 1

        if angle == 90: 
            ref_listi.append((Index_I,lon,lat))          
            Index_I += 1
   
    gridi = create_1Q_I(quadrant_list,ref_listi)
    gridj = create_1Q_J(quadrant_list,ref_listj)
    grid = create_grid_ij(gridi,gridj)

    if len(grid) != len(quadrant_list):
        isnewvertex,new_ref_list_i = find_new_vertex_I(quadrant_list,ref_listi,ref_listj,Index_I)
        isnewvertexj, new_ref_list_j = find_new_vertex_J(quadrant_list, ref_listi, ref_listj,Index_I)

        if isnewvertex and isnewvertexj:
            new_gridi = create_1Q_I(quadrant_list, new_ref_list_i)
            new_gridj = create_1Q_J(quadrant_list,Index_I)
            gridfinal = create_grid_ij(new_gridi,new_gridj)
            return gridfinal, Index_I, Index_J,new_ref_list_i,new_ref_list_j
        
        elif isnewvertex and not isnewvertexj:
            new_gridi = create_1Q_I(quadrant_list, new_ref_list_i)
            gridfinal = create_grid_ij(new_gridi,gridj)
            return gridfinal, Index_I, Index_J, new_ref_list_i , ref_listj
        
        elif isnewvertexj and not isnewvertex:
            new_gridj = create_1Q_J(quadrant_list,new_ref_list_j)
            gridfinal = create_grid_ij(gridi,new_gridj)
            return gridfinal, Index_I, Index_J, ref_listi , new_ref_list_j
        
        else:   
            return gridfinal, Index_I, Index_J,ref_listi, ref_listj
    
    else: return grid, Index_I, Index_J, ref_listi, ref_listj

def create_1Q_I(quadrant_list,ref_points_i):
    grid_1Q_i = []
    
    for index, lon_ref, lat_ref in ref_points_i:
        for lon,lat in quadrant_list:
            harvesine = Harvesine(lon_ref,lat_ref,lon,lat)
            angle = harvesine.harvesine_angle()
            if angle == 0:
                if (index, lon, lat) not in grid_1Q_i:
                    grid_1Q_i.append((index,lon,lat)) 
  
    return grid_1Q_i

def create_1Q_J(quadrant_list,ref_points_j):
    grid_1Q_j = []

    for index, lon_ref, lat_ref in ref_points_j:
        for lon, lat in quadrant_list:
            harvesine = Harvesine(lon_ref, lat_ref, lon, lat)
            angle = harvesine.harvesine_angle()
            distance = harvesine.harvesine_distance()
            if angle == 0 and distance < 10:
                grid_1Q_j.append((index,lon,lat))
            if angle == 90:
                if (index, lon, lat) not in grid_1Q_j:
                    grid_1Q_j.append((index, lon, lat))
    
    return grid_1Q_j   

def create_grid_ij(grid_1Q_i,grid_1Q_j):

    grid_ij = []

    for index, lon,lat in grid_1Q_i:
        for index1, lon1, lat1 in grid_1Q_j:
            if lon == lon1 and lat == lat1:
                if not any(entry[1:] == (lon, lat) for entry in grid_ij):
                    grid_ij.append((index, index1, lon, lat))

#    gridNotCreated = False
    return grid_ij 

def find_new_vertex_I(quadrant_list,ref_points_i, ref_points_j,Index_I):

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
            if angle == 180:          
                points_in_angle.remove((lonref,latref))

    for lon, lat in points_in_angle:
        if not any((lonref, latref) == (lon, lat) for (_,lonref, latref) in ref_points_i):
            ref_points_i.append((Index_I, lon, lat))
            Index_I += 1
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
            if angle == -90:          
                points_in_angle.remove((lonref,latref))

    for lon, lat in points_in_angle:
        if not any((lonref, latref) == (lon, lat) for (_,lonref, latref) in ref_points_j):
            ref_points_j.append((Index_J, lon, lat))
            Index_J += 1
            find_new_vertex = True
            
    return find_new_vertex, ref_points_j