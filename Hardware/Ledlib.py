from time import sleep 
from gpiozero import OutputDevice  

class MY9221:
    def __init__(self, di, dcki):
        self._d = OutputDevice(di)
        self._c = OutputDevice(dcki)

    def _latch(self):
        self._d.off()
        sleep(0.001)
        for _ in range(4):  # Loop without using the index
            self._d.on()
            self._d.off()
        sleep(0.001)

    def _write16(self, data):
        for i in range(15, -1, -1):
            self._d.value = (data >> i) & 1
            state = self._c.value
            self._c.value = not state

    def _begin(self):
        self._write16(0)  # command: 8bit mode

    def _end(self):
        self._write16(0)  # unused last 2 channels
        self._write16(0)  # are required to fill the 208 bit shift register
        self._latch()
           
    #led_pattern = 0b0000000001 << i   #BOT TO TOP   
    def writeLedBar(self, val, brightness=255):
        val &= 0x3FF  # Perform bitwise AND operation to ensure 10-bit value
        self._begin() 
        for i in range(9, -1, -1):
            self._write16(brightness if (val >> i) & 1 else 0)
        self._end()


   # brightness_levels = [255, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                         #BOT                            TOP
    def writeBufferToBar(self, buf):
        self._begin()
        for i in range(9, -1, -1):
            self._write16(buf[i])
        self._end()


class LedBar_Write:
    def __init__(self, led_bar):    
        self.ledWriter = led_bar
                   

         
    def allLedON(self):
        brightness = 255
        led_pattern = 0b1111111111
        self.ledWriter.writeLedBar(led_pattern, brightness)
  
    def allLedOFF(self):              
        brightness = 0
        led_pattern = 0b1111111111   #TOP  BOT
        self.ledWriter.writeLedBar(led_pattern, brightness)  
    
    
    def turn_sequential_LEDS(self): 
        for i in range(10):  # TOP 0000000000  BOT
            brightness = 255 
            led_pattern = 0b0000000001 << i   #TOP  BOT
            self.ledWriter.writeLedBar(led_pattern, brightness)
            sleep(0.1)
            
            
    def writeRisk(self, risk):
        risk = int(risk)
        patterns = {
            1: 0b0010000000,
            2: 0b0100000000,
            3: 0b1000000000
        }

        led_pattern = patterns.get(risk)
        if led_pattern is not None:
            self.ledWriter.writeLedBar(led_pattern, 255)
            
    def gps_not_working_risk(self, risk):   
        brightness = 255 
        patterns = {
            1: 0b0010000000,
            2: 0b0100000000,
            3: 0b1000000000
        }  
        
        led_pattern = 0b0000111111  #TOP  BOT
         
        risk = int(risk)        
        led_pattern_risk = patterns.get(risk)
            
        combined_pattern = led_pattern | led_pattern_risk
                    
        self.ledWriter.writeLedBar(combined_pattern, brightness)
            
            
    def gps_not_working(self):   
        brightness = 255 
        led_pattern = 0b0000111111  #TOP  BOT
        self.ledWriter.writeLedBar(led_pattern, brightness)