# Import the necessary packages
from modules.mqtt.mqtt import Mqtt_Worker
from consolemenu import *
from consolemenu.items import *



def door(mqtt,payload):
    mqtt.send(topic='/control/door', payload=payload)

def feeder(mqtt,payload):
    mqtt.send(topic='/control/feeder', payload=payload)

def light(mqtt,payload):
    mqtt.send(topic='/control/light', payload=payload)

def relay1(mqtt,payload):
    mqtt.send(topic='/control/relay1', payload=payload)

def relay2(mqtt,payload):
    mqtt.send(topic='/control/relay2', payload=payload)

def ventilation(mqtt,payload):
    mqtt.send(topic='/control/ventilation', payload=payload)

def createEngineMenu(mqtt):
    menu = ConsoleMenu("Door Menu")
    items=[]
    items.append(FunctionItem("Open door", door, [mqtt,1]))
    items.append(FunctionItem("Close door", door, [mqtt,2]))

    for item in items:
        menu.append_item(item)

    return menu

def createFeederMenu(mqtt):
    menu = ConsoleMenu("Door Menu")
    items=[]
    items.append(FunctionItem("Start feeding", feeder, [mqtt,1]))
    items.append(FunctionItem("Stop feeding", feeder, [mqtt,0]))

    for item in items:
        menu.append_item(item)

    return menu

def createLightMenu(mqtt):
    menu = ConsoleMenu("Door Menu")
    items=[]
    items.append(FunctionItem("Light on", light, [mqtt,1]))
    items.append(FunctionItem("Light off", light, [mqtt,0]))

    for item in items:
        menu.append_item(item)

    return menu

def createVentilationMenu(mqtt):
    menu = ConsoleMenu("Ventilation Menu")
    items=[]
    items.append(FunctionItem("Ventilation on", ventilation, [mqtt,1]))
    items.append(FunctionItem("Ventilation off", ventilation, [mqtt,0]))

    for item in items:
        menu.append_item(item)

    return menu

def createRelay1Menu(mqtt):
    menu = ConsoleMenu("Relay1 Menu")
    items=[]
    items.append(FunctionItem("Relay1 on", relay1, [mqtt,1]))
    items.append(FunctionItem("Relay1 off", relay1, [mqtt,0]))

    for item in items:
        menu.append_item(item)

    return menu

def createRelay2Menu(mqtt):
    menu = ConsoleMenu("Relay2 Menu")
    items=[]
    items.append(FunctionItem("Relay2 on", relay2, [mqtt,1]))
    items.append(FunctionItem("Relay2 off", relay2, [mqtt,0]))

    for item in items:
        menu.append_item(item)

    return menu

menu = ConsoleMenu('Main Menu',r"""
ChickenCTRL V.0.0.1

                    ,.
                   (\(\)
   ,_              ;  o >
    {`-.          /  (_)
    `={\`-._____/`   |
     `-{ /    -=`\   |
   .="`={  -= = _/   /`"-.
  (M==M=M==M=M==M==M==M==M)
   \=N=N==N=N==N=N==N=NN=/
    \M==M=M==M=M==M===M=/
     \N=N==N=N==N=NN=N=/
      \M==M==M=M==M==M/
       `-------------'"
""")

mqtt = Mqtt_Worker(broker='127.0.0.1', port=1883)

items = []

items.append(SubmenuItem("Door menu", createEngineMenu(mqtt), menu))
items.append(SubmenuItem("Feeder menu", createFeederMenu(mqtt), menu))
items.append(SubmenuItem("Light menu", createLightMenu(mqtt), menu))
items.append(SubmenuItem("Ventilation menu", createVentilationMenu(mqtt), menu))
items.append(SubmenuItem("Relay1 menu", createRelay1Menu(mqtt), menu))
items.append(SubmenuItem("Relay2 menu", createRelay2Menu(mqtt), menu))
items.append(FunctionItem("DEBUG", print, ["Add code"]))
items.append(FunctionItem("Log", print, ["Add code"]))

for item in items:
    menu.append_item(item)

menu.show()