""" Simple example of digital output

    This example outputs the values of data on line 0 to 7
"""
from sys import platform
import numpy as np
from time import sleep, time
from datetime import datetime

from DAQ import DAQ
from SimpleOrientationExperiment import SimpleOrientationExperiment

bool_DEBUG = True

def create_experiment_name():
    if not bool_DEBUG:
        experiment_id = input("Enter Experiment name: (MXXXX_XXXXX_XX): ")
    else:
        # when debugging we make a fake tag 
        now = datetime.now()
        date = str(now).split(" ")[0].replace("-", "")[2:]
        experiment_id = "M{}_12345_FB".format(date)

    return experiment_id


if __name__ == "__main__":
    experiment_id = create_experiment_name()
    data_aq = DAQ(experiment_id)

    exp = SimpleOrientationExperiment(experiment_id, data_aq, "monitor_config.yaml", "save_settings_config.yaml", "simple_orientation_config.yaml", debug=bool_DEBUG)

    exp.load_experiment_config()
    exp.start_data_acquisition()

    exp.run_experiment()

    exp.stop_data_acquisition()