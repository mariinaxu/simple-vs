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

        # Name of experiment params
        self.exp_protocol = self.exp_parameters['name']

        # Load n trials and timing lengths
        self.n_trials = self.exp_parameters['n_trials']
        self.experiment_delay = self.exp_parameters['experiment_delay']
        self.stim_length = self.exp_parameters['stim_length']
        self.inter_trial_delay = self.exp_parameters['inter_trial_delay']

        # Load the stim parameters
        self.grating_sf = self.exp_parameters['grating_sf']
        self.grating_position = self.exp_parameters['grating_position']
        self.grating_orientations = self.exp_parameters['grating_orientations']
        self.grating_phases_range = self.exp_parameters['grating_phases_range']
        self.grating_size = self.exp_parameters['grating_size']
        self.grating_mask = self.exp_parameters['grating_mask']

        # ps stands for psychopy... 
        self.ps_grating = psychopy.visual.GratingStim(win=self.window, units="deg", pos=self.grating_position, sf=self.grating_sf,
                                                       size=self.grating_size, mask=self.grating_mask)

        # log the experiment parameters
        self.exp_log.log.create_dataset("exp_parameters", data=self.exp_protocol)
        self.exp_log.trial_params_columns = self.exp_parameters['trial_params_columns']
        



    def run_experiment(self, ):
        bool_logged_start = False
        bool_logged_end = False
        # pre experiment delay
        self.clock.reset()
        self.master_clock.reset()
        
        # Half of the experiment delay there is no black square and then we draw it, that's when the experiment starts.
        while self.clock.getTime() < self.experiment_delay:
            if self.clock.getTime() >= self.experiment_delay/2:
                if not bool_logged_start:
                    self.exp_log.log_exp_start(self.master_clock.getTime())
                    bool_logged_start = True
                self.photodiode_square.draw()

            self.window.flip()

        self.absolute_total_time += self.experiment_delay

        for trial in range(self.n_trials):
            print("Trial {} out of {}.".format(trial+1, self.n_trials))
            current_orientation = np.random.choice(self.grating_orientations)
            #current_phase = np.random.randint(self.grating_phases_range[0], self.grating_phases_range[1])

            self.ps_grating.ori = current_orientation
            self.ps_grating.phase = 0


            total_time = 0
            self.clock.reset()

            self.photodiode_square.fillColor = self.photodiode_square.lineColor = self.square_color_on
            # Log stimulus
            # TODO figure out how to dump all the PS grating information easily....
            self.exp_log.log_stimulus(self.master_clock.getTime(), trial, current_orientation, 0)
            while self.clock.getTime() < self.stim_length:
                self.ps_grating.phase = np.mod(self.clock.getTime() / 0.9, 1)

                # log stim ON

                self.ps_grating.draw()
                self.photodiode_square.draw()

                self.window.flip()
            self.photodiode_square.fillColor = self.photodiode_square.lineColor = self.square_color_off

            total_time += self.stim_length


            while self.clock.getTime() < total_time+self.inter_trial_delay:
                self.photodiode_square.draw()
                self.window.flip()

            total_time += self.inter_trial_delay

        # Half of the experiment delay there IS black square and then we stop drawing it, that's when the experiment ends.
        self.clock.reset()
        while self.clock.getTime() < self.experiment_delay:
            if self.clock.getTime() < self.experiment_delay/2:
                self.photodiode_square.draw()
                if not bool_logged_end:
                    self.exp_log.log_exp_end(self.master_clock.getTime(), self.n_trials)
                    bool_logged_end = True
            self.window.flip()

        self.exp_log.save_log()

