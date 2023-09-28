from modules.mqtt.mqtt import Mqtt_Worker
from modules.sensors.sensors import Temperature
import time

def main():
    mqtt = Mqtt_Worker(broker='127.0.0.1',port=1883)
    sensor = Temperature()
    while True:
        time.sleep(1)
        mqtt.send(topic='sensors/temperature/1', payload=sensor.readTempSensor1())
        mqtt.send(topic='sensors/temperature/2', payload=sensor.readTempSensor2())

if __name__ == "__main__":
    main()