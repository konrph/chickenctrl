#!/usr/bin/env python
# encoding: utf-8
import json
import time
import multiprocessing
import threading
from flask import Flask
lock = threading.Lock()
app = Flask(__name__)

# Process objects for openDoor and closeDoor functions
open_process = None
close_process = None

def openDoorProcess():
    ############ Dummy Function
    for i in range(1, 11):
        print('opening')
        time.sleep(1)

def closeDoorProcess():
    ############ Dummy Function
    for i in range(1, 11):
        print('opening')
        time.sleep(1)

@app.route('/control/door/open')
def openDoor():
    global open_process
    with lock:
        if open_process and open_process.is_alive():
            return json.dumps({'result': 'already running'})
        open_process = multiprocessing.Process(target=openDoorProcess)
        open_process.start()
        open_process.join()
    return json.dumps({'result': 'ok'})


@app.route('/control/door/close')
def closeDoor():
    global close_process
    with lock:
        if close_process and close_process.is_alive():
            return json.dumps({'result': 'already running'})
        close_process = multiprocessing.Process(target=closeDoorProcess)
        close_process.start()
        close_process.join()
    return json.dumps({'result': 'ok'})

@app.route('/control/door/stop')
def stopDoor():
    global open_process
    global close_process

    if open_process and open_process.is_alive():
        open_process.terminate()  # Terminate the openDoor process

    if close_process and close_process.is_alive():
        close_process.terminate()  # Terminate the openDoor process

    #TODO Add Engine Stop

    return json.dumps({'result': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
