import requests
import time
from datetime import datetime
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

# Function to check if it's time to open the door in the morning
def is_time_to_open(opening_time):
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
                if not is_time_to_close():
                    if is_time_to_open() or is_bright_enough():
                        state = 'open'


            if read_door() == True:
                # door is open
                if is_time_to_close() or not is_bright_enough():
                    state = 'close'

            # Sleep for a specified interval (e.g., 5 minutes)
            # Adjust the sleep interval as needed
            time.sleep(300)  # 5 minutes
        except KeyboardInterrupt:
            break

if __name__ == '__main__':
    main()