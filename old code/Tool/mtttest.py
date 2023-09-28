from modules.mqtt.mqtt import Mqtt_Worker
import time



def blocker(msg):
    print('starting')
    time.sleep(30)
    print('finishing')


listener_endswitch = Mqtt_Worker(sub='test', function=blocker)
while True:
    time.sleep(1)