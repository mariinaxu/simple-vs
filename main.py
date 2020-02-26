""" Simple example of digital output

    This example outputs the values of data on line 0 to 7
"""

import nidaqmx as ni
import numpy as np


data = np.array([0,1,1,0,1,0,1,0], dtype=np.uint8)

system = ni.system.System.local()

for device in system.devices:
    print(device)

# task = ni.Task()
# task.ai_channels.add_ai_voltage_chan("Dev0/ai1:7")
# task.CreateDOChan("/TestDevice/port0/line2","",PyDAQmx.DAQmx_Val_ChanForAllLines)
# task.StartTask()
# task.WriteDigitalLines(1,1,10.0,PyDAQmx.DAQmx_Val_GroupByChannel,data,None,None)
# task.StopTask()