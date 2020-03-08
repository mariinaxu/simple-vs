from datetime import datetime
import pandas as pd

class ExperimentLogger():
    def __init__(self, filename, experiment_id):
        self.filename = filename
        self.log = {}

        self.log['experiment_id'] = experiment_id
        self.log['date_start'] = str(datetime.now())
        self.log['trial_params'] = {}


    def log_exp_start(self, clock_time):
        self.log['experiment_start'] = clock_time


    def log_exp_end(self, clock_time):
        self.log['experiment_end'] = clock_time


    def log_stimulus(self, clock_time, trial_number, stimulus_info):
        self.log['trial_params']['trial_{}'.format(trial_number)] = {}

        self.log['trial_params']['trial_{}'.format(trial_number)]['clock_time'] = clock_time
        self.log['trial_params']['trial_{}'.format(trial_number)]['trial_number'] = trial_number
        self.log['trial_params']['trial_{}'.format(trial_number)]['stimulus_info'] = stimulus_info


    def print_log(self):
        df = pd.DataFrame.from_dict(self.log)
        print(df)