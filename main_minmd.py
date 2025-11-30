import numpy as np 
import math
from datetime import datetime
import os
from run_booksim import *
from simulations import *
from comb_chiplet import *
from m_dist import *
from utility import *
import sys
import yaml
from result import *

# Function to print chiplet combinations
def print_combinations(combinations, chiplet_type,manhattan_distance, num_config_cntr, num_chiplet, trace_file_directory_to_look_up):
    for idx,chiplet in enumerate(combinations):

        #print('Genrating config with ID: ' + str(num_config_cntr))

        #print(f"{chiplet_type} chiplet:")
        #print(f"manhattan_distance: ",manhattan_distance[idx])

        #create the directory to put the trace files
        dir_name = str('config_' + str(num_config_cntr))
        os.mkdir(dir_name)
        os.chdir(dir_name)
        
        config_file = open("configs.txt", "w") 
        config_file.write(chiplet_type)
        config_file.write('\n')
        for row in chiplet:
            config_file.write(' '.join(row))
            config_file.write('\n')
        config_file.close()
  
        os.system('cp ../' + trace_file_directory_to_look_up + '/trace_file_' + chiplet_type + '_chiplet_' + str(idx) + '.txt .')

        os.chdir('..')
                
        # increment the counter
        num_config_cntr = num_config_cntr + 1

    return num_config_cntr
       
# Main function for chiplet placement

#def chip_placement(num_router, num_cores, mc_per_hbm, num_i,num_chiplets_per_chip,is_size_even = false):
def chip_placement(num_router, num_cores, mc_per_hbm, num_hbm_per_side, num_i,num_chiplet,simulate_flag):
    Total = num_router + num_cores + mc_per_hbm + num_i    #all the components present in the chiplet
    chiplet_size = math.ceil(math.sqrt(Total))    
    chiplet_size = max(chiplet_size,num_i+mc_per_hbm+1)  # place for hbm placement
    group_length = 4                       # each hbm has four mesh stops for memory controllers
    total_groups = mc_per_hbm // group_length         
    factor_pairs = factors(num_chiplet)
   
    # create a directory for trace file
    date_time = datetime.now()
    date_time_string = date_time.strftime("%d_%m_%Y_%H_%M_%S")
    dir_name = 'trace_files_' + date_time_string
    os.mkdir(dir_name)
    os.chdir(dir_name)


    # counter to hold all configs
    num_config_cntr = 0
    min_conf = None

    # variable to hold all manhattan distances
    manhattan_distances = []

    # variable to hold all simulation latencies
    simulation_latencies = []
    side_chiplet_latencies = []
    periphery_chiplet_one_latencies = []
    periphery_chiplet_two_latencies = []
    corner_chiplet_latencies = []
    

    count_corner = 0 
    for cur_factor_pair in factor_pairs:
    
        length = cur_factor_pair[0]
        breadth = cur_factor_pair[1]
        while True:
            Chiplet_matrix = chiplet_size * chiplet_size

            if Chiplet_matrix >= Total:
                if (chiplet_size - 2) * (chiplet_size - 2) >= num_cores:    #cores are inside the boundaries
                    if (chiplet_size % 2 == 0): #HACK:even sized chiplet for all configurations
                        if ((chiplet_size - 2) >= (total_groups - (chiplet_size - 1 - num_i) // group_length) * group_length):  #total groups to fit in the chiplet  
                        # if ((length != 2 and breadth != 2) and (chiplet_size % 2 != 0 )):
                            manhattan_distance = []

                            '''#SIDE CHIPLET
                            side_chiplet_combinations, side_chiplet_dir = generate_chiplet_side_combinations(chiplet_size, num_i, num_router, mc_per_hbm,group_length,num_cores,num_hbm_per_side, num_chiplet, dir_name, length, breadth)
                            side_manhattan_distance = calculate_side_manhattan_distance(side_chiplet_combinations,num_chiplet)

                            #simulate the trace for side chiplets
                            side_chiplet_latencies = simulate_and_gather_results(side_chiplet_dir_name, chiplet_size, 'trace_file_side_chiplet_')
                            
                        
                            #PERIPHERY CHIPLET FOR 1*n
                            periphery_chiplet_combinations_one, periphery_chiplet_one_dir_name = generate_chiplet_periphery_combinations_one(chiplet_size, num_router,mc_per_hbm,group_length,num_cores,num_hbm_per_side, num_chiplet, dir_name, length, breadth)
                            periphery_one_manhattan_distance = calculate_periphery_one_manhattan_distance(periphery_chiplet_combinations_one,num_chiplet)
                            
                            #simulate the trace for periphery one chiplets
                            periphery_chiplet_one_latencies = simulate_and_gather_results(periphery_chiplet_one_dir_name, chiplet_size, 'trace_file_periphery_chiplet_one_')
                            

                            #PERIPHERY CHIPLET FOR 2*n
                            periphery_chiplet_combinations_two, periphery_chiplet_two_dir_name = generate_chiplet_periphery_combinations_two(chiplet_size, num_router,mc_per_hbm,group_length,num_cores,num_hbm_per_side, num_chiplet, dir_name, length, breadth)
                            periphery_two_manhattan_distance = calculate_periphery_two_manhattan_distance(periphery_chiplet_combinations_two,num_chiplet)
                            
                            #simulate the trace for periphery two chiplets
                            periphery_chiplet_two_latencies = simulate_and_gather_results(periphery_chiplet_two_dir_name, chiplet_size, 'trace_file_periphery_chiplet_two_')'''
                            
                            #CORNER CHIPLET                                             
                            corner_chiplet_combinations, corner_chiplet_dir_name = generate_chiplet_corner_combinations(chiplet_size, num_i, num_router,mc_per_hbm,group_length,num_cores,num_hbm_per_side, num_chiplet, dir_name, length, breadth)
                            #corner_chiplet_dir_name = '../trace_files_31_10_2024_10_59_39/corner_chiplet_trace_files_8_3_3'
                            corner_manhattan_distance = calculate_corner_manhattan_distance(corner_chiplet_combinations,num_chiplet)

                            #simulate the trace for corner chiplets
                            if(simulate_flag):
                              corner_chiplet_latencies = simulate_and_gather_results(corner_chiplet_dir_name, chiplet_size, 'trace_file_corner_chiplet_')
                            
                            ##PERIPHERY CHIPLET FOR n*m
                            #periphery_chiplet_combinations, periphery_chiplet_dir_name = generate_chiplet_periphery_combinations(chiplet_size, num_router,mc_per_hbm,group_length,num_cores,num_hbm_per_side, num_chiplet, dir_name, length, breadth)
                            ##periphery_chiplet_dir_name = '../trace_files_31_10_2024_10_59_39/periphery_chiplet_trace_files_8_3_3/'                   
                            #periphery_manhattan_distance = calculate_periphery_manhattan_distance(periphery_chiplet_combinations,num_chiplet)                          
                            #
                            ##simulate the trace for periphery chiplets
                            #periphery_chiplet_latencies = simulate_and_gather_results(periphery_chiplet_dir_name, chiplet_size, 'trace_file_periphery_chiplet_')
                            #
                            ##CENTRE CHIPLET                            
                            #centre_chiplet_combinations, centre_chiplet_dir_name = generate_chiplet_centre_combinations(chiplet_size, num_router,num_cores, num_chiplet, dir_name, length, breadth, mc_per_hbm, num_hbm_per_side)
                            ##centre_chiplet_dir_name = '../trace_files_31_10_2024_10_59_39/centre_chiplet_trace_files_8_3_3'
                            #centre_manhattan_distance = calculate_centre_manhattan_distance(centre_chiplet_combinations,num_chiplet)

                            ##simulate the trace for corner chiplets
                            #centre_chiplet_latencies = simulate_and_gather_results(centre_chiplet_dir_name, chiplet_size, 'trace_file_centre_chiplet_')
                            
                            #LAYOUT
                              
                            #if prime(num_chiplet):
                            if num_chiplet ==2:


                                num_config_cntr = print_combinations(side_chiplet_combinations, "side",side_manhattan_distance, num_config_cntr, num_chiplet, 'side_chiplet_trace_files_'+str(chiplet_size) + '_' + str(length) + '_' + str(breadth))
                                manhattan_distances.extend(side_manhattan_distance)
                                simulation_latencies.extend(side_chiplet_latencies)
                                #find argmin of manhattan distances
                                min_md = min(manhattan_distances)
                                min_md_idx = manhattan_distances.index(min_md)
                                #find configuration with that index
                                min_conf = [side_chiplet_combinations[min_md_idx]]
                                

                            elif num_chiplet==4:
                                if (length != 1 and breadth != 1):
                                    #Generate corner combinations
                                    num_config_cntr = print_combinations(corner_chiplet_combinations, "corner",corner_manhattan_distance, num_config_cntr, num_chiplet, 'corner_chiplet_trace_files_'+str(chiplet_size) + '_' + str(length) + '_' + str(breadth))
                                    manhattan_distances.extend(corner_manhattan_distance)
                                    simulation_latencies.extend(corner_chiplet_latencies)
                                    #Generate combinations for 1x4
                                    #find argmin of manhattan distances
                                    min_md = min(manhattan_distances)
                                    min_md_idx = manhattan_distances.index(min_md)
                                    #find configuration with that index
                                    min_conf = [corner_chiplet_combinations[min_md_idx]]
                                    
                            else:
                                #COMBINATIONS FOR n*m CORNER PERIPHERY AND CENTRE
                                num_corner_chiplet, num_periphery_chiplet, num_centre_chiplet = calculate_cor_peri_centre(num_chiplet,length,breadth)
                                min_conf,num_config_cntr, manhattan_distances,simulation_latencies = cor_peri_centre_combinations(corner_chiplet_combinations, periphery_chiplet_combinations, centre_chiplet_combinations,corner_manhattan_distance,periphery_manhattan_distance,centre_manhattan_distance,num_corner_chiplet,num_periphery_chiplet,num_centre_chiplet, num_config_cntr, manhattan_distances,num_chiplet, chiplet_size, length, breadth,corner_chiplet_latencies, periphery_chiplet_latencies, centre_chiplet_latencies, simulate_latencies)
                            
                        if(simulate_flag == 0):
                            print(min_conf)               
                        break    
            chiplet_size += 1

    # number of configurations should be equal to number of entries to the manhattan distance list
    if (len(manhattan_distances) != num_config_cntr):
        assert(0)

    with open("manhattan_distances.txt", "w") as f:
        for distance in manhattan_distances:
            f.write(str(distance) +"\n")


    with open("avg_latencies.txt", "w") as f:
        for latency in simulation_latencies:
            f.write(str(latency) +"\n")

    # get out of trace file directory
    os.chdir('..')
    return dir_name


def main(simulate_flag):
    with open("config.yml", "r") as file:
        config = yaml.safe_load(file)

    chip_config = config["chip_placement"]
    
    dir_name = chip_placement(
        num_router = chip_config["num_router"],
        num_cores = chip_config["num_cores"],
        mc_per_hbm = chip_config["mc_per_hbm"],
        num_hbm_per_side = chip_config["num_hbm_per_side"],
        num_i = chip_config["num_i"],
        num_chiplet = chip_config["num_chiplet"],
        simulate_flag = 0
        )

if __name__ == "__main__":
    #Ask user if he wants simulate or not
    simulate_flag = 0
    if(len(sys.argv)> 1 and sys.argv[1] == "simulate"):
        simulate_flag = 1
    main(simulate_flag)
