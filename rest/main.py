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

lock = threading.Lock()
manlock = threading.Lock()
app = Flask(__name__)

# Process objects for openDoor and closeDoor functions
open_process = None
close_process = None

global es
global d
global timeout
ls = Lightsensor()
es = EndSwitch()
ts = Temperature()
d = Door()
timeout = 0


def read_config():
    global conf
    conf = Config().conf


def openDoorProcess():
    global d, timeout
    d.open(unsafe=True)
    do_sleep()


def closeDoorProcess():
    global d, timeout
    d.close(unsafe=True)
    do_sleep()


def do_sleep():
    global timeout
    i = timeout
    while i >= 0:
        time.sleep(1)
        i -= 1
        timeout = i


@app.route('/control/door/open')
def openDoor(time=0):
    global close_process, open_process, timeout
    with lock:
        timeout = time
        if close_process and close_process.is_alive() or open_process and open_process.is_alive():
            return json.dumps({'result': 'already running'})
        open_process = multiprocessing.Process(target=openDoorProcess)
        open_process.start()
    return json.dumps({'result': 'ok', 'value': 'null'})


@app.route('/control/door/close')
def closeDoor(time=0):
    global close_process, open_process, timeout
    with lock:
        timeout = time
        if close_process and close_process.is_alive() or open_process and open_process.is_alive():
            return json.dumps({'result': 'already running'})
        close_process = multiprocessing.Process(target=closeDoorProcess)
        close_process.start()
    return json.dumps({'result': 'ok', 'value': 'null'})


@app.route('/control/door/stop')
def stopDoor():
    global open_process, close_process, d

    if open_process and open_process.is_alive():
        while open_process.is_alive():
            open_process.terminate()  # Terminate the openDoor process
            open_process = None

    if close_process and close_process.is_alive():
        while close_process.is_alive():
            close_process.terminate()  # Terminate the closeDoor process
            close_process = None
    time.sleep(0.25)
    d.stop()

    return json.dumps({'result': 'ok', 'value': 'null'})


@app.route('/control/door/manual/close')
def manualClose():
    with manlock:
        stopDoor()
        closeDoor(time=calculate_next_event())
    return json.dumps({'result': 'ok', 'value': None})


@app.route('/control/door/manual/open')
def manualOpen():
    with manlock:
        stopDoor()
        openDoor(time=calculate_next_event())
    return json.dumps({'result': 'ok', 'value': None})


@app.route('/get/light')
def readLight():
    return json.dumps({'result': 'ok', 'value': int(ls.get_highres())})


@app.route('/get/endswitch/high')
def getEndswitchHigh():
    return json.dumps({'value': es.readHigh()})


@app.route('/get/endswitch/low')
def getEndswitchLow():
    return json.dumps({'value': es.readLow()})


@app.route('/get/door/position')
def getDoorPosition():
    global es
    return json.dumps({'result': 'ok', 'value': es.doorisOpen()})


@app.route('/get/temp1')
def readTemp1():
    global ts
    return json.dumps({'value': ts.readTempSensor1()})


@app.route('/get/temp2')
def readTemp2():
    global ts
    return json.dumps({'value': ts.readTempSensor2()})


@app.route('/get/timeout')
def readTimeout():
    global timeout
    return json.dumps({'value': timeout})


def calculate_next_event():
    global conf
    current_date_time = datetime.now()

    # Calculate the opening and closing times for the current day
    opening_time = datetime.strptime(conf['TIMING']['open'], '%H:%M').replace(
        year=current_date_time.year,
        month=current_date_time.month,
        day=current_date_time.day
    )

    closing_time = datetime.strptime(conf['TIMING']['close'], '%H:%M').replace(
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


if __name__ == '__main__':
    read_config()
    app.run(host='0.0.0.0', port=5000)
