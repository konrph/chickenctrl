import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import subprocess
import sys
import time
from modules.mqtt.mqtt import Mqtt_Worker
from threading import Event
from apscheduler.schedulers.background import BackgroundScheduler
from modules.config.config import Config
from datetime import datetime

class Processor:
    def __init__(self):
        self.config = Config().read_config()
        self.init_var()
        self.init_schedule()
        self.mqtt = Mqtt_Worker()
        listener_endswitch = Mqtt_Worker(sub='sensors/endswitch', function=self.endswitch_mapper)
        listener_light = Mqtt_Worker(sub='sensors/light', function=self.light_mapper)

        self.start_processes()
        self.compute()
        Event().wait()

    def light_mapper(self, msg):
        self.light = int(msg.payload.decode('utf-8'))

    def endswitch_mapper(self, msg):
        self.doorIsOpen =int(msg.payload.decode('utf-8'))
        if self.doorIsOpen == 0:
            self.doorIsOpen = True
        elif self.doorIsOpen == 1:
            self.doorIsOpen = False
        # value = 0 = Open
        # value = 1 = Close

    def init_schedule(self):

        self.schedule = BackgroundScheduler()
        self.schedule.add_job(func=self.schedule_open, trigger='cron',
                              hour=int(self.config['TIMING']['open'].split(':')[0]),
                              minute=int(self.config['TIMING']['open'].split(':')[1]))
        self.schedule.add_job(func=self.schedule_close, trigger='cron',
                              hour=int(self.config['TIMING']['close'].split(':')[0]),
                              minute=int(self.config['TIMING']['close'].split(':')[1]))

        self.schedule.start()

    def schedule_open(self):
        self.opentime = True
        self.closingtime = False

    def schedule_close(self):
        self.opentime = False
        self.closingtime = True

    def init_var(self):
        self.light = None
        self.endswitch = None
        self.doorIsOpen = None
        current_date_time = datetime.now()
        opening = datetime.strptime(self.config['TIMING']['open'], '%H:%M').replace(year=current_date_time.year, month=current_date_time.month, day=current_date_time.day)
        closing = datetime.strptime(self.config['TIMING']['close'], '%H:%M').replace(year=current_date_time.year, month=current_date_time.month, day=current_date_time.day)

        if opening < current_date_time and closing > current_date_time:
            self.opentime = True
            self.closingtime = False
        else:
            self.closingtime = True
            self.opentime = False

    def start_processes(self):
        print('Starting Lightsensor')
        #p = subprocess.Popen([sys.executable, '../lightsensor/main.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print('Starting Endswitches')
       # p2 = subprocess.Popen([sys.executable, '../endswitch/main.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print('Starting Engines')
        #p3 = subprocess.Popen([sys.executable, '../engine/main.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def compute(self):
        done=None
        while True:
            while self.light == None:
                time.sleep(1)
            #if self.doorIsOpen == 2:  # Calibration
            #    if not self.door.find_position():
            #        exit(1)
            if None:
                pass

            else:  # Door position is clear
                if self.opentime and not self.closingtime and self.light <= int(self.config['TIMING']['light']):
                    print('1 close door')
                    #zu dunkel
                    if done != 1:
                        self.mqtt.send(topic='control/door', payload=2)
                        done = 1
                elif self.opentime and not self.closingtime and self.light > int(self.config['TIMING']['light']):
                    print('2 keep open')
                    if done != 2:
                        self.mqtt.send(topic='control/door', payload=1)
                        done = 2
                elif self.opentime and not self.closingtime and self.light > int(self.config['TIMING']['light']):
                    print('3 open door')
                    if done != 3:
                        self.mqtt.send(topic='control/door', payload=1)
                        done = 3
                elif not self.opentime and self.closingtime and self.light <= int(self.config['TIMING']['light']):
                    print('4 keep close')
                    if done != 4:
                        self.mqtt.send(topic='control/door', payload=2)
                        done = 4
                elif not self.opentime and self.closingtime and self.light > int(self.config['TIMING']['light']):
                     print('5 open door')
                     if done !=5:
                        self.mqtt.send(topic='control/door', payload=1)
                        done = 5
                elif not self.opentime and self.closingtime and self.light <= int(self.config['TIMING']['light']):
                    print('6 close door')
                    if done != 6:
                        self.mqtt.send(topic='control/door', payload=2)
                        done = 6
                elif not self.opentime and self.closingtime and self.light > int(self.config['TIMING']['light']):
                    print('7 keep open')
                    if done != 7:
                        self.mqtt.send(topic='control/door', payload=1)
                        done = 7
                else:
                    print('cornercase')
                    done = None
                time.sleep(1)

Processor()
