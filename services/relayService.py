import time
from modules.mqtt.mqtt import Mqtt_Worker
from modules.relays.relays import *
from threading import Event
from modules.config.config import Config

ventilation = Ventilation()
light = Light()
relay1 = Relay1()
relay2 = Relay2()

def run_ventilation(msg):
    id = msg.payload.decode('utf-8')
    if id == '1':
        ventilation.start()
    if id == '0':
        ventilation.stop()

def run_light(msg):
    id = msg.payload.decode('utf-8')
    if id == '1':
        light.on()
    if id == '0':
        light.off()

def run_relay1(msg):
    id = msg.payload.decode('utf-8')
    if id == '1':
        relay1.start()
    if id == '0':
        relay1.stop()

def run_relay2(msg):
    id = msg.payload.decode('utf-8')
    if id == '1':
        relay2.start()
    if id == '0':
        relay2.stop()

def main():
    config = Config()
    Mqtt_Worker(broker=config.secrets['localServer'], port=config.secrets['localPort'], function=run_ventilation, sub='/control/ventilation')
    Mqtt_Worker(broker=config.secrets['localServer'], port=config.secrets['localPort'], function=run_light, sub='/control/light')
    Mqtt_Worker(broker=config.secrets['localServer'], port=config.secrets['localPort'], function=run_relay1, sub='/control/relay1')
    Mqtt_Worker(broker=config.secrets['localServer'], port=config.secrets['localPort'], function=run_relay2, sub='/control/relay2')
    Event().wait()

if __name__ == "__main__":
    main()
