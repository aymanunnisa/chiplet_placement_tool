import pandas as pd

def find_min_latency(file_path, min_index2):
    data = pd.read_csv(file_path)
    
    min_value1 = data.iloc[:, 0].min()      
    min_index1 = data.iloc[:, 0].idxmin()     
    
    latency_at_min_md = data.iloc[min_index2, 0] 
    print(data.to_string()) 
    print("--------------")
    print(f"data_size: {data.shape[0]}")
    print(f"Min latency: {min_value1}")
    print(f"Index of Min latency: {min_index1}")
    
    print(f"Manhattan distance at Min latency index: {latency_at_min_md}")
    return min_index1, min_value1, latency_at_min_md

def find_min_md(file_path):
    data = pd.read_csv(file_path)
    
    min_value2 = data.iloc[:, 0].min()         
    min_index2 = data.iloc[:, 0].idxmin()      
    
    print(f"Min Manhattan distance: {min_value2}")
    print(f"Index of Min Manhattan distance: {min_index2}")
    #print(f"Manhattan distance at Min latency index: {latency_at_min_md}")
    
    return min_index2, min_value2
    


'''# File paths
latency_file_path = '/home/ayman/chiplet_placement/source_code/4r_32_60_n-1//avg_latencies.csv'
md_file_path = '/home/ayman/chiplet_placement/source_code/4r_32_60_n-1/manhattan_distances.csv'

min_index2, min_value2 = find_min_md(md_file_path)
# Step 1: Find the minimum latency and its index
min_index1, min_value1, latency_at_min_md = find_min_latency(latency_file_path, min_index2)

# Step 2: Find the minimum Manhattan distance, index, and Manhattan distance at min latency index
#:x
#min_index2, min_value2 = find_min_md(md_file_path)

# Calculate the total percentage
total_perc = (float(latency_at_min_md - min_value1) / min_value1) * 100
print(f"Total Percentage: {total_perc}")'''
