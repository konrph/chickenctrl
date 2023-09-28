import os
import sys
import wiringpi
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from signal import pause
from gpiozero import Button
from modules.config.config import Config
from modules.mqtt.mqtt import Mqtt_Worker
from apscheduler.schedulers.blocking import BlockingScheduler



wiringpi.wiringPiSetupGpio()

config = Config().conf
high = Button(int(config['SENSORS']['endSwitch_HIGH']))
low = Button(int(config['SENSORS']['endSwitch_LOW']))
mqtt = Mqtt_Worker(broker='127.0.0.1')

def high_press():
    mqtt.send(topic='control/door', payload='0')
    mqtt.send(topic='sensors/endswitch', payload=1)

def low_press():
    mqtt.send(topic='control/door', payload='0')
    mqtt.send(topic='sensors/endswitch', payload=0)

def init_schedule():
    scheduler = BlockingScheduler()
    scheduler.add_job(init, 'interval', seconds=5)
    scheduler.start()

def init():
    if low.is_pressed:
        mqtt.send(topic='control/door', payload='0')
        mqtt.send(topic='sensors/endswitch', payload=0)

    if high.is_pressed:
        mqtt.send(topic='control/door', payload='0')
        mqtt.send(topic='sensors/endswitch', payload=1)

    if not low.is_pressed and not high.is_pressed:
        mqtt.send(topic='control/door', payload='0')
        mqtt.send(topic='sensors/endswitch', payload=2)

def main():
    init_schedule()
    init()

    high.when_pressed = high_press
    low.when_pressed = low_press


    pause()

if __name__ == "__main__":
    main()