# simple-VS

A comprehensive visual stimulus presentation system for neuroscience experiments, designed to coordinate visual stimulation with various data acquisition devices.

## Overview
This system enables precise control and synchronization of:
- Visual stimulus presentation on calibrated displays
- Two-photon microscope triggering
- Eye-tracking camera control
- Body-tracking camera control
- TTL signal collection for post-hoc data synchronization

## Installation
1. Clone the repository:
   ```bash
   git clone [repository-url]
   ```

2. Create and activate a conda environment using the provided environment file:
   ```bash
   conda env create -f simple-vs_env.yaml
   conda activate simple-vs
   ```

3. Hardware setup:
   - Connect your National Instruments/PCO DAQ device
   - Configure your display monitor
   - Connect your tracking cameras and microscope triggers

## Features
- Multiple experiment paradigms:
  - Retinotopy mapping
  - Texture analysis
  - Locally sparse noise
  - Dynamic battery
  - Simple orientation
  - Custom experiments via extensible base classes
- Flexible configuration via YAML files for:
  - Monitor settings and calibration
  - Experiment parameters
  - Data saving preferences
- Robust data acquisition (DAQ) support:
  - National Instruments
  - PCO
  - Other DAQ systems via extensible interfaces

## Dependencies
* psychopy - Visual stimulus presentation
* nidaqmx - National Instruments DAQ interface
* numpy - Numerical computations
* pyaml - Configuration file parsing
* h5py - Data storage
* pandas - Data analysis and logging

## Project Structure
- `BaseExperiment.py` - Core experiment infrastructure
- `*Experiment.py` files - Specific experiment implementations
- `*DAQ.py` files - Data acquisition interfaces
- `*_config.yaml` files - Configuration templates

## Usage
1. Configure your experiment parameters in the appropriate YAML file
2. Set up your monitor configuration in `monitor_config.yaml`
3. Configure data saving preferences in `save_settings_config.yaml`
4. Run your experiment using the corresponding runner script (e.g., `run_TEX_experiment.py`)

### Example Usage

#### Running a Texture Experiment
1. Edit `texture_FB-VGG_config.yaml` to set your desired parameters:
   ```yaml
   name: texture_FB-VGG
   experiment_delay: 5
   # ... other parameters
   ```

2. In `main.py`, uncomment the desired experiment (current manual selection process):
   ```python
   # Comment out other experiments and uncomment:
   experiment = TextureExperimentFBVGG(
       experiment_id=experiment_id,
       mouse_id=mouse_id,
       daq=daq,
       monitor_config_filename='monitor_config.yaml',
       save_settings_config_filename='save_settings_config.yaml',
       exp_config_filename='texture_FB-VGG_config.yaml',
       debug=bool_DEBUG
   )
   ```

3. Run the experiment:
   ```bash
   python main.py
   ```

#### Running a Retinotopy Experiment
1. Configure `retinotopy_config.yaml`
2. In `main.py`, uncomment the RetinotopyExperiment section
3. Run:
   ```bash
   python main.py
   ```

Note: The current experiment selection process requires manually editing `main.py` to uncomment the desired experiment. Future versions may implement a command-line argument or configuration-based selection system.

## Contributing
This project is maintained by the Visual Neuroscience Group at UBC. For questions or contributions, please contact the repository maintainers.
