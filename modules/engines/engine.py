import time
from modules.config.config import Config
import wiringpi
import multiprocessing
from ..sensors.sensors import EndSwitch

class Door:
    def __init__(self):
        self.config=Config().conf
        self.setUpGpios()
        self.es = EndSwitch()
        self.emergencystop_process = multiprocessing.Process(target=self.emergencystop)

    def setUpGpios(self):
        OUTPUT = 1
        wiringpi.wiringPiSetupGpio()
        wiringpi.pinMode(int(self.config['ENGINES']['doorpin_1']), OUTPUT)
        wiringpi.pinMode(int(self.config['ENGINES']['doorpin_2']), OUTPUT)

    def open(self):
        self.stop()
        if self.es.readHigh() == 0 and self.es.doorisOpen() != None:
            wiringpi.digitalWrite(int(self.config['ENGINES']['doorpin_1']),1)
            wiringpi.digitalWrite(int(self.config['ENGINES']['doorpin_2']),0)
            while self.es.readHigh() != 1:
                None
        self.stop()

    def close(self):
        self.stop()
        if self.es.readLow() == 0 and self.es.doorisOpen() != None:
            wiringpi.digitalWrite(int(self.config['ENGINES']['doorpin_1']),0)
            wiringpi.digitalWrite(int(self.config['ENGINES']['doorpin_2']),1)
        while self. es.readLow() != 1:
            None
        self.stop()


    def stop(self):
        wiringpi.digitalWrite(int(self.config['ENGINES']['doorpin_1']),0)
        wiringpi.digitalWrite(int(self.config['ENGINES']['doorpin_2']),0)

    def readStatus(self):
        if wiringpi.digitalRead(int(self.config['ENGINES']['doorpin_1'])) or wiringpi.digitalRead(int(self.config['ENGINES']['doorpin_2'])):
            return 1 #engine is moving
        else:
            return 0 #engine stopped

    def start_emergencystop(self):
        if self.emergencystop_process.is_alive():
            self.emergencystop_process.terminate()
        self.emergency_process = multiprocessing.Process(target=self.emergencystop)
        self.emergency_process.start()

    def emergencystop(self):
        start=time.time()
        while self.readStatus() != 0:
            if time.time() - start >= int(self.config['ENGINES']['door_max_runtime']):
                self.stop()

class Feeder:
    def __init__(self):
        self.config=Config().conf
        self.setUpGpios()
        self.emergencystop_process = multiprocessing.Process(target=self.emergencystop)

    def setUpGpios(self):
        OUTPUT = 1
        wiringpi.wiringPiSetupGpio()
        wiringpi.pinMode(int(self.config['ENGINES']['feeder']), OUTPUT)

    def run(self):
        wiringpi.digitalWrite(int(self.config['ENGINES']['feeder']),1)
        self.start_emergencystop()

    def stop(self):
        wiringpi.digitalWrite(int(self.config['ENGINES']['feeder']), 0)

    def start_emergencystop(self):
        if self.emergencystop_process.is_alive():
            self.emergencystop_process.terminate()
        self.emergency_process = multiprocessing.Process(target=self.emergencystop)
        self.emergency_process.start()

    def emergencystop(self):
        start=time.time()
        while self.readStatus() != 0:
            if time.time() - start >= int(self.config['ENGINES']['feeder_mx_runtime']):
                self.stop()

    def readStatus(self):
        if wiringpi.digitalRead(int(self.config['ENGINES']['feeder'])):
            return 1 #engine is moving
        else:
            return 0 #engine stopped

