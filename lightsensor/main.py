# !/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from modules.mqtt.mqtt import Mqtt_Worker
from modules.sensors.sensors import Lightsensor
import time

def main():
    mqtt=Mqtt_Worker(broker='127.0.0.1',port=1883)
    sensor = Lightsensor()
    while True:
        value=int(sensor.readLight())
        mqtt.send(topic='sensors/light',payload=value)
        time.sleep(0.5)

if __name__ == "__main__":
    main()