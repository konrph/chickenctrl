from modules.mqtt.mqtt import Mqtt_Worker
from threading import Event
from modules.config.config import Config
class MqttRelay:
    def __init__(self):
        self.conf = Config()
        self.last_local = {'topic':None, 'payload':None}
        self.last_public = {'topic':None, 'payload':None}

        self.local = Mqtt_Worker()
        self.public = Mqtt_Worker(broker='127.0.0.1', port=1883)

        self.local_Listener  = Mqtt_Worker(function=self.listen_local,
                                           sub='#')
        self.public_listener = Mqtt_Worker(broker=self.conf.secrets['remoteServer'],
                                           user=self.conf.secrets['remoteUser'],
                                           password=self.conf.secrets['remotePass'],
                                           port=self.conf.secrets['remotePort'],
                                           function=self.listen_public,
                                           sub='#')
        Event().wait()


    def listen_local(self,msg):
        self.last_local = {'topic':msg.topic, 'payload':msg.payload.decode('utf-8')}
        if msg.topic == self.last_public['topic'] and msg.payload.decode('utf-8') == self.last_public['payload']:
            pass
        else:
            self.public.send(topic=msg.topic,payload=msg.payload.decode('utf-8'))

    def listen_public(self,msg):
        self.last_public = {'topic':msg.topic, 'payload':msg.payload.decode('utf-8')}
        if msg.topic == self.last_local['topic'] and msg.payload.decode('utf-8') == self.last_local['payload']:
            pass
        else:
            self.local.send(topic=msg.topic,payload=msg.payload.decode('utf-8'))

MqttRelay()