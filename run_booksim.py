import os, re, glob, sys, math
import numpy as np
import shutil
from multiprocessing import Pool


def process_trace_files(trace_file_dir, mesh_size):


    os.chdir(trace_file_dir)

    # Get a list of all files in directory
    print (trace_file_dir)
    files = glob.glob('*.txt')
        
    # Open read file handle of config file
    fp = open('../../mesh_config_trace_based', 'r')

    # Set path to config file
    config_file = 'mesh_config'
    
    # Open write file handle for config file
    outfile = open(config_file, 'w')
    
    # Iterate over file and set size of mesh in config file
    for line in fp :
    
        line = line.strip()
    
        # Search for pattern
        matchobj = re.match(r'^k=', line)
    
        # Set size of mesh if line in file corresponds to mesh size
        if matchobj :
            line = 'k=' + str(mesh_size) + ';'
    
        ## Search for pattern
        #matchobj1 = re.match(r'^channel_width = ', line)
    
        ## Set size of mesh if line in file corresponds to mesh size
        #if matchobj1 :
        #  line = 'channel_width = ' + str(bus_width) + ';'
        
        # Write config to file
        outfile.write(line + '\n')
    
    # Close file handles
    fp.close()
    outfile.close()

    os.chdir('..')


    return files, config_file

def run_booksim(dir_name, config_file, file_name_prefix, trace_file):
    
    
    # Extract file name without extension and absolute path from filename

    os.chdir(dir_name)

    run_name = os.path.splitext(os.path.basename(trace_file))[0]
    run_id = run_name.strip(file_name_prefix)
    os.mkdir('trace_file_execution_' + str(run_id))
    os.chdir('trace_file_execution_' + str(run_id))

    # copy booksim binary and provide exec permission
    os.system('cp ../../../booksim .')
    os.system('chmod +x booksim')
    
    config_file_this_trace = 'config_file_' + str(run_id)
    os.system('cp ../' + config_file + ' ' + config_file_this_trace)


    # Set path to log file for trace files
    log_file = 'log_file_'  + str(run_id) + '.log'

    # Copy trace file
    os.system('cp ../' + trace_file + ' trace_file.txt')

    # Run Booksim with config file and save log
    booksim_command = './booksim ' + config_file_this_trace + ' > ' + log_file

    #print('Simulating trace_file_' + str(run_id))

    os.system(booksim_command)
    
    # Grep for total latency from log file
    latency_str = os.popen('grep "Trace is finished in" ' + log_file + ' | tail -1 | awk \'{print $5}\'').read().strip()
    latency = float(latency_str)
    #print('[ INFO] Latency for Trace file : ' + str(run_id) + ' is ' + str(latency) +'\n')
    latency_file = open('latency_file.txt', 'w')
    latency_file.write(latency_str)    



         # Grep for packet latency average from log file
    avg_latency_str = os.popen('grep "Packet latency average" ' + log_file + ' | tail -1 | awk \'{print $5}\'').read().strip()
    avg_latency = float(avg_latency_str)
    #print('[ INFO] Average Packet Latency for Trace file : ' + str(run_id) + ' is ' + str(avg_latency) +'\n')
    avg_latency_file = open('avg_latency_file.txt', 'w')
    avg_latency_file.write(avg_latency_str)    
    
    os.chdir('../..')



def gather_simulation_result(dir_name):

    os.chdir(dir_name)

    # remove mesh_config. otherwise it is also treated as directory
    os.system('rm mesh_config')

    dirs = [d for d in os.listdir(os.getcwd()) if os.path.isdir(d)] 
    num_dirs = len(dirs)

    avg_latencies = np.zeros(num_dirs)

    for directory in dirs:
        run_name = os.path.splitext(os.path.basename(directory))[0]
        run_id = run_name.strip('trace_file_execution_')
        avg_latency_file = open(directory + '/avg_latency_file.txt', 'r')
        avg_latency = avg_latency_file.read()
        avg_latencies[int(run_id)-1] = float(avg_latency)

    os.chdir('..')
    
    #print(avg_latencies)
    np.savetxt('avg_latencies_file.txt', np.c_[avg_latencies])
    return avg_latencies
 
