#!/usr/bin/python3

# This tool requires some HP packages onserver.
# Use HP repository - http://downloads.linux.hp.com/downloads/ManagementComponentPack/ubuntu
# Install 3 packages - hpacucli hp-health hponcfg

from py3tools.shell_exec import shell_exec

def hp_monitoring(param):
    if param == 'temperature':
        shell_command = 'hplog -t'
        # Define columns by teir size
        t_keys = ['id','type','location','status','current-f','current-c','threshold-f','threshold-c']
        t_keys_size = [4,13,16,9,5,5,5,4] # Define column size

    if param == 'fan':
        shell_command = 'hplog -f'
        # Define columns by teir size
        t_keys = ['id','type','location','status','redundant','speed-status','speed']
        t_keys_size = [4,13,16,11,8,9,5] # Define column size

    if param == 'power':
        shell_command = 'hplog -p'
        # Define columns by teir size
        t_keys = ['id','type','location','status','redundant']
        t_keys_size = [4,13,16,11,5] # Define column size


    (output, error, return_code) = shell_exec(shell_command)
    if return_code != 0: # If command fails return all shell outputs and errors
        return (output, error, return_code)



    t_values_list = []

    formated_output = output.split('\n')
    formated_output = formated_output[1:] # Delete column name line

    for line in formated_output:
        t_dict = {}
        temp_line = line
        for i,value in enumerate(t_keys):
            t_dict[value] = temp_line[:t_keys_size[i]].strip()
            if value == 'current-f' or value == 'threshold-f':
                t_dict[value] = t_dict[value][:-2] # Delete last 2 characters - 'F/'
            if value == 'current-c' or value == 'threshold-c':
                t_dict[value] = t_dict[value][:-1] # Delete last character - 'C'
            if value == 'speed':
                t_dict[value] = t_dict[value][1:-1].strip() # Delete first and last characters - '(' and ')'

            temp_line = temp_line[t_keys_size[i]:] # Each iteration line is shortened by used characters
        t_values_list.append(t_dict) # Array of dictionaries
    return (t_values_list, '', 0)

