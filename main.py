""" Simple example of digital output

    This example outputs the values of data on line 0 to 7
"""
from sys import platform
import numpy as np
from time import sleep, time
from datetime import datetime

from NISDAQ import NISDAQ
from PCODAQ import PCODAQ

from SimpleOrientationExperiment import SimpleOrientationExperiment
from TextureExperimentFB import TextureExperimentFB
from TextureExperimentFBVGG import TextureExperimentFBVGG
from TextureExperimentFBVGGMultiTime import TextureExperimentFBVGGMultiTime
from DynamicBatteryExperiment import  DynamicBatteryExperiment

bool_DEBUG = True

def create_experiment_name():
    if not bool_DEBUG:
        experiment_id = input("Enter Experiment name: (MXXXX_XXXXX_XX): ")
        mouse_id = input("Enter mouse ID (XXXXX): ")
    else:
        # when debugging we make a fake tag 
        now = datetime.now()
        date = str(now).split(" ")[0].replace("-", "")[2:]
        experiment_id = "M{}_123411_FB".format(date)

        mouse_id = "12345"

    return experiment_id, mouse_id


if __name__ == "__main__":
    try:
        experiment_id, mouse_id = create_experiment_name()
        # change the line below to use PCO or NIS (2p)
        #data_aq = NISDAQ(experiment_id)
        data_aq = PCODAQ(experiment_id)
        #exp = DynamicBatteryExperiment(experiment_id, mouse_id, data_aq, "monitor_config.yaml", "save_settings_config.yaml", "dynamic_battery_config.yaml", debug=bool_DEBUG)
        #exp = SimpleOrientationExperiment(experiment_id, mouse_id, data_aq, "monitor_config.yaml", "save_settings_config.yaml", "simple_orientation_config.yaml", debug=bool_DEBUG)
        exp = TextureExperimentFBVGG(experiment_id, mouse_id, data_aq, "monitor_config.yaml", "save_settings_config.yaml", "texture_FB-VGG_config.yaml", debug=bool_DEBUG)
        #exp = TextureExperimentFBVGGMultiTime(experiment_id, mouse_id, data_aq, "monitor_config.yaml", "save_settings_config.yaml", "texture_FB-VGGMultiTime_config.yaml", debug=bool_DEBUG)

        exp.load_experiment_config()
        exp.start_data_acquisition()

        exp.run_experiment()

        exp.stop_data_acquisition()

        print("ALL DONE with experiment {}! ".format(experiment_id))
    except KeyboardInterrupt:
        print("Received CTRL-C event")
        if exp.experiment_running:
            # We need to run the stopping functions.
            pass
        if exp.acquisition_running:
            exp.stop_data_acquisition()
    finally:
        del exp.data_aq

