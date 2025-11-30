						# All Chiplet Configurations

## Description

This Python-based tool performs placement of Processing Elements (PEs) within chiplets for 2.5D systems, optimizing for performance and cost under realistic physical design constraints. The placement strategy involves exploring valid PE arrangements to minimize communication cost and it supports fast design space exploration.

## Repository Structure

```text
**File / Folder**		          **Description**

main.py		  	  Main script to generate configurations and trace files.

comb_chiplet.py    	  Logic to generate all possible chiplet combinations.

comb_core.py	   	  Core placement logic.

comb_hbm.py	   	  High Bandwidth Memory (HBM) placement logic.

comb_router.py	   	  Router placement logic.

m_dist.py	  	  Manhattan distance calculation.

simulations.py	   	  Functions to run simulations for generated configurations.

run_booksim.py	   	  Interface to run BookSim with generated configuration files.

utility.py	  	  Helper functions for file handling and configuration generation.

config.yml	   	  YAML configuration file for specifying system parameters.

booksim/	   	  		 Contains BookSim-related files (config templates, etc.).

mesh_config_trace_based/  Configuration files for trace-based mesh simulations.

## Installation

1. Install dependencies:

	```bash
		pip install -r requirements.txt
	```
##Usage

Run the main generator: 

	```bash
		Run the main generator: 
   python3 main.py simulate (performs the simulation): Performs cycle accurate simulation, hence slow 
   python3 main.py (prints minimum configuration): Proposed fast and accurate design space exploration
	```

##Configuration

The parameters for chiplet arrangement (grid size, number of cores, routers, HBMs, etc.) can be set in: config.yml
 
- `num_router = Total number of routers to be distributed across all chiplets for enabling on-package communication.`
- `num_cores = Total number of compute cores (PEs) to be placed across chiplets.`
- `mc_per_hbm = Each High Bandwidth Memory (HBM) interface connects to this many Memory Controllers (MCs).`
- `num_hbm_per_side = Number of HBM stacks per side of the interposer/package (used to determine memory interface layout).`
- `num_i = Number of I/O ports or interfaces (e.g., for chiplet-to-chiplet or chiplet-to-package communication).`
- `num_chiplet = Total number of chiplets in the 2.5D system to place the cores, routers, and MCs into.`

##Outputs

The scripts generate:

If simulate flag = 0:

The minimum Manhattan distance that is the best configuration and its configurations

otherwise, 
 Configuration directories 


