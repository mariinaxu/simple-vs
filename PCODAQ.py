from sys import platform
import socket
from time import sleep, time
import numpy as np


# control NI dacs only on windows
if platform == "win32":
    import nidaqmx as ni


# TODO consider making a BaseDAQ such that one can use the pco system too
class DAQ:
    def __init__(self, experiment_id):
        self.experiment_id = experiment_id

        # TODO make it a yaml settings
        self.ip_address_list = ["172.17.150.202"]
        if platform == "win32":
            self.port = 1001
        else:
            self.port = 10001

        # TODO make into a proper setting????
        self.sampling_rate = 5000
        self.sock = socket.socket(socket.AF_INET,
                                  socket.SOCK_DGRAM)

        self.ni_log_filename = None
        self.data = []

        if platform == "win32":
            self.create_NI_tasks()                        


    def __del__(self):
        if platform == "win32":
            self.ai_log_task.close()


    # TODO make the channels into a settings file somehow...
    def create_NI_tasks(self):
        self.ai_log_task = ni.Task()
        self.ai_log_task.ai_channels.add_ai_voltage_chan("Dev1/ai0:7")
        #self.ai_log_task.ci_channels.add_ci_xx() #TODO
        self.ai_log_task.timing.cfg_samp_clk_timing(rate=self.sampling_rate, sample_mode=ni.constants.AcquisitionType.CONTINUOUS)
        self.ai_log_task.register_every_n_samples_acquired_into_buffer_event(self.sampling_rate, self.data_read_callback)



    def data_read_callback(self, task_handle, every_n_samples_event_type,
                    number_of_samples, callback_data):
        #print('Every N Samples callback invoked.')

        samples = self.ai_log_task.read(number_of_samples_per_channel=self.sampling_rate)
        self.data.append(samples)

        return 0


    def send_message_to_list(self, message):
        message = message.encode()
        for address in self.ip_address_list:
            print(message, address, self.port)
            self.sock.sendto(message, (address, self.port)) 


    def start_cameras(self):
        message1 = "ExpStart {} 1 1".format(self.experiment_id)
        message2 = "BlockStart {} 1 1 1".format(self.experiment_id)

        self.send_message_to_list(message1)
        self.send_message_to_list(message2)


    def stop_cameras(self):
        message1 = "BlockEnd {} 1 1 1".format(self.experiment_id)
        message2 = "ExpEnd {} 1 1".format(self.experiment_id)

        self.send_message_to_list(message1)
        self.send_message_to_list(message2)

    def start_everything(self):
        self.start_logging()
        sleep(1)  
        self.start_cameras()
    
    def stop_everything(self):
        self.stop_cameras()
        print("Waiting additional 3 seconds before stopping logging.")
        sleep(3)
        self.stop_logging()

        self.save_log(self.ni_log_filename)
        self.acquisition_running = False

    def start_logging(self):
        self.ai_log_task.start()


    def stop_logging(self):
        self.ai_log_task.stop()


    def save_log(self, filename):
        self.data = np.asarray(self.data)
        
        np.save(filename, self.data)
        print("Saved NI log (size): ", filename, self.data.shape)