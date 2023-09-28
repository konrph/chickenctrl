import time
from gpiozero import Button
from modules.config.config import Config
from modules.mqtt.mqtt import Mqtt_Worker
from modules.sensors.sensors import EndSwitch
from threading import Event

config = Config().conf
high = Button(int(config['SENSORS']['endSwitch_HIGH']))
low = Button(int(config['SENSORS']['endSwitch_LOW']))
mqtt = Mqtt_Worker(broker='127.0.0.1')
swtich = EndSwitch()


def on_press():
    if high.is_pressed:
        mqtt.send(topic='sensors/endswitch', payload=1)

    if low.is_pressed:
        mqtt.send(topic='sensors/endswitch', payload=0)
def read_sensors():
    while True:
        highvalue = int(EndSwitch().readHigh())
        lowvalue = int(EndSwitch().readLow())

        if highvalue == lowvalue:  # Door is in a faulty postion
            mqtt.send(topic='sensors/endswitch', payload=2)
            value = 2
        else:
            if highvalue == 1:  # Door is open
                mqtt.send(topic='sensors/endswitch', payload=1)
                value = 1
            else:  # Door is closed
                mqtt.send(topic='sensors/endswitch', payload=0)
                value = 0
        time.sleep(0.25)
def main():
    read_sensors()

if __name__ == "__main__":
    main()
