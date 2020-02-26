""" Simple example of digital output

    This example outputs the values of data on line 0 to 7
"""

import nidaqmx as ni
import numpy as np
from time import sleep, time

data = []

def callback(task_handle, every_n_samples_event_type,
                number_of_samples, callback_data):
    print('Every N Samples callback invoked.')

    samples = task.read(number_of_samples_per_channel=200)
    data.append(samples)

    return 0

task = ni.Task()
task.ai_channels.add_ai_voltage_chan("Dev1/ai1:7")
task.timing.cfg_samp_clk_timing(1000)
task.register_every_n_samples_acquired_into_buffer_event(200, callback)

task.start()

sleep(5)

data = np.asarray(data)
print(data.shape)

task.close()
# task = ni.Task()
# task.ai_channels.add_ai_voltage_chan("Dev0/ai1:7")
# task.CreateDOChan("/TestDevice/port0/line2","",PyDAQmx.DAQmx_Val_ChanForAllLines)
# task.StartTask()
# task.WriteDigitalLines(1,1,10.0,PyDAQmx.DAQmx_Val_GroupByChannel,data,None,None)
# task.StopTask()