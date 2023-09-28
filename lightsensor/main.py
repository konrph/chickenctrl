# !/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from apscheduler.schedulers.blocking import BlockingScheduler

from modules.mqtt.mqtt import Mqtt_Worker
from modules.sensors.sensors import Lightsensor

global sensor

sensor = Lightsensor()
mqtt=Mqtt_Worker(broker='127.0.0.1',port=1883)

def rw_light():
    value = int(sensor.readLight())
    mqtt.send(topic='sensors/light', payload=value)

def main():
    rw_light()
    scheduler = BlockingScheduler()
    scheduler.add_job(rw_light, 'interval', seconds=60)
    scheduler.start()

if __name__ == "__main__":
    main()