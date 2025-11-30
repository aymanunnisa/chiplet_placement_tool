from run_booksim import *
from multiprocessing import Pool
from functools import partial

def trace_file_noc(filename, memory_controller_position, core_position, router_position, num_cores, num_mc, num_router, num_chiplet, mc_per_hbm, num_hbm_per_side):
    


    #print('Generating trace file: ' + filename)

    with open(filename, 'w') as file:


        trace = []
        timestamp = 0
        
        # Inputs
        cores = num_cores  # Number of cores
        memory_controller = num_mc # Number of memory controllers
        routers = num_router #Number of routers
        dram_base_latency = 100
        dram_latency_range = 10
        packets_per_read = 4
        packets_per_write = 0

        
        # Initialize packets
        packets_core_to_mc = int(packets_per_read/mc_per_hbm)  # Packets from core to memory controller
        packets_mc_to_core = int(packets_per_write/mc_per_hbm)  # Packets from memory controller to core

        # Generating traces for read
        cur_timestamp = timestamp
        for num_src in range(1, cores + 1):
            timestamp = cur_timestamp
            for num_dest in range(1, memory_controller + 1):
                for num_packet in range(1, packets_core_to_mc + 1):
                    timestamp += 1  # Increment timestamp
                    src_index = core_position[num_src - 1]  # Source index
                    dest_index = memory_controller_position[num_dest - 1]  # Destination index
                    trace.append((src_index, dest_index, timestamp))
       
        packets_core_to_routers = int(packets_core_to_mc * mc_per_hbm * num_hbm_per_side* 2* (num_chiplet-1)/num_router) #HACK:assumed average 2 HBMs per side 
        cur_timestamp = timestamp
        
        for num_src in range(1, cores + 1):
            timestamp = cur_timestamp
            for num_dest in range(1, routers + 1):
                for num_packet in range(1, packets_core_to_routers + 1):
                    timestamp += 1  # Increment timestamp
                    src_index = core_position[num_src - 1]  # Source index
                    dest_index = router_position[num_dest - 1]  # Destination index
                    trace.append((src_index, dest_index, timestamp))

        packets_routers_to_mc = int(packets_core_to_mc*memory_controller*cores*(num_chiplet-1)/num_router) 
        cur_timestamp = 0
        for num_src in range(1, routers + 1):
            timestamp = cur_timestamp
            for num_dest in range(1, num_mc + 1):
                for num_packet in range(1, packets_routers_to_mc + 1):
                    timestamp += 1  # Increment timestamp
                    src_index = router_position[num_src - 1]  # Source index
                    dest_index = memory_controller_position[num_dest - 1]  # Destination index
                    trace.append((src_index, dest_index, timestamp)) 
                    
                    
                    
        # Generating traces for write 
        dram_base_latency = timestamp
        dram_base_latency_copy = timestamp
        for num_src in range(1, memory_controller + 1):
            timestamp = dram_base_latency  # Base latency for DRAM
            for num_dest in range(1, cores + 1):
                for num_packet in range(1, packets_mc_to_core + 1):
                    timestamp += 1  # Increment timestamp
                    src_index = memory_controller_position[num_src - 1]  # Source index
                    dest_index = core_position[num_dest - 1]  # Destination index
                    trace.append((src_index, dest_index, timestamp))
                    
                    
        packets_mc_to_routers = int(packets_mc_to_core * memory_controller *cores*(num_chiplet - 1)/num_router)
        dram_base_latency = timestamp
        for num_src in range(1, memory_controller + 1):
            timestamp = dram_base_latency  # Base latency for DRAM
            for num_dest in range(1, routers + 1):
                for num_packet in range(1, packets_mc_to_routers + 1):
                    timestamp += 1  # Increment timestamp
                    src_index = memory_controller_position[num_src - 1]  # Source index
                    dest_index = router_position[num_dest - 1]  # Destination index
                    trace.append((src_index, dest_index, timestamp))
                    
                    
        packets_routers_to_core = int(packets_mc_to_core * mc_per_hbm * num_hbm_per_side* 2 *(num_chiplet - 1)/num_router) #HACK:assumed average 2 HBMs per side
        for num_src in range(1, routers + 1):
            timestamp = dram_base_latency_copy  # Base latency for DRAM
            for num_dest in range(1, cores + 1):
                for num_packet in range(1, packets_routers_to_core + 1):
                    timestamp += 1  # Increment timestamp
                    src_index = router_position[num_src - 1]  # Source index
                    dest_index = core_position[num_dest - 1]  # Destination index
                    trace.append((src_index, dest_index, timestamp))
        
        # Sort data by timestamp
        sorted_data = sorted(trace, key=lambda x: x[2])

        # Write trace to file
        for entry in sorted_data:
            file.write(f"{entry[0]} {entry[1]} {entry[2]}\n")
    #print(f"Text file '{filename}' generated successfully.")    
    


def get_positions(matrix, char):
    positions = []
    num_rows = len(matrix)
    num_cols = len(matrix[0]) if num_rows > 0 else 0

    for i in range(num_rows):
        for j in range(num_cols):
            if matrix[i][j] == char:
                position = i * num_cols + j
                positions.append(position)

    return positions

def position_for_trace(chiplet,filename,num_chiplet, mc_per_hbm, num_hbm_per_side):

    router_positions = get_positions(chiplet, 'R')
    core_positions = get_positions(chiplet, 'C')
    mc_positions = get_positions(chiplet, 'H')

    num_cores = len(core_positions)
    num_mc = len(mc_positions)
    num_routers = len(router_positions)


    trace_file_noc(filename, mc_positions, core_positions, router_positions, num_cores, num_mc, num_routers, num_chiplet, mc_per_hbm, num_hbm_per_side)
    

def simulate_and_gather_results(chiplet_type_directory, chiplet_size, trace_file_name_prefix):

    trace_files, config_file = process_trace_files(chiplet_type_directory, chiplet_size)
    simulation_latencies = [0]*len(trace_files)

    if (len(trace_files) != 0):
    
        func = partial(run_booksim, chiplet_type_directory, config_file, trace_file_name_prefix)

        #with Pool(128) as p:
            #p.map(func, trace_files)

        #simulation_latencies = gather_simulation_result(chiplet_type_directory)

    #else:
        #simulation_latencies = []

    return simulation_latencies
    
