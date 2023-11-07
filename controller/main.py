#!/usr/bin python3
# encoding: utf-8
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import requests
import time
from  modules.config.config import Config
from datetime import datetime


base_url = 'http://localhost:5000'

def read_config():
    global conf
    conf = Config().conf


# Function to check if it's bright enough to open the door
def is_bright_enough():
    response = requests.get(f'{base_url}/get/light')
    if response.status_code == 200:
        light_value = response.json().get('value')
        # Adjust this threshold value as per your brightness criteria
        return light_value >= int(conf['TIMING']['light_open'])  # Example threshold: 100
    return False

# Function to check if it's dark enough to close the door
def is_dark_enough():
    response = requests.get(f'{base_url}/get/light')
    if response.status_code == 200:
        light_value = response.json().get('value')
        # Adjust this threshold value as per your darkness criteria
        return light_value < int(int(conf['TIMING']['light_close']))  # Example threshold: 50
    return False


def is_moving():
    response = requests.get(f'{base_url}/get/doormovment')
    if response.status_code == 200:
        moving = response.json().get('value')
        # Adjust this threshold value as per your darkness criteria
        if moving == 'True':
            return True
        elif moving == 'False':
            return False
        else:
            return None

# Function to check if it's time to open the door in the morning
def is_time_to_open():
    global conf
    current_date_time = datetime.now()
    opening_time = datetime.strptime(conf['TIMING']['open'], '%H:%M').replace(year=current_date_time.year,
                                                               month=current_date_time.month,
                                                               day=current_date_time.day)
    return current_date_time >= opening_time

# Function to check if it's time to close the door in the evening
def is_time_to_close():
    global conf
    current_date_time = datetime.now()
    closing_time = datetime.strptime(conf['TIMING']['close'], '%H:%M').replace(year=current_date_time.year,
                                                                            month=current_date_time.month,
                                                                            day=current_date_time.day)
    return current_date_time >= closing_time

# Function to open the door
def open_door():
    response = requests.get(f'{base_url}/control/door/open')
    if response.status_code == 200:
        result = response.json().get('result')
        return result == 'ok'
    return False

def stop_door():
    response = requests.get(f'{base_url}/control/door/stop')
    if response.status_code == 200:
        result = response.json().get('result')
        return result == 'ok'
    return False

# Function to close the door
def close_door():
    response = requests.get(f'{base_url}/control/door/close')
    if response.status_code == 200:
        result = response.json().get('result')
        return result == 'ok'
    return False

def read_door():
    response = requests.get(f'{base_url}/get/door/position')
    if response.status_code == 200:
        result = response.json().get('value')
        return result
    return False

# Main controller logic
def main():
    read_config()
    while True:
        try:
            if read_door() == False:
                # door is close
                if not is_time_to_close() and is_bright_enough() == True:
                    if is_time_to_open() or is_bright_enough() and not is_moving():
                        print('Open Door Automatic')
                        open_door()


            if read_door() == True:
                # door is open
                if is_time_to_close() or is_bright_enough() == False and not is_moving():
                    print('Close Door Automatic')
                    close_door()

            time.sleep(1)
        except KeyboardInterrupt:
            stop_door()
            break

if __name__ == '__main__':
    main()
