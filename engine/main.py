import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import time
from modules.mqtt.mqtt import Mqtt_Worker
from modules.engines.engine import Door, Feeder

from signal import pause
from modules.sensors.sensors import EndSwitch
import threading
door = Door()
feeder = Feeder()

# Variables to track the latest received commands and their timestamps
latest_door_command = {"command": None, "timestamp": None}
latest_feeder_command = {"command": None, "timestamp": None}
switch = EndSwitch()


def run_door(msg):
    id = msg.payload.decode('utf-8')
    if id == '0':
        print(0)
        latest_door_command["command"] = "stopping"
        latest_door_command["timestamp"] = time.time()
        door.stop()
    elif id == '1':
        print(2)
        if not switch.doorisOpen():
            latest_door_command["command"] = "open"
            latest_door_command["timestamp"] = time.time()
            door.open()
    elif id == '2':
        print(3)
        if switch.doorisOpen():
            latest_door_command["command"] = "closing"
            latest_door_command["timestamp"] = time.time()
            door.close()

def run_feeder(msg):
    id = msg.payload.decode('utf-8')
    if id == '1':
        latest_feeder_command["command"] = "run"
        latest_feeder_command["timestamp"] = time.time()
    elif id == '0':
        latest_feeder_command["command"] = "stop"
        latest_feeder_command["timestamp"] = time.time()

def process_commands():
    while True:
        # Check if there's a new door command
        if latest_door_command["timestamp"] is not None:
            current_time = time.time()
            command = latest_door_command["command"]
            timestamp = latest_door_command["timestamp"]

            # Check if the command is still valid (not too old)
            if current_time - timestamp <= 60:  # Assuming a maximum execution time of 60 seconds
                if command == "open":
                    time.sleep(659)
                    #door.open()
                elif command == "stop":
                    print('stop')
                    #door.stop()

            # Reset the latest_door_command
            latest_door_command["command"] = None
            latest_door_command["timestamp"] = None

        # Check if there's a new feeder command
        if latest_feeder_command["timestamp"] is not None:
            current_time = time.time()
            command = latest_feeder_command["command"]
            timestamp = latest_feeder_command["timestamp"]

            # Check if the command is still valid (not too old)
            if current_time - timestamp <= 60:  # Assuming a maximum execution time of 60 seconds
                if command == "run":
                    #feeder.run()
                    print('rund')
                elif command == "stop":
                    print('stop')
                    #feeder.stop()

            # Reset the latest_feeder_command
            latest_feeder_command["command"] = None
            latest_feeder_command["timestamp"] = None

        # Sleep for a short interval before checking for new commands again
        time.sleep(1)

def main():
    door_thread = Mqtt_Worker(broker='127.0.0.1', port=1883, function=run_door, sub='control/door')
    feeder_thread = Mqtt_Worker(broker='127.0.0.1', port=1883, function=run_feeder, sub='control/feeder')

    # Start the command processing thread
    command_thread = threading.Thread(target=process_commands)
    command_thread.daemon = True
    command_thread.start()
    pause()
if __name__ == "__main__":
    main()
