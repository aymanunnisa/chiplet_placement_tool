import math
#FACTORS OF num chiplet for chip layout
def factors(num_chiplet):
    factor_pairs = []
    for num in range(1,(int (num_chiplet**0.5)+1)):
        if num_chiplet % num == 0:
            factor_pairs.append([num,num_chiplet//num])
    return factor_pairs
                        
#1:Prime or not
def prime(num_chiplet):
    if num_chiplet <= 1:
        return False
    for i in range(2, int(math.sqrt(num_chiplet)) + 1):
        if num_chiplet % i == 0:
            return False
    return True 
    
#2:Even or not
def even(num_chiplet):
    if num_chiplet>2:
        return num_chiplet % 2 == 0
    
def calculate_side_peri(num_chiplet):
    num_side_chiplet = 2
    num_periphery_one_chiplet = num_chiplet - num_side_chiplet
    return num_side_chiplet,num_periphery_one_chiplet

def calculate_corner_peri(num_chiplet):
    num_corner_chiplet = 4
    num_periphery_two_chiplet = num_chiplet - num_corner_chiplet
    return num_corner_chiplet,num_periphery_two_chiplet

def calculate_cor_peri_centre(num_chiplet,length,breadth):
    num_corner_chiplet = 4
    num_periphery_chiplet = 2*(length+breadth)-num_corner_chiplet
    num_centre_chiplet = num_chiplet - (num_periphery_chiplet + num_corner_chiplet)
    return num_corner_chiplet,num_periphery_chiplet,num_centre_chiplet
