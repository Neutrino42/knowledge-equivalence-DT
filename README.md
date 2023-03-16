# knowledge-equivalence-DT

This repository contains the source code and data that is used in the following paper:

> Nan Zhang, Rami Bahsoon, Nikos Tziritas, and Georgios Theodoropoulos, ‘**Knowledge Equivalence in Digital Twins of Intelligent Systems**’, Apr. 2022. Available: http://arxiv.org/abs/2204.07481
> 
> **Submitted to ACM Transactions on Modeling and Computer Simulation (TOMACS)**

The repository also contains a simulator as a `.jar` file, whose source code can be found in https://github.com/digitwins/mobile-cameras-repast

The directory `output` contains the simulation results. However, due to the storage limitation of GitHub, it now only contains the statistics of the simulation. The raw data of all simulation traces can be found at: https://tinyurl.com/knowledge-equivalence-DT (redirects to Google Drive)


## Run
The experiment was conducted in a conda environment. The required packages are listed in `conda_environment.yml`.

The experiment can be run by executing `./src/runner/Run.py`. All the parameter configurations used in the paper are recorded in `Run.py`.

## Data analysis
The file `analyse.ipynb` contains the code that is used for analysis and figure plotting. It reads the data from the `output` directory and generates the figures that appear in the paper.

