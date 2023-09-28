import os
import sys
import time
from apscheduler.schedulers.blocking import BlockingScheduler
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from modules.mqtt.mqtt import Mqtt_Worker
from modules.sensors.sensors import Temperature

global mqtt
global sensor

mqtt = Mqtt_Worker(broker='127.0.0.1',port=1883)
sensor = Temperature()

def rw_temp():
    try:
        mqtt.send(topic='sensors/temperature/1', payload=sensor.readTempSensor1())
        mqtt.send(topic='sensors/temperature/2', payload=sensor.readTempSensor2())
    except:
        mqtt.send(topic='sensors/temperature/1', payload='n/a')
        mqtt.send(topic='sensors/temperature/2', payload='n/a')

def main():
    scheduler = BlockingScheduler()
    scheduler.add_job(rw_temp, 'interval', seconds=5)
    scheduler.start()

if __name__ == "__main__":
    main()

