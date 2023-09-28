from modules.sensors.sensors import EndSwitch
from modules.engines.engine import Door
import time
switch = EndSwitch()
engine = Door()


try:
    while True:
        i=0
        if switch.readHigh() == 1 and switch.readLow() == 0:
            engine.open_step_big()
            while switch.readHigh() != 0:
                #engine.open()
                engine.open_step()
                i += 1
                time.sleep(0.1)
        print(f'{i} Steps for opening')
        time.sleep(5)
        i = 0

        if switch.readHigh() == 0 and switch.readLow() == 1:
            engine.close_step_big()
            while switch.readLow() != 0:
                #engine.close()
                engine.close_step()
                i += 1

            print(f'{i} Steps for closing')

        time.sleep(5)



except KeyboardInterrupt:
    # quit
   engine.stop()