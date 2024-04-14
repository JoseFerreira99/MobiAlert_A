from grove_gps import GPS


class GPSHandler:
    def __init__(self):
        self.GPS = GPS() 
       
    def getLatitude(self): 
        GPSlatitude = "{:.6f}".format(self.GPS.getLatitude())
        
        return GPSlatitude

    def getLongitude(self): 
        GPSlongitude = "{:.6f}".format(self.GPS.getLongitude())       
        return GPSlongitude
    
    def getVelocity(self):
        vel = self.GPS.getSpeed()
        vel =  vel* 0.27778
        return vel
        
        
   