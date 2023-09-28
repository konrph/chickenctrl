import wiringpi
from modules.config.config import Config


class Ventilation:
    def __init__(self):
        self.config = Config().conf
        self.setUpGpios()

    def setUpGpios(self):
        OUTPUT = 1
        wiringpi.wiringPiSetupGpio()
        wiringpi.pinMode(int(self.config['RELAYS']['ventilation']), OUTPUT)

    def start(self):
        print('bin hier')
        wiringpi.digitalWrite(int(self.config['RELAYS']['ventilation']),1)

    def stop(self):
        wiringpi.digitalWrite(int(self.config['RELAYS']['ventilation']),0)

class Light:
    def __init__(self):
        self.config = Config().conf
        self.setUpGpios()

    def setUpGpios(self):
        OUTPUT = 1
        wiringpi.wiringPiSetupGpio()
        wiringpi.pinMode(int(self.config['RELAYS']['light']), OUTPUT)

    def on(self):
        wiringpi.digitalWrite(int(self.config['RELAYS']['light']),1)

    def off(self):
        wiringpi.digitalWrite(int(self.config['RELAYS']['light']),0)

class Relay1:
    def __init__(self):
        self.config = Config().conf
        self.setUpGpios()

    def setUpGpios(self):
        OUTPUT = 1
        wiringpi.wiringPiSetupGpio()
        wiringpi.pinMode(int(self.config['RELAYS']['relay_1']), OUTPUT)

    def start(self):
        wiringpi.digitalWrite(int(self.config['RELAYS']['relay_1']),1)

    def stop(self):
        wiringpi.digitalWrite(int(self.config['RELAYS']['relay_1']),0)

class Relay2:
    def __init__(self):
        self.config = Config().conf
        self.setUpGpios()

    def setUpGpios(self):
        OUTPUT = 1
        wiringpi.wiringPiSetupGpio()
        wiringpi.pinMode(int(self.config['RELAYS']['relay_2']), OUTPUT)

    def start(self):
        wiringpi.digitalWrite(int(self.config['RELAYS']['relay_2']), 1)

    def stop(self):
        wiringpi.digitalWrite(int(self.config['RELAYS']['relay_2']), 0)