from Harvesine import  Harvesine

def calculate_ref_lists_3Q(quadrant_list, ref_points_i, ref_points_j): 

    gridi = create_3Q_I(quadrant_list,ref_points_i)
    gridj = create_3Q_J(quadrant_list,ref_points_j)

    grid = create_grid_ij(gridi,gridj)

    if len(grid) != len(quadrant_list):
        isnewvertex,new_ref_list_i = find_new_vertex_I(quadrant_list,ref_points_i,ref_points_j)
        isnewvertexj, new_ref_list_j = find_new_vertex_J(quadrant_list, ref_points_i, ref_points_j)
    
        if isnewvertex and isnewvertexj:
                new_gridi = create_3Q_I(quadrant_list, new_ref_list_i)
                new_gridj = create_3Q_J(quadrant_list,new_ref_list_j)
                gridfinal = create_grid_ij(new_gridi,new_gridj)
                return gridfinal
        
        elif isnewvertex and not isnewvertexj:
            new_gridi = create_3Q_I(quadrant_list, new_ref_list_i)
            gridfinal = create_grid_ij(new_gridi,gridj)
            return gridfinal
        
        elif isnewvertexj and not isnewvertex:    
            new_gridj = create_3Q_J(quadrant_list,new_ref_list_j)
            gridfinal = create_grid_ij(gridi,new_gridj)
            return gridfinal
        
        else: return grid
    return grid

def create_3Q_I(quadrant_list,ref_points_i):
    grid_3Q_i = []
    
    for index, lon_ref, lat_ref in ref_points_i:
        for lon,lat in quadrant_list:
            harvesine = Harvesine(lon_ref,lat_ref,lon,lat)
            angle = harvesine.harvesine_angle()   
            if angle == 180:
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
            if angle == -90:
                if (index, lon, lat) not in grid_3Q_j:
                    grid_3Q_j.append((index, lon, lat))


    return grid_3Q_j   

def create_grid_ij(grid_3Q_i,grid_3Q_j):

    grid_ij = []

    for index, lon,lat in grid_3Q_i:
        for index1, lon1, lat1 in grid_3Q_j:
            if lon == lon1 and lat == lat1:
                if not any(entry[1:] == (lon, lat) for entry in grid_ij):
                    grid_ij.append((index, index1, lon, lat))

#    gridNotCreated = False
   
    return grid_ij 

def find_new_vertex_I(quadrant_list,ref_points_i, ref_points_j):
    
    points_in_angle = []
    idxi = 0
    idxj = 0
    find_new_vertex = False

    for index,_,_ in ref_points_i:
        idxi = index
        if index > idxi:
            idxi = index
    

    for _, lon_ref, lat_ref in ref_points_j: 
        for lon, lat in quadrant_list: 
        #Pego em todos os pontos de ref para achar distancia maxima ao topo do nvertex
            harvesine = Harvesine(lon_ref, lat_ref, lon, lat)
            angle = harvesine.harvesine_angle()    
            if angle  == -90: #SE angulo for -90, encontra-se abaixo do ponto de ref.
                points_in_angle.append((lon,lat))
            
    for lon,lat in quadrant_list:
        for  lonref, latref in points_in_angle:
            harvesine = Harvesine(lonref, latref, lon, lat)
            angle = harvesine.harvesine_angle()
            if angle == 180:          
                points_in_angle.remove((lonref,latref))

    for lon, lat in points_in_angle:
        if not any((lonref, latref) == (lon, lat) for (_,lonref, latref) in ref_points_i):
            idxi += 1
            ref_points_i.append((idxi, lon, lat))
            find_new_vertex = True


    return find_new_vertex, ref_points_i   



def find_new_vertex_J(quadrant_list, ref_points_i, ref_points_j):
    points_in_angle = []

    find_new_vertex = False
    idxj = 0
    for index,_,_ in ref_points_j:
        idxj = index
        if index > idxj:
            idxj = index   
             
    for _, lon_ref, lat_ref in ref_points_i: 
        for lon, lat in quadrant_list: #TEM DE PERTENCER AO 1Q
        #Pego em todos os pontos de ref para achar distancia maxima ao topo do nvertex
            harvesine = Harvesine(lon_ref, lat_ref, lon, lat)
            angle = harvesine.harvesine_angle()    
            if angle  == 180: #SE angulo for -90, encontra-se abaixo do ponto de ref.
                points_in_angle.append((lon,lat))
            
    for lon,lat in quadrant_list:
        for  lonref,latref in points_in_angle:
            harvesine = Harvesine(lonref, latref, lon, lat)
            angle = harvesine.harvesine_angle()
            if angle == -90:          
                points_in_angle.remove((lonref,latref))

    for lon, lat in points_in_angle:
        if not any((lonref, latref) == (lon, lat) for (_,lonref, latref) in ref_points_j):

            ref_points_j.append((idxj, lon, lat))
            idxj += 1
            find_new_vertex = True
            
    return find_new_vertex, ref_points_j