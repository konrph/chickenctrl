import paho.mqtt.client as mqtt
import traceback
class Mqtt_Worker:
    def __init__(self,broker='127.0.0.1',port='1883',user=None,password=None,function=None,sub=None,qos=0,clean_session=True):

        self.clean_session = clean_session
        self.client = mqtt.Client(clean_session=self.clean_session)
        self.broker = broker
        self.user=user
        self.password = password
        self.qos=qos
        self.port=port
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

        self.subscription=sub
        self.func = function

        self.msg=''
        self.error=''

        self.first_connect()

    def on_connect(self,client, userdata, flags, rc):
        if self.subscription != None:
            client.subscribe(topic=self.subscription, qos=int(self.qos))
        #print("Connected to Server")

    def on_disconnect(self,client, userdata, rc):
        #print('Disconnected form Server')
        pass

    def send(self,topic,payload,qos=0,retain=False):
        try:
            self.client.publish(topic=topic, payload=str(payload), qos=int(qos),retain=bool(retain))
        except:
            traceback.print_exc()
            quit(0)

    def first_connect(self):
        while self.error!=False:
            if self.user and self.password:
                try:
                    self.client.tls_set()
                    self.client.username_pw_set(username=self.user, password=self.password)
                    self.client.connect(self.broker, int(self.port), 60)
                    self.error = False
                except:
                    self.error = True

            else:
                try:
                    self.client.connect(self.broker, int(self.port), 60)
                    self.error=False
                except Exception as e:
                    self.error=True
        self.client.loop_start()

    def on_message(self,client, userdata, msg):
        self.msg=msg
        if self.func !=None:
            try:
                self.func(msg)
            except:
                traceback.print_exc()
                quit(0)




