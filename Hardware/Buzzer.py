from gpiozero import Buzzer
import time
class BuzzerHandler:
    def __init__(self, buzzer_pin):
        self.buzzer = Buzzer(buzzer_pin)

    def playBuzzer(self):
        self.buzzer.on()
        time.sleep(1)
        self.buzzer.off()