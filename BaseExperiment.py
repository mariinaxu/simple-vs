from abc import ABC, abstractmethod

from DAQ import DAQ
from ExperimentLogger import ExperimentLogger

import psychopy.visual
import psychopy.event
import psychopy.monitors
import yaml
from sys import platform
import os

class BaseExperiment(ABC):
    def __init__(self, experiment_id, mouse_id, daq, monitor_config_filename, save_settings_config_filename, exp_config_filename, debug):
        self.experiment_id = experiment_id
        self.mouse_id = mouse_id
        self.debug = debug

        # the NI daq logging class 
        self.daq = daq

        self.monitor = None
        self.monitor_settings = None
        self.window = None

        self.exp_parameters = None
        self.exp_parameters_filename = exp_config_filename
        
        self.clock = psychopy.core.Clock()
        self.master_clock = psychopy.core.Clock()
        self.absolute_total_time = 0

        self.load_monitor(monitor_config_filename)
        self.load_window()

        self.save_dir = None
        self.experiment_log_filename = None
        self.ni_log_filename = None
        self.create_save_directories(save_settings_config_filename)

        # experiment trial params logger
        self.exp_log = ExperimentLogger(self.experiment_log_filename, self.experiment_id, self.mouse_id) 
        self.daq.ni_log_filename = self.ni_log_filename

        self.create_photodiode_square()



    def __del__(self):
        self.window.close()

    
    def load_monitor(self, monitor_config_filename):
        with open(monitor_config_filename, 'r') as file:
            self.monitor_settings = yaml.load(file, Loader=yaml.FullLoader)
        
        monitor_name = self.monitor_settings['monitor_name']
        monitor_width_pixels = self.monitor_settings['monitor_width_pixels']
        monitor_height_pixels = self.monitor_settings['monitor_height_pixels']
        monitor_width_cm = self.monitor_settings['monitor_width_cm']
        viewing_distance_cm = self.monitor_settings['viewing_distance_cm']
        monitor_gamma = self.monitor_settings['monitor_gamma']



        self.monitor = psychopy.monitors.Monitor(monitor_name, width=monitor_width_cm, distance=viewing_distance_cm, gamma=monitor_gamma)
        self.monitor.setSizePix((monitor_width_pixels, monitor_height_pixels))

        
        # TODO  check if monitor needs to get saved in win
        #mon.save()

    def load_window(self):
        self.window = psychopy.visual.Window(monitor=self.monitor, 
                                            size=(self.monitor_settings['monitor_width_pixels'],
                                                  self.monitor_settings['monitor_height_pixels']),
                                            color='gray',
                                            colorSpace='rgb',
                                            units='deg',
                                            screen=self.monitor_settings['screen_id'],
                                            allowGUI=False,
                                            fullscr=True,
                                            waitBlanking=True)


    def create_photodiode_square(self):
        # Load the settings of the square that goes on the photodiode
        self.square_size = self.monitor_settings['square_size']
        self.square_position = self.monitor_settings['square_position']
        self.square_color_off = self.monitor_settings['square_color_off']
        self.square_color_on = self.monitor_settings['square_color_on']

        # Since 2020 psychopy argument 'color' was deprecated.
        self.photodiode_square = psychopy.visual.Rect(win=self.window, pos=self.square_position, width=self.square_size[0], height=self.square_size[1], 
                                                      units='pix', fillColor=self.square_color_off, lineColor=self.square_color_off)


    def create_save_directories(self, save_settings_config_filename):
        with open(save_settings_config_filename, 'r') as file:
            save_settings = yaml.load(file, Loader=yaml.FullLoader)

        if platform == "win32":
            self.save_dir = os.path.join(save_settings['LABSERVER_DIR_WIN'], self.experiment_id)
        else:
            self.save_dir = os.path.join(save_settings['LABSERVER_DIR_LIN'], self.experiment_id)

        self.data_log_dir = os.path.join(self.save_dir, save_settings['log_folder']) 
        dirs_to_make = save_settings["dirs_to_make"]

        # set the log filenames for the NI log and the exp log
        self.experiment_log_filename = os.path.join(self.data_log_dir, "{}_exp_log.h5".format(self.experiment_id))
        self.ni_log_filename = os.path.join(self.data_log_dir, "{}_ni_log.npy".format(self.experiment_id))


        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        else:
            if not self.debug:
                raise Exception("Experiment ID: {} already exists make new ID...".format(self.experiment_id))

        for dir_to_make in dirs_to_make:
            os.makedirs(os.path.join(self.save_dir, dir_to_make), exist_ok=self.debug)



    def start_data_acquisition(self,):
        if self.daq is None:
            raise Exception("Please set the daq object, it has not been set.")

        if platform == "win32":
            self.daq.start_logging()  
            self.daq.start_2p()
            self.daq.start_cameras()

            if not self.daq.wait_for_2p_aq():
                raise Exception("2-photon microscope did not start acqsuisition...")


    def stop_data_acquisition(self,):
        if platform == "win32":
            self.daq.stop_cameras()
            self.daq.stop_2p()
            self.daq.stop_logging()

            self.daq.save_log(self.ni_log_filename)




    @abstractmethod
    def load_experiment_config(self, ):
        pass

    @abstractmethod
    def run_experiment(self,):
        pass
