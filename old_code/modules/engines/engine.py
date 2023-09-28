import time
from modules.config.config import Config
import wiringpi
import multiprocessing
from ..sensors.sensors import EndSwitch


class Door:
    def __init__(self):
        self.config = Config().conf
        self.setUpGpios()
        self.emergencystop_process = multiprocessing.Process(target=self.emergencystop)
        self.switch = EndSwitch()

    def setUpGpios(self):
        OUTPUT = 1
        wiringpi.wiringPiSetupGpio()
        wiringpi.pinMode(int(self.config['ENGINES']['doorpin_1']), OUTPUT)
        wiringpi.pinMode(int(self.config['ENGINES']['doorpin_2']), OUTPUT)

    def open(self):
        self.stop()
        wiringpi.digitalWrite(int(self.config['ENGINES']['doorpin_1']), 1)
        wiringpi.digitalWrite(int(self.config['ENGINES']['doorpin_2']), 0)
        self.start_emergencystop()

    def close(self):
        self.stop()
        wiringpi.digitalWrite(int(self.config['ENGINES']['doorpin_1']), 0)
        wiringpi.digitalWrite(int(self.config['ENGINES']['doorpin_2']), 1)
        self.start_emergencystop()

    def stop(self):
        wiringpi.digitalWrite(int(self.config['ENGINES']['doorpin_1']), 0)
        wiringpi.digitalWrite(int(self.config['ENGINES']['doorpin_2']), 0)

    def engineRunning(self):
        if wiringpi.digitalRead(int(self.config['ENGINES']['doorpin_1'])) == 1 or wiringpi.digitalRead(
                int(self.config['ENGINES']['doorpin_2'])) == 1:
            return True  # engine is moving
        else:
            return False  # engine stopped

    def close_step(self):
        self.stop()
        wiringpi.digitalWrite(int(self.config['ENGINES']['doorpin_1']), 0)
        wiringpi.digitalWrite(int(self.config['ENGINES']['doorpin_2']), 1)
        time.sleep(0.1)
        self.stop()
        time.sleep(0.1)

    def close_step_big(self):
        self.stop()
        wiringpi.digitalWrite(int(self.config['ENGINES']['doorpin_1']), 0)
        wiringpi.digitalWrite(int(self.config['ENGINES']['doorpin_2']), 1)
        time.sleep(2.3)
        self.stop()

    def open_step(self):
        self.stop()
        wiringpi.digitalWrite(int(self.config['ENGINES']['doorpin_1']), 1)
        wiringpi.digitalWrite(int(self.config['ENGINES']['doorpin_2']), 0)
        time.sleep(0.1)
        self.stop()
        time.sleep(0.1)

    def open_step_big(self):
        self.stop()
        wiringpi.digitalWrite(int(self.config['ENGINES']['doorpin_1']), 1)
        wiringpi.digitalWrite(int(self.config['ENGINES']['doorpin_2']), 0)
        time.sleep(2.3)
        self.stop()

    def start_emergencystop(self):
        if self.emergencystop_process.is_alive():
            self.emergencystop_process.terminate()
        self.emergency_process = multiprocessing.Process(target=self.emergencystop)
        self.emergency_process.start()

    def emergencystop(self):
        start = time.time()
        while self.readStatus() != 0:
            if time.time() - start >= int(self.config['ENGINES']['door_max_runtime']):
                self.stop()

    def find_position(self):
        intervall = 1
        breaker = None
        i = 0
        while self.switch.readHigh() == self.switch.readLow() and i < 20 and breaker != True:
            if not breaker:
                for i in range(intervall + 1):
                    self.close_step()
                    if not self.switch.readHigh() == self.switch.readLow():
                        breaker = True
                        break
                    time.sleep(0.1)
            if not breaker:
                for i in range(intervall):
                    self.open_step()
                    if not self.switch.readHigh() == self.switch.readLow():
                        breaker = True
                        break
                    time.sleep(0.1)
                intervall += 1
        if self.switch.readHigh() == self.switch.readLow():
            return False
        else:
            return True
    def ready(self):
        if self.switch.readHigh() == self.switch.readLow():
            return False
        else:
            return True


class Feeder:
    def __init__(self):
        self.config = Config().conf
        self.setUpGpios()
        self.emergencystop_process = multiprocessing.Process(target=self.emergencystop)

    def setUpGpios(self):
        OUTPUT = 1
        wiringpi.wiringPiSetupGpio()
        wiringpi.pinMode(int(self.config['ENGINES']['feeder']), OUTPUT)

    def run(self):
        wiringpi.digitalWrite(int(self.config['ENGINES']['feeder']), 1)
        self.start_emergencystop()

    def stop(self):
        wiringpi.digitalWrite(int(self.config['ENGINES']['feeder']), 0)

    def start_emergencystop(self):
        if self.emergencystop_process.is_alive():
            self.emergencystop_process.terminate()
        self.emergency_process = multiprocessing.Process(target=self.emergencystop)
        self.emergency_process.start()

    def emergencystop(self):
        start = time.time()
        while self.readStatus() != 0:
            if time.time() - start >= int(self.config['ENGINES']['feeder_mx_runtime']):
                self.stop()

    def readStatus(self):
        if wiringpi.digitalRead(int(self.config['ENGINES']['feeder'])):
            return 1  # engine is moving
        else:
            return 0  # engine stopped
