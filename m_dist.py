import math
def position(chiplet):
    router_position =[]
    memory_controller_position = []
    core_position =[]

    for row_idx in range(len(chiplet)):
        for col_idx in range(len(chiplet[row_idx])):
            if chiplet[row_idx][col_idx] == 'R':
                router_position.append((row_idx,col_idx))

            elif chiplet[row_idx][col_idx] == 'H':
                memory_controller_position.append((row_idx,col_idx))

            elif chiplet[row_idx][col_idx] == 'C':
                core_position.append((row_idx,col_idx))
    return router_position, memory_controller_position, core_position

def calculate_manhattan_distance(router_position, memory_controller_position, core_position,num_chiplet):
    total_manhattan_distance = 0

    #distance b/w routers and memory controllers
    for router_x, router_y in router_position:
        for mc_x, mc_y in memory_controller_position:
            distance_to_mc = (num_chiplet-1)*(abs(router_x - mc_x) + abs(router_y - mc_y))
            total_manhattan_distance += distance_to_mc 

    # distance b/w routers and cores
    for router_x, router_y in router_position:
        for core_x, core_y in core_position:
            distance_to_core = (num_chiplet-1)*(abs(router_x - core_x) + abs(router_y - core_y))
            total_manhattan_distance += distance_to_core

    # distance b/w cores and memory controllers
    for core_x, core_y in core_position:
        for mc_x, mc_y in memory_controller_position:
            distance_to_mc = abs(core_x - mc_x) + abs(core_y - mc_y)
            total_manhattan_distance += distance_to_mc

    return total_manhattan_distance

#MANHATTAN DISTANCES 
def calculate_side_manhattan_distance(side_chiplet_combinations,num_chiplet):
    side_manhattan_distance =[]
    for chiplet in side_chiplet_combinations:
        router_position, memory_controller_position, core_position= position(chiplet)
        total_manhattan_distance = calculate_manhattan_distance(router_position,memory_controller_position,core_position,num_chiplet)
        side_manhattan_distance.append(total_manhattan_distance)

    return side_manhattan_distance    

def calculate_corner_manhattan_distance(corner_chiplet_combinations,num_chiplet):
    corner_manhattan_distance =[]
    for chiplet in corner_chiplet_combinations:
        router_position,memory_controller_position,core_position = position(chiplet)
        total_manhattan_distance = calculate_manhattan_distance(router_position,memory_controller_position,core_position,num_chiplet)
        corner_manhattan_distance.append(total_manhattan_distance)
    return corner_manhattan_distance

def calculate_periphery_manhattan_distance(periphery_chiplet_combinations,num_chiplet):
    periphery_manhattan_distance =[]
    for chiplet in periphery_chiplet_combinations:
        router_position,memory_controller_position,core_position = position(chiplet)
        total_manhattan_distance = calculate_manhattan_distance(router_position,memory_controller_position,core_position,num_chiplet)
        periphery_manhattan_distance.append(total_manhattan_distance)
    return periphery_manhattan_distance

def calculate_periphery_two_manhattan_distance(periphery_chiplet_combinations_two,num_chiplet):
    periphery_two_manhattan_distance =[]
    for chiplet in periphery_chiplet_combinations_two:
        router_position,memory_controller_position,core_position = position(chiplet)
        total_manhattan_distance = calculate_manhattan_distance(router_position,memory_controller_position,core_position,num_chiplet)
        periphery_two_manhattan_distance.append(total_manhattan_distance)
    return periphery_two_manhattan_distance

def calculate_periphery_one_manhattan_distance(periphery_chiplet_combinations_one,num_chiplet):
    periphery_one_manhattan_distance =[]
    for chiplet in periphery_chiplet_combinations_one:
        router_position,memory_controller_position,core_position = position(chiplet)
        total_manhattan_distance = calculate_manhattan_distance(router_position,memory_controller_position,core_position,num_chiplet)
        periphery_one_manhattan_distance.append(total_manhattan_distance)
    return periphery_one_manhattan_distance

def calculate_centre_manhattan_distance(centre_chiplet_combinations,num_chiplet):
    centre_manhattan_distance =[]
    for chiplet in centre_chiplet_combinations:
        router_position,memory_controller_position,core_position = position(chiplet)
        total_manhattan_distance = calculate_manhattan_distance(router_position,memory_controller_position,core_position,num_chiplet)
        centre_manhattan_distance.append(total_manhattan_distance)
    return centre_manhattan_distance
    