from modules.config.config import Config
import wiringpi
import smbus
import time


class Temperature:
    def __init__(self):
        self.config=Config().conf

    def readTempSensor1(self):
        return self.readSensor(self.config['SENSORS']['temp_1'])
    def readTempSensor2(self):
        return self.readSensor(self.config['SENSORS']['temp_2'])

    def readSensor(self,address):
        file = open('/sys/bus/w1/devices/'+address+'/w1_slave')
        data = file.read()
        file.close()
        data = data.split("\n")[1].split(" ")[9]
        return float(data[2:])/1000

class EndSwitch:
    def __init__(self):
        self.config=Config().conf
        self.setUpGpios()

    def setUpGpios(self):
        INPUT = 0
        wiringpi.wiringPiSetupGpio()
        wiringpi.pinMode(int(self.config['SENSORS']['endSwitch_HIGH']), INPUT)
        wiringpi.pinMode(int(self.config['SENSORS']['endSwitch_LOW']), INPUT)

    def readHigh(self):
        return wiringpi.digitalRead(int(self.config['SENSORS']['endSwitch_HIGH']))

    def readLow(self):
        return wiringpi.digitalRead(int(self.config['SENSORS']['endSwitch_LOW']))

    def doorisOpen(self):
        low = int(self.readLow())
        high = int(self.readHigh())
        if low == high:
            doorIsOpen = None
        elif high == 1 and low == 0:
            doorIsOpen = False
            #door is close
        elif high == 0 and low == 1 :
            doorIsOpen = True
            #door is open
        else:
            doorIsOpen = None

        return doorIsOpen

class LightSwitch:
    def __init__(self):
        self.config=Config().conf
        self.setUpGpios()

    def setUpGpios(self):
        INPUT = 0
        wiringpi.wiringPiSetupGpio()
        wiringpi.pinMode(int(self.config['SENSORS']['endSwitch_1']), INPUT)
        wiringpi.pinMode(int(self.config['SENSORS']['endSwitch_2']), INPUT)


class Lightsensor:
    def __init__(self):
        self.conf=Config().conf
        self.init_i2c()
        self.longtime=None
        self.total_average=None
        self.measurement=[]

    def init_i2c(self):
        self.ADRESS = int(self.conf['I2C']['ligthsensor'], 16)
        self.POWER_DOWN = 0x00  # No active state
        self.POWER_ON = 0x01  # Power on
        self.RESET = 0x07  # Reset data register value

        # Start measurement at 4lx resolution. Time typically 16ms.
        self.CONTINUOUS_LOW_RES_MODE = 0x13
        # Start measurement at 1lx resolution. Time typically 120ms
        self.CONTINUOUS_HIGH_RES_MODE_1 = 0x10
        # Start measurement at 0.5lx resolution. Time typically 120ms
        self.CONTINUOUS_HIGH_RES_MODE_2 = 0x11
        # Start measurement at 1lx resolution. Time typically 120ms
        # Device is automatically set to Power Down after measurement.
        self.ONE_TIME_HIGH_RES_MODE_1 = 0x20
        # Start measurement at 0.5lx resolution. Time typically 120ms
        # Device is automatically set to Power Down after measurement.
        self.ONE_TIME_HIGH_RES_MODE_2 = 0x21
        # Start measurement at 1lx resolution. Time typically 120ms
        # Device is automatically set to Power Down after measurement.
        self.ONE_TIME_LOW_RES_MODE = 0x23

        # bus = smbus.SMBus(0) # Rev 1 Pi uses 0
        self.bus = smbus.SMBus(1)  # Rev 2 Pi uses 1


    def convertToNumber(self, data):
        result = (data[1] + (256 * data[0])) / 1.2
        return result

    def collect_values(self):
        return self.convertToNumber(self.bus.read_i2c_block_data(self.ADRESS, self.ONE_TIME_LOW_RES_MODE))

    def get_lowres(self):
        return self.convertToNumber(self.bus.read_i2c_block_data(self.ADRESS, self.ONE_TIME_LOW_RES_MODE))

    def get_highres(self):
        return self.convertToNumber(self.bus.read_i2c_block_data(self.ADRESS, self.CONTINUOUS_HIGH_RES_MODE_1))
    def get_highres2(self):
        return self.convertToNumber(self.bus.read_i2c_block_data(self.ADRESS, self.CONTINUOUS_HIGH_RES_MODE_2))

    def remove_high_low(self,values):
        if values:
            if len(values)==10:
                for i in range(0,4,1):
                    values.remove(max(values))

                for i in range(0,5,1):
                    values.remove(min(values))
                return values

    def readLight(self):
        data = []
        while len(data)!=10:
            data.append(self.collect_values())
            time.sleep(2)
        data=self.remove_high_low(data)
        return data[0]


    def run(self):
        if len(self.measurement) >= 60:
            self.measurement.pop(0)
        value=self.readLight()
        if value:
            self.measurement.append(value)
        self.total_average=round(sum(self.measurement)/len(self.measurement),2)
        return self.total_averag

    def test(self):
        return self.convertToNumber(self.bus.read_i2c_block_data(self.ADRESS, self.ONE_TIME_HIGH_RES_MODE_2))