from datetime import datetime
from time import time
import h5py
import numpy as np

class ExperimentLogger():
    def __init__(self, filename, experiment_id, mouse_id):
        self.filename = filename
        self.log = h5py.File(filename, 'w')

        self.log.create_dataset('experiment_id', data=experiment_id)
        self.log.create_dataset('mouse_id', data=mouse_id)

        self.log.create_dataset('datetime_start', data=time())
        self.log.create_dataset('datetime_start_str', data=str(datetime.now()))

        self.trial_params = []
        self.trial_params_columns = None




    def log_exp_start(self, clock_time):
        self.log.create_dataset('experiment_start', data=clock_time)


    def log_exp_end(self, clock_time, n_trials):
        self.log.create_dataset('experiment_end', data=clock_time)
        self.log.create_dataset('datetime_end', data=time())
        self.log.create_dataset('datetime_end_str', data=str(datetime.now()))

        # think if it's ok to log this at the end.... seems weird to me.
        self.log.create_dataset('n_trials', data=n_trials)



    def log_stimulus(self, clock_time, trial_number, stimulus_info, stimulus_info_str):
        log_row = []

        log_row.append(trial_number)
        log_row.append(clock_time)
        log_row.append(stimulus_info)
        log_row.append(stimulus_info_str)

        self.trial_params.append(log_row)



    def save_log(self, ni_log=np.zeros([10, 10])):
        self.log.create_dataset("trial_params", data=self.trial_params)
        # self.log.create_group('trial_params')
        # dt = h5py.string_dtype()
        # for name, data in zip(self.trial_params_columns, self.trial_params):
        #     print(type(data))
        #     if type(data) == str:
        #         print(data)
        #         self.log.create_dataset(name, data=data, dtype=dt)
        #     else:
        #         self.log.create_dataset(name, data=data)

        self.log.close()
        print("Saved log:", self.filename)