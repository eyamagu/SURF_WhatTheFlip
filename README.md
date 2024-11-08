# SURF_WhatTheFlip
Bash scripts to run experiments for the Fixed-Point-Controller, https://github.com/robomorphic/Fixed-Point-Controller

This code assumes that the Fixed-Point-Controller is a sif file that is running on a high-performance computer. To run this code, Fixed-Point-Controller must be configured and made, and then saved as a tar file. If you can run the Fixed Point Controller without accessing an external computer or by sending jobs, ignore fb.sb

fb.sb
- This sbatch file is for submitting a job to a high-performance computer. Once sent, this file will call run.sh to start the simulation process

run.sh
- This script goes to the path which has the folder for all the scripts, runs apptainer to simulate within the sif file, which holds the code from Fixed-Point-Controller

fix.sh
- This script fixes the code files from the Fixed Point Controller so it works on a Linux machine
- Updates the heatmap python file and score python file to the ones in the folder. 
- It also adds the necessary code to manipulate the bits of values that are the fixed point type.

flipbit.sh
- The script for the tests and simulations
- Sets the number of integer bits and fraction bits for the Fixed Point values
- Runs the bit flipped simulation for each integer/frac bits
- Creates a heatmap to show results.
