
import numpy as np

def gen_combination(groups,size):
    if(groups <= size):
        if(size == 1):
           all_combinations = ["."]
           if(groups != 0):
               all_combinations = ["G"]
           return all_combinations   #base case with one position

        all_combinations = []
        combinations_with_G = []
        if(groups >=1):   #recursive call with one less group
            combinations_with_G = gen_combination(groups-1,size-1)

        combinations_without_G = gen_combination(groups,size-1)   #recursive call without G
        for cur_combination in combinations_with_G:
            cur_combination = cur_combination + "G"
            all_combinations.append(cur_combination)
        for cur_combination in combinations_without_G:
            cur_combination = cur_combination + "."
            all_combinations.append(cur_combination)
        return all_combinations
    return []
    
def expand_groups(combinations,group_length):
    expanded_combinations = []
    HBM_group = ''.join(["H"]*group_length)   #string of H for HBM groups

    for group_comb in combinations:
        cur_combination = ""
        for space in group_comb:
            if(space == 'G'):
                cur_combination = cur_combination+HBM_group   #replacing G
            else:
                cur_combination = cur_combination+space
        expanded_combinations.append(list(cur_combination))   #converting string to list
    return expanded_combinations        

def side_hbm_combinations(num_i,chiplet_size,mc_per_hbm,group_length,chiplet,num_hbm_per_side):
    size_first_row = chiplet_size - num_i - 1
    size_col = chiplet_size - 1
    size_last_row = chiplet_size - 2

    side_combinations = []
    size_first_row_with_groups = size_first_row - group_length + num_hbm_per_side
    size_last_row_with_groups = size_last_row - group_length +  num_hbm_per_side 
    size_col_with_groups = size_col - group_length + num_hbm_per_side

    all_comb_first_row = gen_combination(num_hbm_per_side,size_first_row_with_groups)
    all_comb_last_row = gen_combination(num_hbm_per_side, size_last_row_with_groups)
    all_comb_cols = gen_combination(num_hbm_per_side, size_col_with_groups)

    expanded_combinations_first_row = expand_groups(all_comb_first_row, group_length)        
    expanded_combinations_last_row = expand_groups(all_comb_last_row, group_length)
    expanded_combinations_cols = expand_groups(all_comb_cols, group_length)

    for hbm_comb_first_row in expanded_combinations_first_row:
        for hbm_comb_last_row in expanded_combinations_last_row:
            for hbm_comb_col in expanded_combinations_cols:
               
                cur_config = np.array([x[:] for x in chiplet])
                cur_config[0, num_i:chiplet_size - 1] = hbm_comb_first_row
                cur_config[chiplet_size -1, 1:chiplet_size -1] = hbm_comb_last_row
                cur_config[1:chiplet_size, 0] = hbm_comb_col
                side_combinations.append(cur_config)

    return side_combinations

def corner_hbm_combinations(num_i, chiplet_size, mc_per_hbm, group_length, chiplet,num_hbm_per_side):
    size_row = chiplet_size - num_i - 1
    size_col = chiplet_size - 2
    corner_combinations = []
    
    size_row_with_groups = size_row - (num_hbm_per_side * group_length) + num_hbm_per_side
    size_col_with_groups = size_col - (num_hbm_per_side * group_length) + num_hbm_per_side

    all_comb_rows = gen_combination(num_hbm_per_side, size_row_with_groups)
    all_comb_cols = gen_combination(num_hbm_per_side, size_col_with_groups)

    expanded_combinations_row = expand_groups(all_comb_rows, group_length)
    expanded_combinations_cols = expand_groups(all_comb_cols, group_length)

    for hbm_comb_row in expanded_combinations_row:
        for hbm_comb_col in expanded_combinations_cols:
            cur_config = np.array([x[:] for x in chiplet])
            cur_config[0, num_i:chiplet_size - 1] = hbm_comb_row
            cur_config[1:chiplet_size - 1, 0] = hbm_comb_col
            corner_combinations.append(cur_config)
    return corner_combinations

def periphery_hbm_combinations_one(chiplet_size,mc_per_hbm,group_length,chiplet,num_hbm_per_side):
    size_row = chiplet_size - 2
    size_lrow = chiplet_size - 2
    all_combinations = []
    periphery_one_combinations = []

    size_row_with_groups = size_row - (num_hbm_per_side * group_length) + num_hbm_per_side
    size_lrow_with_groups = size_lrow - (num_hbm_per_side * group_length) + num_hbm_per_side

    all_comb_rows = gen_combination(num_hbm_per_side, size_row_with_groups)
    all_comb_lrow = gen_combination(num_hbm_per_side, size_lrow_with_groups)

    expanded_combinations_row = expand_groups(all_comb_rows, group_length)
    expanded_combinations_lrow = expand_groups(all_comb_lrow, group_length)

    for hbm_comb_row in expanded_combinations_row:
        for hbm_comb_lrow in expanded_combinations_lrow:
            cur_config = np.array([x[:] for x in chiplet])
            cur_config[0, 1:chiplet_size - 1] = hbm_comb_row
            cur_config[chiplet_size -1, 1:chiplet_size -1] = hbm_comb_lrow
            periphery_one_combinations.append(cur_config)
    return periphery_one_combinations

def periphery_hbm_combinations(chiplet_size, mc_per_hbm, group_length, chiplet,num_hbm_per_side):
  
    size_row = chiplet_size - 2 - mc_per_hbm + num_hbm_per_side #2 is the number of routers at (0,0)and (0,n-1)
    periphery_combinations = []
    all_comb_rows = gen_combination(num_hbm_per_side, size_row)
    expanded_combinations_row = expand_groups(all_comb_rows, group_length)
    for hbm_comb_row in expanded_combinations_row:
        cur_config = np.array([x[:] for x in chiplet])
        cur_config[0, 1:chiplet_size - 1] = hbm_comb_row
        periphery_combinations.append(cur_config)    
    return periphery_combinations


