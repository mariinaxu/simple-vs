from BaseExperiment import BaseExperiment

import psychopy.visual
import psychopy.event
import psychopy.monitors
import numpy as np
import yaml
import pandas as pd

class TextureExperimentFB(BaseExperiment):
    def load_experiment_config(self, ):
        with open (self.exp_parameters_filename, 'r') as file:
            self.exp_parameters = yaml.load(file, Loader=yaml.FullLoader)

        self.images_filename = self.exp_parameters['images_filename']
        self.images_properties_filename = self.exp_parameters['images_properties_filename']
        self.experiment_delay = self.exp_parameters['experiment_delay']

        self.image_size = self.exp_parameters['image_size']
        self.image_position = self.exp_parameters['image_position']
        self.image_mask = self.exp_parameters['image_mask']
        self.image_period = self.exp_parameters['image_period']
        self.image_mask_sd = self.exp_parameters['image_mask_sd']
        
        self.chosen_families = self.exp_parameters['chosen_families']
        self.chosen_subfamilies = self.exp_parameters['chosen_subfamilies']

        self.images = None
        self.n_images = None
        self.image_properties = None
        self.load_images()

        self.experiment_image_indices = []
        self.create_randomization()


        self.image_stim = psychopy.visual.ImageStim(win=self.window, image=None, units="deg", pos=self.image_position,
                                                    size=self.image_size, mask=self.image_mask, maskParams={'sd': self.image_mask_sd})

    def load_images(self):
        print("Loading all images to RAM... ", flush=False)
        self.images = np.load(self.images_filename).astype(np.float32)
        self.n_images = self.images.shape[0]
        self.images -= 128
        self.images /= 128
        print("Done!")

        print("Loading all image properties...", flush=False)
        self.image_properties = pd.read_hdf(self.images_properties_filename)


        # Let's check to make sure we have the same number of textures and noise 
        assert (self.image_properties.iloc[np.where(self.image_properties['stim_type'] == 'texture')[0]].count() == 
                self.image_properties.iloc[np.where(self.image_properties['stim_type'] == 'noise')[0]].count()).all()


    def create_randomization(self):
        noise_start_index = im_df.shape[0]//2

        # DataFrame containing only textures
        tex_df = im_df[:][:noise_start_index]



    def run_experiment(self, ):
        self.experiment_running = True
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

        for i, image in enumerate(self.images):
            print("Image {} out of {}.".format(i+1, self.n_images))



            total_time = 0
            self.clock.reset()

            self.photodiode_square.fillColor = self.photodiode_square.lineColor = self.square_color_on
            # Log stimulus
            # TODO figure out how to dump all the PS grating information easily....
            #self.exp_log.log_stimulus(self.master_clock.getTime(), trial, current_orientation, 0)
            while self.clock.getTime() < self.image_period:

                self.image_stim.image = image

                self.image_stim.draw()

                self.photodiode_square.draw()

                self.window.flip()
            self.photodiode_square.fillColor = self.photodiode_square.lineColor = self.square_color_off


        # Half of the experiment delay there IS black square and then we stop drawing it, that's when the experiment ends.
        self.clock.reset()
        while self.clock.getTime() < self.experiment_delay:
            if self.clock.getTime() < self.experiment_delay/2:
                self.photodiode_square.draw()
            if self.clock.getTime() >= self.experiment_delay/2:
                if not bool_logged_end:
                    self.exp_log.log_exp_end(self.master_clock.getTime(), self.n_trials)
                    bool_logged_end = True
            self.window.flip()

        self.exp_log.save_log()
        self.experiment_running = False

