import serial
import time
import os

ser = serial.Serial('/dev/ttyAMA0',  9600, timeout=0)
ser.flush()

def cleanstr(in_str):
    """Removes non-numerical characters, only keeps 0123456789.-"""
    out_str = "".join([c for c in in_str if c in "0123456789.-"])
    if len(out_str) == 0:
        out_str = "-1"
    return out_str

def safefloat(in_str):
    """Converts to float. If there is an error, a deafault
    value is returned
    """
    try:
        out_str = float(in_str)
    except ValueError:
        out_str = -1.0
    return out_str

# Convert to decimal degrees
def decimal_degrees(raw_degrees):
    """Converts coordinates to decimal values"""
    try:
        degrees = float(raw_degrees) // 100
        d = float(raw_degrees) % 100 / 60
        return degrees + d
    except: 
        return raw_degrees

class GPS:
    """"Connect to GPS and read its values"""
    
    inp = []
    inp2 = []
    GGA = []
    RMC = []
    values = []
    
    def __init__(self):
        """Instantiates an object of the class
        and runs the refresh() method
        """
        self.refresh()
    
    def refresh(self):
        """Reads data from the GPS and stores them in
        a global array of the class
        """
        while True: 
                    try:
                        line = ser.readline()
                        
                        GPS.inp = line.decode('ISO-8859-1')
                        #print(GPS.inp + "\n") # uncomment for debugging
                        
                        # GGA data for latitude, longitude, satellites,
                        # altitude, and UTC position               
                        if GPS.inp[0:6] =='$GPGGA': 
                            GPS.GGA = GPS.inp.split(",")
                            if len(GPS.GGA) >= 10:
                                #initialize values obtained from the GPS device
                
                                if GPS.GGA[2] == '':  # latitude. Technically a float
                                    lat =-1.0
                                else:
                                    lat = decimal_degrees(safefloat(cleanstr(GPS.GGA[2])))
                                
                                if GPS.GGA[3] == '':  # this should be either N or S
                                    lat_ns = ""
                                else:
                                    lat_ns=str(GPS.GGA[3])
                                if lat_ns == "S":
                                    lat = -lat
                                    
                                if  GPS.GGA[4] == '':  # longitude. Technically a float
                                    long = -1.0
                                else:
                                    long = decimal_degrees(safefloat(cleanstr(GPS.GGA[4])))
                                
                                if  GPS.GGA[5] == '': # this should be either W or E
                                    long_ew = ""
                                else:
                                    long_ew = str(GPS.GGA[5])
                                if long_ew == "W":
                                    long = -long

                                if lat == -1.0 or long == -1.0:
                                    GPS.values = [lat, lat_ns, long, long_ew]                            
                                else: 
                                    GPS.values = [lat, lat_ns, long, long_ew]
                                    
                                break
                    except serial.SerialException:
                        lat = -1.0
                        lat_ns = -1.0
                        long  = -1.0
                        long_ew = -1.0
                        print(serial.SerialException)
                        ser.close()  
                        GPS.values = [lat, lat_ns, long, long_ew]
                        ser.open()
                        break
                    
                        
            
                            


    # Accessor methods for all the desired GPS values
    def getLatitude(self):
        """Returns the latitude"""
        return GPS.values[0]
    def getLongitude(self):
        """Returns the longitude"""
        return GPS.values[2]


        
if __name__ == "__main__":
    gps = GPS()
    