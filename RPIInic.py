import time

from grove_gps.grove_gps import GPS
#from Hardware.GPS import GPSHandler #GPSHandler

from Hardware.Ledlib import *   #LEDHandler
from Hardware.Buzzer import *

from calculateClosestCenter import getCenter, calculateMaxDistance
from functions import get_current_city, getFinalGrid_notorganized
from FileHandler import write_log_file, write_log_file_session
from test import create_list
from Grid.calculateGrid import create_grid_search, search_grid, get_grid_to_search

#filepath = '/home/jose/Documentos/GitHub/MobiAlert/MobiAlert/Cities'
#filepath_grid = '/home/jose/Documentos/GitHub/MobiAlert/MobiAlert/Cities_grids'
#filepath_sessions = '/home/jose/Documentos/GitHub/MobiAlert/MobiAlert/Sessions'
filepath = '/home/admin/MobiAlert/Cities'
filepath_grid = '/home/admin/MobiAlert/Cities_grids'
filepath_sessions = '/home/admin/MobiAlert/Sessions'

Index_I = 0
Index_J = 0

#from plotfunc import plot_items

#DI_PIN = 16
#DCKI_PIN = 17
led_bar = MY9221(16, 17)
write_led_bar = LedBar_Write(led_bar)       

#buzzer_PIN = 5
buzzer = BuzzerHandler(5)

polygon_side = 50
maxdistance = calculateMaxDistance(polygon_side)

gps = GPS()

# Specify the port path to check
port_path = '/dev/ttyAMA0'  #
def main():
    global filepath,maxdistance ,Index_I, Index_J

    current_city = None
    is_rpi_first_inic = True
    gps_flag = False
    
    if is_rpi_first_inic == True:
        print('MobiAlert Started')
        write_led_bar.allLedON()
                            
        Px = gps.getLongitude() #Lon   
        Py = gps.getLatitude() #Lat
            
        Px = float(Px)
        Py = float(Py)
            
            # Px = -8.65440450081201
            # Py = 41.138737447421335
            
        is_serial_exception = False    
        if Px == -1.0 or Py == -1.0 or Px == 0 or Py == 0:  
            write_led_bar.allLedOFF()
            write_led_bar.gps_not_working()  
            
            if Px == -1.0 and Py == -1.0 and is_serial_exception == False:
                print('is Serial Excpetion')
                is_serial_exception = True
                while is_serial_exception:
                    #buzzer.playBuzzer()
                    print('GPS Refresh')
                    gps.refresh()
                    
                    Px = gps.getLongitude() #Lon   
                    Py = gps.getLatitude() #Lat

                    if Px != -1 and Py != -1:
                        print('Left serial exception')
                        write_led_bar.allLedOFF()
                        is_serial_exception = False
                        break
                    else: 
                        write_led_bar.gps_not_working()
  

                        
                Px = round(float(Px), 6)
                Py = round(float(Py), 6)  
                                         
        if Px != -1.00000 and Py != -1.00000 or Px != 0 and Py != 0:    
            print('Starting grid creation')              
            start_time1 = time.time()
            current_city = get_current_city(filepath,Px,Py, maxdistance)   #Do diretório "Cities" verifico qual a cidade em qual o ciclista se encontra
            write_log_file_session(filepath_sessions,current_city)
            
            print('Current City:', current_city)
                #end_time1 = time.time()
                #print('Time to find the City where user is', end_time1-start_time1)
                #start_time2 = time.time()
                
            final_grid = getFinalGrid_notorganized(current_city, filepath, filepath_grid) #Escrevo a final grid no diretório "Cities_grid" com o nome igual ao do ficheiro Cities e dou fetch na mesma
            print('Grid Created')
                #end_time2 = time.time()
                #print('Time to gett final grid 1', end_time2-start_time2)               
                
                #start_time3 = time.time()
            closest_center = getCenter(Px,Py, final_grid, maxdistance) #Numa primeira iteração da RPI verifico qual o ponto mais proximo, (lon, lat, risk)
            print('Fetched Zone')  
                #end_time3 = time.time()
                #print('Time to get first closestCenter', end_time3-start_time3)                     
                
                #start_time4 = time.time()
            write_log_file(filepath_sessions,current_city,closest_center,Px,Py)  #Escrevo no ficheiro log unix, cidade (nome do ficheiro), centro(lon,lat,risk), ponto apanhado pelo gps (lon,lat)
            print('Log file written')  
                #end_time4 = time.time()
                #print('Time to write log file', end_time4-start_time4)
                
            Index_I = closest_center[0]  #Index up or down
            Index_J = closest_center[1]  #Index right or left

            indexes_to_search = create_grid_search(Index_I ,Index_J) #Verifico a existência da grid, se não existir crio uma nova
            print('Fetched idxs to search')
                #start_time5 = time.time()           
            grid = get_grid_to_search(current_city,filepath_grid)
            print('Fetched Grid')
                #end_time5 = time.time()
                #print('Time to get final grid', end_time5-start_time5)   
                
                #start_time6 = time.time()  
            idxs, coord = search_grid(Px, Py, indexes_to_search, grid, maxdistance) #Procuro na grid com base o Index_I, Index_J, +3,-3, retorna index e coordenada             
            #print('Fetched idxs ') 
            Index_I = idxs[0] 
            Index_J = idxs[1]
                
            risk = coord[2]
            prev_risk = risk
            write_led_bar.writeRisk(risk)
            #print('Updated Hardware')
            is_rpi_first_inic = False
                
            #end_time1 = time.time()
            #print('End of first inic, when rpi turns on', end_time1-start_time1)       
                
            interval = 1
            
            is_serial_exception = False     
            
        while True:
            if not is_rpi_first_inic:
                print('Start Safe Loop')
                total_time = time.time()
            
                gps.refresh()
                Px = gps.getLongitude() #Lon   
                Py = gps.getLatitude() #Lat
                
                if Px == -1.0 and Py == -1.0 and is_serial_exception == False:
                    is_serial_exception = True
                    write_led_bar.gps_not_working_risk(risk)
                    while is_serial_exception:
                        #print('serial exception 2')
                        #buzzer.playBuzzer()
                        gps.refresh()
                        Px = gps.getLongitude() #Lon   
                        Py = gps.getLatitude() #Lat
                        if Px != -1.0 and Py != -1.0:
                            is_serial_exception = False
                            write_led_bar.allLedOFF()
                            break     
                                       
                Py = float(Py)
                Px = float(Px) 
                Px = round(float(Px), 6)
                Py = round(float(Py), 6)


                indexes_to_search = create_grid_search(Index_I ,Index_J)
        
                #start_time7 = time.time() ########
                idxs, coord = search_grid(Px,Py, indexes_to_search, grid, maxdistance)
                #end_time7 = time.time() ######  
                #print('Time to read final grid', end_time7-start_time7) #####

                Index_I = idxs[0]
                Index_J = idxs[1]     
                #start_time8 = time.time() ########
        
                risk = coord[2]
                write_led_bar.writeRisk(risk)
                
                if risk != prev_risk:
                    buzzer.playBuzzer()

                
                #end_time8 = time.time() #######
                #print('Time to update ledbar', end_time8-start_time8) ######
                    
                #start_time9 = time.time()#####
                write_log_file(filepath_sessions,current_city,coord,Px,Py)
                #end_time9 = time.time() #######
                #print('Time to write logFile', end_time9-start_time9) #####

                #print('Loop Time', time.time()-total_time)
                
                elapsed_total_time = time.time() - total_time
            
                if elapsed_total_time < interval:
                    time.sleep(interval-elapsed_total_time)    
                    
if __name__ == "__main__": 
    main()
    
"""
from plotfunc import plot_items

session = 0

def main(): 



        centerCSV_List = read_csv(os.path.join(filepath,current_city))
        plot_items(centerCSV_List,final_grid,Px,Py,idxs, coord)
     """
