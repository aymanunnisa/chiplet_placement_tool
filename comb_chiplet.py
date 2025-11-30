from comb_router import *
from comb_core import *
from comb_hbm import *
import os
from simulations import *
import numpy as np

#different chiplet combinations generation

def generate_chiplet_side_combinations(chiplet_size, num_i, num_router, mc_per_hbm, group_length, num_cores,num_hbm_per_side, num_chiplet, trace_file_dir, length, breadth):
    combinations = []
    side_chiplet_dir_name = 'side_chiplet_trace_files_' + str(chiplet_size) + '_' + str(length) + '_' + str(breadth)
    os.mkdir(side_chiplet_dir_name)
    os.chdir(side_chiplet_dir_name)

    side_chiplet_counter = 0
    for start in range(chiplet_size - num_router):
        chiplet = [['.' for rows in range(chiplet_size)] for columns in range(chiplet_size)]
        chiplet = place_inputs(chiplet, num_i)  # Place inputs
        chiplet = place_side_routers(chiplet, start, num_router, chiplet_size)  # Place routers
        hbm_combinations = side_hbm_combinations(num_i, chiplet_size, mc_per_hbm * 3, group_length, chiplet,num_hbm_per_side) #place HBMs
        for hbm_chiplet in hbm_combinations:
            core_combinations = generate_core_combination(hbm_chiplet, chiplet_size, num_cores)#place cores
            combinations.extend(core_combinations)

            #trace files
            for combination in core_combinations:
                filename = 'trace_file_side_chiplet_' + str(side_chiplet_counter) + '.txt'
                position_for_trace(combination, filename, num_chiplet, mc_per_hbm, num_hbm_per_side)
                side_chiplet_counter = side_chiplet_counter + 1            
                
    os.chdir('..')
    
    #print('Number of side chiplet combinations is ', str(len(combinations)))
    return combinations, side_chiplet_dir_name

def generate_chiplet_corner_combinations(chiplet_size, num_i, num_router, mc_per_hbm, group_length, num_cores,num_hbm_per_side, num_chiplet, trace_file_dir, length, breadth):
    combinations = []
    corner_chiplet_dir_name = 'corner_chiplet_trace_files_' + str(chiplet_size) + '_' + str(length) + '_' + str(breadth)
    os.mkdir(corner_chiplet_dir_name)
    os.chdir(corner_chiplet_dir_name)

    corner_chiplet_counter = 0

    for start in range(chiplet_size - num_router):
        chiplet = [['.' for rows in range(chiplet_size)] for columns in range(chiplet_size)]
        chiplet = place_inputs(chiplet, num_i)  # Place inputs
        chiplet = place_corner_routers(chiplet, start, num_router, chiplet_size)  # Place routers
        hbm_combinations = corner_hbm_combinations(num_i, chiplet_size, mc_per_hbm * 2, group_length, chiplet,num_hbm_per_side) #place HBMs and 2 is the groups of hbm
        for hbm_chiplet in hbm_combinations:
            core_combinations = generate_core_combination(hbm_chiplet, chiplet_size, num_cores)#place cores
            combinations.extend(core_combinations)

            #trace files
            for combination in core_combinations:
                filename = 'trace_file_corner_chiplet_' + str(corner_chiplet_counter) + '.txt'
                position_for_trace(combination, filename, num_chiplet, mc_per_hbm, num_hbm_per_side)
                corner_chiplet_counter = corner_chiplet_counter + 1
                
    os.chdir('..')
    
    #print('Number of corner chiplet combinations is ', str(len(combinations)))
    return combinations, corner_chiplet_dir_name

def generate_chiplet_periphery_combinations(chiplet_size, num_router,mc_per_hbm, group_length, num_cores,num_hbm_per_side, num_chiplet, trace_file_dir, length, breadth):
    combinations = []
    periphery_chiplet_dir_name = 'periphery_chiplet_trace_files_' + str(chiplet_size) + '_' + str(length) + '_' + str(breadth)
    os.mkdir(periphery_chiplet_dir_name)
    os.chdir(periphery_chiplet_dir_name)

    periphery_chiplet_counter = 0

    for col_start in range(chiplet_size - num_router + 1):
        for row_start in range(chiplet_size - num_router + 1):
            chiplet = [['.' for rows in range(chiplet_size)] for columns in range(chiplet_size)]
            chiplet = place_periphery_routers(chiplet, col_start, row_start, num_router, chiplet_size)  # Place routers
            hbm_combinations = periphery_hbm_combinations(chiplet_size, mc_per_hbm, group_length, chiplet,num_hbm_per_side) #place HBMs
            for hbm_chiplet in hbm_combinations:
                core_combinations = generate_core_combination(hbm_chiplet, chiplet_size, num_cores)#place cores
                combinations.extend(core_combinations)
                
                #trace file
                for combination in core_combinations:
                    filename = 'trace_file_periphery_chiplet_' + str(periphery_chiplet_counter) + '.txt'
                    position_for_trace(combination, filename, num_chiplet, mc_per_hbm, num_hbm_per_side)
                    periphery_chiplet_counter = periphery_chiplet_counter + 1
                
    
    os.chdir('..')
    
    #print('Number of periphery chiplet combinations is ', str(len(combinations)))
    return combinations,periphery_chiplet_dir_name

def generate_chiplet_periphery_combinations_two(chiplet_size, num_router, mc_per_hbm, group_length, num_cores,num_hbm_per_side, num_chiplet, trace_file_dir, length, breadth):
    combinations = []
    periphery_chiplet_two_dir_name = 'periphery_chiplet_two_trace_files_' + str(chiplet_size) + '_' + str(length) + '_' + str(breadth)
    os.mkdir(periphery_chiplet_two_dir_name)
    os.chdir(periphery_chiplet_two_dir_name)

    periphery_chiplet_two_counter = 0

    for col_start in range(chiplet_size - num_router + 1):
        chiplet = [['.' for rows in range(chiplet_size)] for columns in range(chiplet_size)]
        chiplet = place_periphery_routers_two(chiplet, col_start, num_router, chiplet_size)  # Place routers
        hbm_combinations = periphery_hbm_combinations(chiplet_size, mc_per_hbm, group_length, chiplet,num_hbm_per_side) #place HBMs
        for hbm_chiplet in hbm_combinations:
            core_combinations = generate_core_combination(hbm_chiplet, chiplet_size, num_cores)#place cores
            combinations.extend(core_combinations)
            
            #trace file
            for combination in core_combinations:
                filename = 'trace_file_periphery_chiplet_two_' + str(periphery_chiplet_two_counter) + '.txt'
                position_for_trace(combination, filename, num_chiplet, mc_per_hbm, num_hbm_per_side)
                periphery_chiplet_two_counter = periphery_chiplet_two_counter + 1
                
    
    os.chdir('..')
    
    #print('Number of periphery_2  chiplet combinations is ', str(len(combinations)))
    return combinations,periphery_chiplet_two_dir_name

def generate_chiplet_periphery_combinations_one(chiplet_size, num_router, mc_per_hbm, group_length, num_cores,num_hbm_per_side, num_chiplet, trace_file_dir, length, breadth):
    combinations = []
    periphery_chiplet_one_dir_name = 'periphery_chiplet_one_trace_files_' + str(chiplet_size) + '_' + str(length) + '_' + str(breadth)
    os.mkdir(periphery_chiplet_one_dir_name)
    os.chdir(periphery_chiplet_one_dir_name)

    periphery_chiplet_one_counter = 0

    for col_start in range(chiplet_size - num_router + 1):
        chiplet = [['.' for rows in range(chiplet_size)] for columns in range(chiplet_size)]
        chiplet = place_periphery_router_one(chiplet, col_start, num_router, chiplet_size)  # Place routers
        hbm_combinations = periphery_hbm_combinations_one(chiplet_size, mc_per_hbm *2 , group_length, chiplet,num_hbm_per_side) #place HBMs
        for hbm_chiplet in hbm_combinations:
            core_combinations = generate_core_combination(hbm_chiplet, chiplet_size, num_cores)#place cores
            combinations.extend(core_combinations)
            
            #trace file
            for combination in core_combinations:
                filename = 'trace_file_periphery_chiplet_one_' + str(periphery_chiplet_one_counter) + '.txt'
                position_for_trace(combination, filename, num_chiplet, mc_per_hbm, num_hbm_per_side)
                periphery_chiplet_one_counter = periphery_chiplet_one_counter + 1
                
    
    os.chdir('..')
    
    #print('Number of periphery_one chiplet combinations is ', str(len(combinations)))
    return combinations,periphery_chiplet_one_dir_name

 
def generate_chiplet_centre_combinations(chiplet_size, num_router,num_cores, num_chiplet, trace_file_dir, length, breadth, mc_per_hbm, num_hbm_per_side):

    combinations = []
    centre_chiplet_dir_name = 'centre_chiplet_trace_files_' + str(chiplet_size) + '_' + str(length) + '_' + str(breadth)
    os.mkdir(centre_chiplet_dir_name)
    os.chdir(centre_chiplet_dir_name)

    centre_chiplet_counter = 0


    for start in range(1, chiplet_size - num_router):
        chiplet = [['.' for rows in range(chiplet_size)] for columns in range(chiplet_size)]
        chiplet = place_centre_routers(chiplet, start, num_router, chiplet_size)  # Place routers
        core_combinations = generate_core_combination(chiplet, chiplet_size, num_cores)#place cores 
        combinations.extend(core_combinations)
        #generate trace file for centre chiplets
        for combination in core_combinations:
            filename = 'trace_file_centre_chiplet_' + str(centre_chiplet_counter) + '.txt'
            position_for_trace(combination, filename, num_chiplet, mc_per_hbm, num_hbm_per_side)
            centre_chiplet_counter = centre_chiplet_counter + 1
            

    os.chdir('..')
    #print('Number of center chiplet combinations is ', str(len(combinations)))
    return combinations, centre_chiplet_dir_name


#Combinations
def corner_peri_combinatons(corner_combinations, periphery_combinations_two,corner_manhattan_distance,periphery_two_manhattan_distance,num_corner_chiplet,num_periphery_two_chiplet, num_config_cntr, manhattan_distances,num_chiplet, chiplet_size, length, breadth,corner_chiplet_latencies, periphery_chiplet_two_latencies, simulation_latencies):

    for corner_idx, corner_chiplet in enumerate(corner_combinations):
        corner_last_column = corner_chiplet[:,-1]

        for periphery_idx, periphery_chiplet_two in enumerate(periphery_combinations_two):
            periphery_last_column = periphery_chiplet_two[:,-1]
            periphery_last_row = periphery_chiplet_two[-1]
            
            if np.all(corner_last_column == periphery_last_column):
        
                #print('Genrating config with ID: ' + str(num_config_cntr))

                #print("Corner and Periphery_two:")
                #print(str(corner_manhattan_distance[corner_idx]) + " " + str(periphery_two_manhattan_distance[periphery_idx]))
                total_manhattan_distance =(num_corner_chiplet *corner_manhattan_distance[corner_idx]+num_periphery_two_chiplet*periphery_two_manhattan_distance[periphery_idx])
               
                #compute average of average latencies
                average_simulation_latency = (num_corner_chiplet * corner_chiplet_latencies[corner_idx]+num_periphery_two_chiplet*periphery_chiplet_two_latencies[periphery_idx])/(num_corner_chiplet+num_periphery_two_chiplet)

                #create the directory to put the configuration and trace files
                dir_name = str('config_' + str(num_config_cntr))
                os.mkdir(dir_name)
                os.chdir(dir_name)

                config_file = open("configs.txt", "w") 
                config_file.write("Corner and Periphery:")
                config_file.write('\n')
                for row in range(len(corner_chiplet)):
                    config_file.write(' '.join(corner_chiplet[row]) + "    " + ' '.join(periphery_chiplet_two[row]))
                    config_file.write('\n')
                config_file.close()

                manhattan_distances.append(total_manhattan_distance)
                simulation_latencies.append(average_simulation_latency)


                #save the trace file here
                corner_chiplet_trace_file_dir = 'corner_chiplet_trace_files_' + str(chiplet_size) + '_' + str(length) + '_' + str(breadth) 
                periphery_chiplet_two_trace_file_dir = 'periphery_chiplet_two_trace_files_' + str(chiplet_size) + '_' + str(length) + '_' + str(breadth) 

                os.system('cp ../' + corner_chiplet_trace_file_dir + '/trace_file_corner_chiplet_' + str(corner_idx) + '.txt .')
                os.system('cp ../' + periphery_chiplet_two_trace_file_dir + '/trace_file_periphery_chiplet_two_' + str(periphery_idx) + '.txt .')
                
                os.chdir('..')
                
                # increment the counter
                num_config_cntr = num_config_cntr + 1
    return num_config_cntr, manhattan_distances, simulation_latencies

def side_peri_combinations(side_combinations, periphery_combinations_one ,side_manhattan_distance,periphery_one_manhattan_distance,num_side_chiplet,num_periphery_one_chiplet, num_config_cntr, manhattan_distances,num_chiplet, chiplet_size, length, breadth, side_chiplet_latencies, periphery_chiplet_one_latencies, simulation_latencies):    
    for side_idx, side_chiplet in enumerate (side_combinations):
        side_last_column = side_chiplet[:,-1]
  
        for periphery_idx, periphery_chiplet in enumerate(periphery_combinations_one):
            periphery_last_column = periphery_chiplet[:,-1]
            periphery_last_row = periphery_chiplet[-1]
            
            if np.all(side_last_column ==periphery_last_column):
        
                #print('Genrating config with ID: ' + str(num_config_cntr))

                #print("Side and Periphery:")
                #print(str(side_manhattan_distance[side_idx])+" "+str(periphery_one_manhattan_distance[periphery_idx]))
                total_manhattan_distance =(num_side_chiplet *side_manhattan_distance[side_idx]+num_periphery_one_chiplet*periphery_one_manhattan_distance[periphery_idx])

                #compute average of average latencies
                average_simulation_latency = (num_side_chiplet *side_chiplet_latencies[side_idx]+num_periphery_one_chiplet*periphery_chiplet_one_latencies[periphery_idx])/(num_side_chiplet+num_periphery_one_chiplet)

                #create the directory to put the configuration and trace files
                dir_name = str('config_' + str(num_config_cntr))
                os.mkdir(dir_name)
                os.chdir(dir_name)
                
                config_file = open("configs.txt", "w") 
                config_file.write("Side and Periphery:")
                config_file.write('\n')
                for row in range(len(side_chiplet)):
                    config_file.write(' '.join(side_chiplet[row]) + "    " + ' '.join(periphery_chiplet[row]))
                    config_file.write('\n')
                config_file.close()

                manhattan_distances.append(total_manhattan_distance)
                simulation_latencies.append(average_simulation_latency)
                                
                #trace file
                side_chiplet_trace_file_dir = 'side_chiplet_trace_files_' + str(chiplet_size) + '_' + str(length) + '_' + str(breadth) 
                periphery_chiplet_one_trace_file_dir = 'periphery_chiplet_one_trace_files_' + str(chiplet_size) + '_' + str(length) + '_' + str(breadth) 

                os.system('cp ../' + side_chiplet_trace_file_dir + '/trace_file_side_chiplet_' + str(side_idx) + '.txt .')
                os.system('cp ../' + periphery_chiplet_one_trace_file_dir + '/trace_file_periphery_chiplet_one_' + str(periphery_idx) + '.txt .')
                
                os.chdir('..')
                        
                # increment the counter
                num_config_cntr = num_config_cntr + 1
    return num_config_cntr, manhattan_distances, simulation_latencies

def cor_peri_centre_combinations(corner_combinations, periphery_combinations, centre_combinations,corner_manhattan_distance,periphery_manhattan_distance,centre_manhattan_distance,num_corner_chiplet,num_periphery_chiplet,num_centre_chiplet, num_config_cntr, manhattan_distances,num_chiplet, chiplet_size, length, breadth,corner_chiplet_latencies, periphery_chiplet_latencies, centre_chiplet_latencies, simulation_latencies):
    min_config = [[]]
    min_md = 1000000
    for corner_idx, corner_chiplet in enumerate(corner_combinations):
        corner_last_column = corner_chiplet[:,-1]

        for periphery_idx, periphery_chiplet in enumerate(periphery_combinations):
            periphery_last_column = periphery_chiplet[:,-1]
            periphery_last_row = periphery_chiplet[-1]

            if np.all(corner_last_column == periphery_last_column):
                for centre_idx, centre_chiplet in enumerate(centre_combinations):
                    centre_last_row = centre_chiplet[-1]
                    if np.all(periphery_last_row == centre_last_row):
        
                        #print('Genrating config with ID: ' + str(num_config_cntr))

                        #print("Corner , Periphery, and Centre:")
                        #print(str(corner_manhattan_distance[corner_idx]) + " " + str(periphery_manhattan_distance[periphery_idx]) + "  " + str(centre_manhattan_distance[centre_idx]))
                        total_manhattan_distance =(num_corner_chiplet *corner_manhattan_distance[corner_idx]+num_periphery_chiplet*periphery_manhattan_distance[periphery_idx]+num_centre_chiplet *centre_manhattan_distance[centre_idx])
                        if(total_manhattan_distance < min_md):
                          min_md = total_manhattan_distance
                          min_conf = [corner_chiplet,periphery_chiplet,centre_chiplet]
                        average_simulation_latency = (num_corner_chiplet *corner_chiplet_latencies[corner_idx]+num_periphery_chiplet*periphery_chiplet_latencies[periphery_idx] + num_centre_chiplet *centre_manhattan_distance[centre_idx])/(num_corner_chiplet+num_periphery_chiplet+num_centre_chiplet)


                        #directory to put the trace files
                        dir_name = str('config_' + str(num_config_cntr))
                        os.mkdir(dir_name)
                        os.chdir(dir_name)
                        
                        config_file = open("configs.txt", "w") 
                        config_file.write("Corner , Periphery, and Centre:")
                        config_file.write('\n')
                        for row in range(len(corner_chiplet)):
                            config_file.write(' '.join(corner_chiplet[row]) + "    " + ' '.join(periphery_chiplet[row]) + "    " + ' '.join(centre_chiplet[row]))
                            config_file.write('\n')
                        config_file.close()


                        manhattan_distances.append(total_manhattan_distance)
                        simulation_latencies.append(average_simulation_latency)

                        #trace file
                        corner_chiplet_trace_file_dir = 'corner_chiplet_trace_files_' + str(chiplet_size) + '_' + str(length) + '_' + str(breadth) 
                        periphery_chiplet_trace_file_dir = 'periphery_chiplet_trace_files_' + str(chiplet_size) + '_' + str(length) + '_' + str(breadth) 
                        centre_chiplet_trace_file_dir = 'centre_chiplet_trace_files_' + str(chiplet_size) + '_' + str(length) + '_' + str(breadth) 

                        os.system('cp ../' + corner_chiplet_trace_file_dir + '/trace_file_corner_chiplet_' + str(corner_idx) + '.txt .')
                        os.system('cp ../' + periphery_chiplet_trace_file_dir + '/trace_file_periphery_chiplet_' + str(periphery_idx) + '.txt .')
                        os.system('cp ../' + centre_chiplet_trace_file_dir + '/trace_file_centre_chiplet_' + str(centre_idx) + '.txt .')
                
                        os.chdir('..')
                        
                                                
                        # increment the counter
                        num_config_cntr = num_config_cntr + 1
                        

    return min_conf,num_config_cntr, manhattan_distances,simulation_latencies
 
