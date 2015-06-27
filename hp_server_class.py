#!/usr/bin/python3
from py3tools.shell_exec import shell_exec

class HpServerClass():
    def __init__(self):
        self.reload()

    def reload_only(self, param):
        if param == 'temp':
            shell_command = 'hplog -t'
            # Define columns by teir size
            keys = ['id','type','location','status','current-f','current-c','threshold-f','threshold-c']
            keys_size = [4,13,16,9,5,5,5,4] # Define column size

        if param == 'fan':
            shell_command = 'hplog -f'
            # Define columns by teir size
            keys = ['id','type','location','status','redundant','fan','speed']
            keys_size = [4,13,16,11,8,9,5] # Define column size

        if param == 'power':
            shell_command = 'hplog -p'
            # Define columns by teir size
            keys = ['id','type','location','status','redundant']
            keys_size = [4,13,16,11,5] # Define column size

        (output, error, return_code) = shell_exec(shell_command)
        if return_code != 0: # If command fails return all shell outputs and errors
            raise ValueError(error, return_code)

        values_list = []

        formated_output = output.split('\n')
        formated_output = formated_output[1:] # Delete column name line

        for line in formated_output:
            t_dict = {}
            temp_line = line
            for i,value in enumerate(keys):
                t_dict[value] = temp_line[:keys_size[i]].strip()
                if value == 'current-f' or value == 'threshold-f':
                    t_dict[value] = t_dict[value][:-2] # Delete last 2 characters - 'F/'
                if value == 'current-c' or value == 'threshold-c':
                    t_dict[value] = t_dict[value][:-1] # Delete last character - 'C'
                if value == 'speed':
                    t_dict[value] = t_dict[value][1:-1].strip() # Delete first and last characters - '(' and ')'

                temp_line = temp_line[keys_size[i]:] # Each iteration line is shortened by used characters
            values_list.append(t_dict) # Array of dictionaries

        if param == 'temp':
            self.temp_list = values_list
        if param == 'fan':
            self.fan_list = values_list
        if param == 'power':
            self.power_list = values_list

    def reload(self):
        self.reload_only('temp')
        self.reload_only('fan')
        self.reload_only('power')

    def has_fan_failed(self):
        for item in self.fan_list:
            if item['status'] == 'Failed':
                return True
        return False

    def count_installed_fans(self):
        count = 0
        for item in self.fan_list:
            if item['status'] == ('Normal' or 'Failed'):
                count += 1
        return count

    def get_average_temp_c(self):
        temp_sum = 0
        count = 0
        for item in self.temp_list:
            if item['current-c'].isdigit():
                temp_sum += int(item['current-c'])
                count += 1
        return round(temp_sum / count)

    def get_average_temp_f(self):
        temp_sum = 0
        count = 0
        for item in self.temp_list:
            if item['current-f'].isdigit():
                temp_sum += int(item['current-f'])
                count += 1
        return round(temp_sum / count)
