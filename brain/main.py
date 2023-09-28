import subprocess
import sys
import time
from signal import pause
from modules.mqtt.mqtt import Mqtt_Worker
from threading import Event
from modules.sensors.sensors import EndSwitch
from apscheduler.schedulers.background import BackgroundScheduler
from modules.config.config import Config
from modules.engines.engine import Door
from datetime import datetime

class Processor:
    def __init__(self):
        self.config = Config().read_config()
        self.init_var()
        self.init_schedule()
        self.mqtt = Mqtt_Worker()
        self.endswitch=EndSwitch()
        self.door=Door()
        listener_endswitch = Mqtt_Worker(sub='sensors/endswitch', function=self.endswitch_mapper)
        listener_light = Mqtt_Worker(sub='sensors/light', function=self.light_mapper)

        self.start_processes()
        #listener_light = Mqtt_Worker(sub='sensors/light', function=self.light_mapper)
        #listener_endswitch = Mqtt_Worker(sub='sensors/endswitch', function=self.endswitch_mapper)

        self.compute()
        Event().wait()

    def light_mapper(self, msg):
        self.light = int(msg.payload.decode('utf-8'))

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

    def endswitch_mapper(self, msg):
        self.doorIsOpen =int(msg.payload.decode('utf-8'))
        if self.doorIsOpen == 0:
            self.doorIsOpen = True
        elif self.doorIsOpen == 1:
            self.doorIsOpen = False
        # value = 0 = Open
        # value = 1 = Close

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
        p = subprocess.Popen([sys.executable, '../lightsensor/main.py'], stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        print('Starting Endswitches')
        p2 = subprocess.Popen([sys.executable, '../endswitch/main.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print('Starting Engines')
        p3 = subprocess.Popen([sys.executable, '../engine/main.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def compute(self):
        while True:
            while self.doorIsOpen == None:
                time.sleep(1)
            if self.doorIsOpen == 2:  # Calibration
                if not self.door.find_position():
                    exit(1)
            else:  # Door position is clear
                if self.opentime and not self.closingtime and self.light <= int(self.config['TIMING']['light']) and self.doorIsOpen:
                    print('1 close door')
                    self.mqtt.send(topic='control/door', payload=2)
                    time.sleep(10)
                elif self.opentime and not self.closingtime and self.light > int(self.config['TIMING']['light']) and self.doorIsOpen:
                    print('2 keep open')
                elif self.opentime and not self.closingtime and self.light > int(self.config['TIMING']['light']) and not self.doorIsOpen:
                    print('3 open door')
                    #run command
                    self.mqtt.send(topic='control/door', payload=1)
                    time.sleep(10)
                elif not self.opentime and self.closingtime and self.light <= int(self.config['TIMING']['light']) and not self.doorIsOpen:
                    print('4 keep close')
                elif not self.opentime and self.closingtime and self.light > int(self.config['TIMING']['light']) and not self.doorIsOpen:
                     print('5 open door')
                elif not self.opentime and self.closingtime and self.light <= int(self.config['TIMING']['light']) and self.doorIsOpen:
                    print('6 close door')
                elif not self.opentime and self.closingtime and self.light > int(self.config['TIMING']['light']) and self.doorIsOpen:
                    print('7 keep open')
                else:
                    print('cornercase')
                time.sleep(1)

Processor()
