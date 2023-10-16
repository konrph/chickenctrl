#!/usr/bin python3
# encoding: utf-8
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import multiprocessing
import threading
import time
from flask import Flask, json
from modules.sensors.sensors import Lightsensor, EndSwitch, Temperature
from modules.engines.engine import Door
from modules.config.config import Config
from datetime import datetime, timedelta

app = Flask(__name__)


class Rest:
    def __init__(self):
        self.conf = Config().conf
        self.lock = threading.Lock()
        self.manlock = threading.Lock()
        self.open_process = None
        self.close_process = None
        self.ls = Lightsensor()
        self.es = EndSwitch()
        self.ts = Temperature()
        self.door = Door()
        self.timeout = multiprocessing.Value('i', 0)

    def openDoorProcess(self):
        self.door.open(unsafe=True)
        self.do_sleep()

    def closeDoorProcess(self):
        self.door.close(unsafe=True)
        self.do_sleep()

    def do_sleep(self):
        while self.timeout.value > 0:
            time.sleep(1)
            self.timeout.value -= 1

    def openDoor(self, time=0):
        with self.lock:
            self.timeout.value = time
            if self.close_process and self.close_process.is_alive() or self.open_process and self.open_process.is_alive():
                return json.dumps({'result': 'already running'})
            open_process = multiprocessing.Process(target=self.openDoorProcess)
            open_process.start()
        return json.dumps({'result': 'ok', 'value': 'null'})

    def closeDoor(self, time=0):
        with self.lock:
            self.timeout.value = time
            if self.close_process and self.close_process.is_alive() or self.open_process and self.open_process.is_alive():
                return json.dumps({'result': 'already running'})
            close_process = multiprocessing.Process(target=self.closeDoorProcess)
            close_process.start()
        return json.dumps({'result': 'ok', 'value': 'null'})

    def stopDoor(self):
        if self.open_process and self.open_process.is_alive():
            while self.open_process.is_alive():
                self.open_process.terminate()  # Terminate the openDoor process

        if self.close_process and self.close_process.is_alive():
            while self.close_process.is_alive():
                self.close_process.terminate()  # Terminate the closeDoor process
        self.door.stop()
        return json.dumps({'result': 'ok', 'value': 'null'})

    def manualClose(self):
        with self.manlock:
            self.stopDoor()
            self.closeDoor(time=self.calculate_next_event())
        return json.dumps({'result': 'ok', 'value': None})

    def manualOpen(self):
        with self.manlock:
            self.stopDoor()
            self.openDoor(time=self.calculate_next_event())
        return json.dumps({'result': 'ok', 'value': None})

    def readLight(self):
        return json.dumps({'result': 'ok', 'value': int(self.ls.get_highres())})

    def getEndswitchHigh(self):
        return json.dumps({'value': self.es.readHigh()})

    def getEndswitchLow(self):
        return json.dumps({'value': self.es.readLow()})

    def getDoorPosition(self):
        return json.dumps({'result': 'ok', 'value': self.es.doorisOpen()})

    def readTemp1(self):
        try:
            return json.dumps({'value': self.ts.readTempSensor1()})
        except:
            return json.dumps({'value': None})

    def readTemp2(self):
        try:
            return json.dumps({'value': self.ts.readTempSensor2()})
        except:
            return json.dumps({'value': None})

    def readTimeout(self):
        return json.dumps({'value': self.timeout.value})

    def calculate_next_event(self):

        current_date_time = datetime.now()

        # Calculate the opening and closing times for the current day
        opening_time = datetime.strptime(self.conf['TIMING']['open'], '%H:%M').replace(
            year=current_date_time.year,
            month=current_date_time.month,
            day=current_date_time.day
        )

        closing_time = datetime.strptime(self.conf['TIMING']['close'], '%H:%M').replace(
            year=current_date_time.year,
            month=current_date_time.month,
            day=current_date_time.day
        )

        next_day_opening_time = opening_time + timedelta(days=1)

        if current_date_time < opening_time:
            next_event = "Opening"
            time_until_event = opening_time - current_date_time
        elif closing_time <= current_date_time < next_day_opening_time:
            next_event = "Opening"
            time_until_event = next_day_opening_time - current_date_time
        else:
            next_event = "Closing"
            time_until_event = closing_time - current_date_time

        # Calculate the number of seconds until the next event
        seconds_until_event = time_until_event.total_seconds()

        return abs(int(seconds_until_event - (2 * 60 * 60)))


@app.route('/get/timeout')
def get_timeout():
    return r.readTimeout()


@app.route('/get/temp2')
def get_temp2():
    return r.readTemp2()


@app.route('/get/temp1')
def get_temp1():
    return r.readTemp1()


@app.route('/get/door/position')
def get_door_position():
    return r.getDoorPosition()


@app.route('/get/endswitch/low')
def get_endswitch_low():
    return r.getEndswitchLow()


@app.route('/get/endswitch/high')
def get_endswitch_high():
    return r.getEndswitchHigh()


@app.route('/get/light')
def get_light():
    return r.readLight()


@app.route('/control/door/manual/open')
def control_door_manual_open():
    return r.manualOpen()


@app.route('/control/door/manual/close')
def control_door_manual_close():
    return r.manualClose()


@app.route('/control/door/open')
def control_door_open():
    return r.openDoor(time=0)


@app.route('/control/door/close')
def control_door_close():
    return r.closeDoor(time=0)


@app.route('/control/door/stop')
def control_door_stop():
    return r.stopDoor()


def main():
    app.run(host='0.0.0.0', port=5000)


r = Rest()
if __name__ == '__main__':
    main()
