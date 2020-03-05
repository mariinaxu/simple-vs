""" Simple example of digital output

    This example outputs the values of data on line 0 to 7
"""
from sys import platform
import numpy as np
from time import sleep, time

from SimpleOrientationExperiment import SimpleOrientationExperiment

save_config_file = ""


if __name__ == "__main__":
    exp = SimpleOrientationExperiment("monitor_config.yaml", "save_settings_config.yaml", "base_config.yaml")
    #data_log = NIDAQ_2p(save_config_file)

    exp.load_experiment_config()

    #data_log.start_logging()
    #data_log.trigger_2p()
    #data_log.trigger_cameras()
    #data_log.wait_for_2p_response()

    exp.run_experiment()