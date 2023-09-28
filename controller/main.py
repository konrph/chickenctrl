import time
from modules.mqtt.mqtt import Mqtt_Worker
from apscheduler.schedulers.background import BackgroundScheduler
from modules.config.config import Config
from datetime import datetime


class Processor:
    def __init__(self):
        self.config = Config().read_config()
        self.init_vars()
        self.init_schedule()
        self.mqtt = Mqtt_Worker()
        self.listen_mqtt()
        self.manual_control = False

    def init_vars(self):
        self.light = None
        self.doorIsOpen = None
        self.opentime = False
        self.closingtime = False

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

    def listen_mqtt(self):
        listener_endswitch = Mqtt_Worker(sub='sensors/endswitch', function=self.endswitch_mapper)
        listener_light = Mqtt_Worker(sub='sensors/light', function=self.light_mapper)
        listener_manual = Mqtt_Worker(sub='control/manual', function=self.manual_control_handler)

    def light_mapper(self, msg):
        self.light = int(msg.payload.decode('utf-8'))

    def endswitch_mapper(self, msg):
        self.doorIsOpen = int(msg.payload.decode('utf-8'))
        self.doorIsOpen = self.doorIsOpen == 0  # Convert to boolean
        # 0 = Open, 1 = Close

    def manual_control_handler(self, msg):
        control_command = msg.payload.decode('utf-8')
        if control_command == "open":
            self.manual_control = True
            self.mqtt.send(topic='control/door', payload=1)  # Open the door manually
        elif control_command == "close":
            self.manual_control = True
            self.mqtt.send(topic='control/door', payload=2)  # Close the door manually
        elif control_command == "auto":
            self.manual_control = False  # Resume automatic control

    def compute(self):
        done = None
        while True:
            while self.light is None:
                time.sleep(1)

            if not self.manual_control:
                # Automatic control logic
                control_action = self.get_control_action()

                if done != control_action:
                    self.mqtt.send(topic='control/door', payload=control_action)
                    done = control_action

            time.sleep(1)

    def get_control_action(self):
        if self.opentime:
            if self.light <= int(self.config['TIMING']['light']):
                return 2  # Close door
            else:
                return 1  # Keep open
        else:
            if self.light <= int(self.config['TIMING']['light']):
                return 2  # Keep closed
            else:
                return 1  # Open door


if __name__ == "__main__":
    processor = Processor()
    processor.compute()
