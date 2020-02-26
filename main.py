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

    samples = task.read(number_of_samples_per_channel=1000)
    data.append(samples)

    return 0

task = ni.Task()
task.ai_channels.add_ai_voltage_chan("Dev1/ai0:7")
task.timing.cfg_samp_clk_timing(rate=1000, sample_mode=ni.constants.AcquisitionType.CONTINUOUS)
task.register_every_n_samples_acquired_into_buffer_event(1000, callback)

ttl_task = ni.Task()
ttl_task.do_channels.add_do_chan("Dev1/port0/line1", line_grouping=ni.constants.LineGrouping.CHAN_FOR_ALL_LINES)

# start analog input acquisition
task.start()
sleep(1)
ttl_task.write([True])
# send ttl to 2p
sleep(15)
ttl_task.write([False])
sleep(1)
data = np.asarray(data)
print(data.shape)

np.save("data-1-1005.npy", data)

ttl_task.close()
task.close()
# task = ni.Task()
# task.ai_channels.add_ai_voltage_chan("Dev0/ai1:7")
# task.CreateDOChan("/TestDevice/port0/line2","",PyDAQmx.DAQmx_Val_ChanForAllLines)
# task.StartTask()
# task.WriteDigitalLines(1,1,10.0,PyDAQmx.DAQmx_Val_GroupByChannel,data,None,None)
# task.StopTask()
