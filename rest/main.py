#!/usr/bin/env python
# encoding: utf-8
import multiprocessing
import threading
import time
from flask import Flask, jsonify, json
from modules.sensors.sensors import Lightsensor, EndSwitch

lock = threading.Lock()
app = Flask(__name__)

# Process objects for openDoor and closeDoor functions
open_process = None
close_process = None

ls = Lightsensor()
es = EndSwitch()


def openDoorProcess():
    ############ Dummy Function
    for i in range(1, 11):
        print('opening')
        time.sleep(1)


def closeDoorProcess():
    ############ Dummy Function
    for i in range(1, 11):
        print('closing')
        time.sleep(1)


@app.route('/control/door/open')
def openDoor():
    global open_process
    with lock:
        if open_process and open_process.is_alive():
            return json.dumps({'result': 'already running'})
        open_process = multiprocessing.Process(target=openDoorProcess)
        open_process.start()
    return json.dumps({'result': 'ok'})


@app.route('/control/door/close')
def closeDoor():
    global close_process
    with lock:
        if close_process and close_process.is_alive():
            return json.dumps({'result': 'already running'})
        close_process = multiprocessing.Process(target=closeDoorProcess)
        close_process.start()
    return json.dumps({'result': 'ok'})


@app.route('/control/door/stop')
def stopDoor():
    global open_process, close_process

    if open_process and open_process.is_alive():
        open_process.terminate()  # Terminate the openDoor process

    if close_process and close_process.is_alive():
        close_process.terminate()  # Terminate the closeDoor process

    # TODO: Add Engine Stop

    return json.dumps({'result': 'ok'})


@app.route('/get/light')
def readLight():
    return json.dumps({'value': int(ls.get_highres())})


@app.route('/get/endswitch/high')
def getEndswitchHigh():
    return json.dumps({'value': es.readHigh()})


@app.route('/get/endswitch/low')
def getEndswitchLow():
    return json.dumps({'value': es.readLow()})


@app.route('/get/door/position')
def getDoorPosition():
    return json.dumps({'value': es.doorisOpen()})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
