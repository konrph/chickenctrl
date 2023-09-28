from modules.sensors.sensors import EndSwitch
from modules.engines.engine import Door
import time
switch = EndSwitch()
engine = Door()

time.sleep(5)
intervall = 1
breaker = None
i = 0
engine.close_step()
engine.close_step()
engine.close_step()
engine.close_step()
engine.close_step()

exit(1)



while switch.readHigh() == switch.readLow() and i < 20 and breaker != True:
    if not breaker:
        for i in range(intervall+1):
            engine.close_step()
            if not switch.readHigh() == switch.readLow():
                breaker = True
                break
            time.sleep(0.1)

            print(switch.readHigh(), switch.readLow())
    if not breaker:
        for i in range(intervall):
            engine.open_step()
            if not switch.readHigh() == switch.readLow():
                breaker = True
                break
            time.sleep(0.1)
            print(switch.readHigh(), switch.readLow())
    intervall +=1

print(switch.readHigh(),switch.readLow())

print('position found')

