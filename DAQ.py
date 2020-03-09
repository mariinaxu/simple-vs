from sys import platform
import socket
from time import sleep
import numpy as np

# control NI dacs only on windows
if platform == "win32":
    import nidaqmx as ni


# TODO consider making a BaseDAQ such that one can use the pco system too
class DAQ:
    def __init__(self, experiment_id):
        self.experiment_id = experiment_id

        # TODO make it a yaml settings
        self.ip_address_list = ["172.17.150.226"]
        if platform == "win32":
            self.port = 1001
        else:
            self.port = 10001

        self.sock = socket.socket(socket.AF_INET,
                                  socket.SOCK_DGRAM)

        self.data = []

        if platform == "win32":
            self.create_NI_tasks()                        


    def __del__(self):
        if platform == "win32":
            self.ai_log_task.close()
            self.out_ttl_task.close()
            self.in_ttl_task.close()


    # TODO make the channels into a settings file somehow...
    def create_NI_tasks(self):
        self.ai_log_task = ni.Task()
        self.ai_log_task.ai_channels.add_ai_voltage_chan("Dev1/ai0:7")
        #self.ai_log_task.ci_channels.add_ci_xx() #TODO
        self.ai_log_task.timing.cfg_samp_clk_timing(rate=1000, sample_mode=ni.constants.AcquisitionType.CONTINUOUS)
        self.ai_log_task.register_every_n_samples_acquired_into_buffer_event(1000, self.data_read_callback)

        self.out_ttl_task = ni.Task()
        self.out_ttl_task.do_channels.add_do_chan("Dev1/port0/line1", line_grouping=ni.constants.LineGrouping.CHAN_FOR_ALL_LINES)

        self.in_ttl_task = ni.Task()
        self.in_ttl_task.di_channels.add_di_chan("Dev1/port0/line3", line_grouping=ni.constants.LineGrouping.CHAN_FOR_ALL_LINES)
        self.in_ttl_task.di_channels.add_di_chan("Dev1/port1/line0", line_grouping=ni.constants.LineGrouping.CHAN_FOR_ALL_LINES)    


    def data_read_callback(self, task_handle, every_n_samples_event_type,
                    number_of_samples, callback_data):
        print('Every N Samples callback invoked.')

        samples = self.ai_log_task.read(number_of_samples_per_channel=1000)
        self.data.append(samples)

        return 0


    def send_message_to_list(self, message):
        message = message.encode()
        print(message)
        for address in self.ip_address_list:
            self.sock.sendto(message, (address, self.port)) 


    def start_cameras(self):
        message = "ExpStart {} 1 1".format(self.experiment_id)

        self.send_message_to_list(message)


    def stop_cameras(self):
        message = "ExpEnd {} 1 1".format(self.experiment_id)

        self.send_message_to_list(message)


    # send a high ttl to trigger 2p acquisition
    def start_2p(self):
        self.out_ttl_task.write([True])

        
    def wait_for_2p_aq(self):
        while (not self.in_ttl_task.read()[0]):
            pass
        print(self.in_ttl_task.read())

    
    def stop_2p(self):
        self.out_ttl_task.write([False])


    def start_logging(self):
        self.ai_log_task.start()


    def stop_logging(self):
        self.ai_log_task.stop()


    def save_log(self, filename):
        self.data = np.asarray(self.data)
        np.save(self.data, filename)
        print("Saved NI log: ", filename)


if __name__ == "__main__":
    data = []

    DEBUG = True

    def callback(task_handle, every_n_samples_event_type,
                    number_of_samples, callback_data):
        print('Every N Samples callback invoked.')

        samples = task.read(number_of_samples_per_channel=1000)
        data.append(samples)

        return 0

    # task = ni.Task()
    # task.ai_channels.add_ai_voltage_chan("Dev1/ai0:7")
    # task.timing.cfg_samp_clk_timing(rate=1000, sample_mode=ni.constants.AcquisitionType.CONTINUOUS)
    # task.register_every_n_samples_acquired_into_buffer_event(1000, callback)

    # out_ttl_task = ni.Task()
    # out_ttl_task.do_channels.add_do_chan("Dev1/port0/line1", line_grouping=ni.constants.LineGrouping.CHAN_FOR_ALL_LINES)

    # in_ttl_task = ni.Task()
    # in_ttl_task.di_channels.add_di_chan("Dev1/port0/line3", line_grouping=ni.constants.LineGrouping.CHAN_FOR_ALL_LINES)
    # in_ttl_task.di_channels.add_di_chan("Dev1/port1/line0", line_grouping=ni.constants.LineGrouping.CHAN_FOR_ALL_LINES)

    # start analog input acquisition
    #task.start()
    sleep(1)

    # send ttl to 2p
    #out_ttl_task.write([True])

    # check for 2p acquisition signal:
    # while (not in_ttl_task.read()[0]):
    #     sleep(0.001)
    # print(in_ttl_task.read())

    sleep(5)

    # stop the 2p aq.
    # out_ttl_task.write([False])
    sleep(1)
    data = np.asarray(data)
    print(data.shape)

    #np.save("data-1-1005.npy", data)

    out_ttl_task.close()
    in_ttl_task.close()
    task.close()
    # task = ni.Task()
    # task.ai_channels.add_ai_voltage_chan("Dev0/ai1:7")
    # task.CreateDOChan("/TestDevice/port0/line2","",PyDAQmx.DAQmx_Val_ChanForAllLines)
    # task.StartTask()
    # task.WriteDigitalLines(1,1,10.0,PyDAQmx.DAQmx_Val_GroupByChannel,data,None,None)
    # task.StopTask()
