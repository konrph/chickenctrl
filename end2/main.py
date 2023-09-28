
from modules.sensors.sensors import EndSwitch
t = EndSwitch()
t.readDoorOpen()

while True:
    print(t.readDoorOpen())
    #print(t.readLow())
    print()