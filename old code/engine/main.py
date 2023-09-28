import time

from modules.mqtt.mqtt import Mqtt_Worker
from modules.engines.engine import Door,Feeder
from modules.sensors.sensors import EndSwitch
from threading import Event

door = Door()
feeder = Feeder()

def run_door(msg):
    id = msg.payload.decode('utf-8')
    switch = EndSwitch()
    if id == '0':
        door.stop()
        print('Stopping Door')

    elif id == '1':
        if door.ready() and not switch.doorisOpen() and not door.engineRunning():
            door.open_step_big()
            while switch.readHigh() != 0:
                door.open_step()
        time.sleep(2)
        print('Opend Door')

    elif id == '2':
        if door.ready() and switch.doorisOpen() and not door.engineRunning():
            door.close_step_big()
            while switch.readLow() != 0:
                door.close_step()
        time.sleep(2)
        print('Closed Door')

    elif id == '3':
        door.close_step()
        print('Baby Step down')

    elif id == '4':
        door.open_step()
        print('Baby Step up')

    else:
        print('Unknown Command')

def run_feeder(msg):
    id = msg.payload.decode('utf-8')
    if id == '1':
        feeder.run()
        print('Starting Door')
    if id == '0':
        feeder.stop()
        print('Stopping Door')


def main():
    Mqtt_Worker(broker='127.0.0.1', port=1883, function=run_door, sub='control/door')
    Mqtt_Worker(broker='127.0.0.1', port=1883, function=run_feeder, sub='control/feeder')
    Event().wait()


if __name__ == "__main__":
    main()