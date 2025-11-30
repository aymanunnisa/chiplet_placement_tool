import numpy as np

def generate_core_combination(configuration, chiplet_size, num_cores):
    core_combination = []
    total_spaces = (chiplet_size - 2) * (chiplet_size - 2) - num_cores

    for initial_spaces in range(total_spaces + 1):
        core_comb = ['.'] * initial_spaces + ['C'] * num_cores + ['.'] * (total_spaces - initial_spaces)
        current_core_comb = [row[:] for row in configuration]
        core_ind = 0
        for row_index in range(1, chiplet_size - 1):
            for column_index in range(1, chiplet_size - 1):
                if core_ind < len(core_comb):
                    current_core_comb[row_index][column_index] = core_comb[core_ind]
                    core_ind += 1

        core_combination.append(np.array(current_core_comb))

    return core_combination
