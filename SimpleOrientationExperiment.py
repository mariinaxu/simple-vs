from BaseExperiment import BaseExperiment

import psychopy.visual
import psychopy.event
import psychopy.monitors
import numpy as np
import yaml

class SimpleOrientationExperiment(BaseExperiment):
    def load_experiment_config(self, ):
        with open (self.exp_parameters_filename, 'r') as file:
            self.exp_parameters = yaml.load(file, Loader=yaml.FullLoader)

        # Load n trials and timing lengths
        self.n_trials = self.exp_parameters['n_trials']
        self.pre_trial_delay = self.exp_parameters['pre_trial_delay']
        self.stim_length = self.exp_parameters['stim_length']
        self.post_trial_delay = self.exp_parameters['post_trial_delay']

        # Load the stim parameters
        self.grating_sf = self.exp_parameters['grating_sf']
        self.grating_position = self.exp_parameters['grating_position']
        self.grating_orientations = self.exp_parameters['grating_orientations']
        self.grating_phases_range = self.exp_parameters['grating_phases_range']
        self.grating_size = self.exp_parameters['grating_size']
        self.grating_mask = self.exp_parameters['grating_mask']

        # ps stands for psychopy... 
        self.ps_grating = psychopy.visual.GratingStim(win=self.window, units="deg", sf=self.grating_sf,
                                                       size=self.grating_size, mask=self.grating_mask)



    def run_experiment(self, ):
        for trial in range(self.n_trials):
            current_orientation = np.random.choice(self.grating_orientations)
            #current_phase = np.random.randint(self.grating_phases_range[0], self.grating_phases_range[1])

            self.ps_grating.ori = current_orientation
            #self.ps_grating.phase = current_phase

            total_time = 0
            self.clock.reset()

            #pre trial delay
            while self.clock.getTime() < self.pre_trial_delay:
                self.window.flip()

            total_time += self.pre_trial_delay

            while self.clock.getTime() < total_time + self.stim_length:
                self.ps_grating.phase = np.mod(self.clock.getTime() / 0.8, 1)

                self.ps_grating.draw()
                self.window.flip()

            total_time += self.stim_length


            while self.clock.getTime() < self.post_trial_delay:
                self.window.flip()

            total_time += self.post_trial_delay

