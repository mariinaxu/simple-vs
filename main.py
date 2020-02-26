""" Simple example of digital output

    This example outputs the values of data on line 0 to 7
"""

import nidaqmx as ni
import numpy as np
from time import sleep, time




task = ni.Task()
task.ai_channels.add_ai_voltage_chan("Dev1/ai1:7")
task.timing.cfg_samp_clk_timing(1000)
task.start()

sleep(5)

data = task.read()


print(data)
print(type(data))

task.close()
# task = ni.Task()
# task.ai_channels.add_ai_voltage_chan("Dev0/ai1:7")
# task.CreateDOChan("/TestDevice/port0/line2","",PyDAQmx.DAQmx_Val_ChanForAllLines)
# task.StartTask()
# task.WriteDigitalLines(1,1,10.0,PyDAQmx.DAQmx_Val_GroupByChannel,data,None,None)
# task.StopTask()