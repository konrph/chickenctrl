from modules.sensors.sensors import Lightsensor
from modules.mqtt.mqtt import Mqtt_Worker
import modules.config.config
import time
import random

def main():
    mqtt = Mqtt_Worker(broker='127.0.0.1', port=1883)
    sensor = Lightsensor()
    while True:
        value=sensor.readLight()
        mqtt.send(topic='sensors/light',payload=int(value),retain=True)
        print(f'Light value is {value}')
        time.sleep(1)


if __name__ == "__main__":
    main()
