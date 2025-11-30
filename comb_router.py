#placement of inputs and routers for different chiplets.

def place_inputs(chiplet, num_i):
    for idx_i in range(num_i):
        chiplet[0][idx_i] = 'i' #IO's in the first row
    return chiplet

def place_side_routers(chiplet, col_start, num_router, chiplet_size):
    for idx_r in range((chiplet_size-num_router)//2, (chiplet_size-num_router)//2 + num_router):
        chiplet[idx_r][chiplet_size - 1] = 'R'      #Routers for last column
    return chiplet

def place_corner_routers(chiplet, start, num_router, chiplet_size):
    for idx_r in range(start, start + num_router):
        chiplet[chiplet_size - 1][idx_r] = 'R'   #Routers in the last row
        chiplet[idx_r][chiplet_size - 1] = 'R'   #last column
    return chiplet

def place_periphery_routers(chiplet, col_start, row_start, num_router, chiplet_size):
    for idx_r in range(col_start, col_start + num_router):
        chiplet[idx_r][0] = 'R'   #Routers in the first column
        chiplet[idx_r][chiplet_size - 1] = 'R'   #last column
    for idx in range (row_start, row_start +num_router):
        chiplet[chiplet_size - 1][idx] = 'R'   #Routers in the last row
    return chiplet

def place_periphery_router_one(chiplet,col_start,num_router,chiplet_size):
    for idx_r in range(col_start, col_start + num_router):
        chiplet[idx_r][0] = 'R'   #Routers in the first column
        chiplet[idx_r][chiplet_size - 1] = 'R'   #last column
    return chiplet

def place_periphery_routers_two(chiplet, col_start,num_router, chiplet_size):
    for idx_r in range(col_start, col_start + num_router):
        chiplet[idx_r][0] = 'R'   #Routers in the first column
        chiplet[idx_r][chiplet_size - 1] = 'R'   #last column
    for idx in range((chiplet_size-num_router)//2, (chiplet_size-num_router)//2 + num_router):   
        chiplet[chiplet_size - 1][idx] = 'R'   #last row
    return chiplet

def place_centre_routers(chiplet, start, num_router, chiplet_size):
    for idx_r in range(start, start + num_router):
        chiplet[0][idx_r] = 'R'
        chiplet[chiplet_size - 1][idx_r] = 'R'
        chiplet[idx_r][0] = 'R'
        chiplet[idx_r][chiplet_size - 1] = 'R'
    return chiplet

 
