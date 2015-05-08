#!/usr/bin/python3
from py3tools.shell_exec import shell_exec

def ping(ip_address, ping_count, return_type='standard'):
    if not isinstance(ping_count, str): # Check if ping_count is not string
        ping_count = str(ping_count) # Convert to string if variable is not string

    (output, error, return_code) = shell_exec("ping -c "+ping_count+" "+ip_address)

    if return_type == 'standard':
        return (output, error, return_code)
    if return_type == 'json':
        if return_code == 0:
            packets_key_list = ['packets transmitted', 'received', 'packet loss', 'time']
            time_key_list = ['min', 'avg', 'max', 'mdev']
            packets_value_list = []

            # Sample of line: "1 packets transmitted, 1 received, 0% packet loss, time 0ms"
            packets = output.split('\n')[-2].split(',')
            for line in packets:
                for key in packets_key_list:
                    if key in line:
                        packets_value_list.append(line.replace(key, "").strip())
            packets_dict = dict(zip(packets_key_list, packets_value_list))

            # Sample of line: "rtt min/avg/max/mdev = 1.868/1.868/1.868/0.000 ms"
            time_value_list = output.split('\n')[-1].split('=')
            time_value_list = time_value_list[1][:-2] # remove "ms" at line end
            time_value_list = time_value_list.split('/')
            time_value_list_stripped = map(str.strip, time_value_list)

            time_dict = dict(zip(time_key_list, time_value_list_stripped))

            # Merge packets_dict and time_dict
            output_dict = packets_dict.copy()
            output_dict.update(time_dict)

            # outpput_dict sample: {'packets transmitted': '1', 'received': '1', 'packet loss': '0%', 'time': '0ms', 'min': '1.868', 'avg': '1.868', 'max': '1.868', 'mdev': '0.000'}
            return(output_dict, error, return_code)
        if return_code == 1:
            # Ping return return code '1' in two different situations

            # Situation 1: Subnet is OK, but host is unreachable
            # Sample output: "2 packets transmitted, 0 received, +2 errors, 100% packet loss, time 1007ms"
            packets_key_list5 = ['packets transmitted', 'received', 'errors', 'packet loss', 'time']

            # Situation 2: Cannot reach even subnet
            # Sample output: "2 packets transmitted, 0 received, 100% packet loss, time 1006ms"
            packets_key_list4 = ['packets transmitted', 'received', 'packet loss', 'time']

            # Usefull output could be on one of two last lines (check by existing of ',')
            if ',' in output.split('\n')[-2]:
                packets = output.split('\n')[-2].split(',')
            else:
                packets = output.split('\n')[-1].split(',')

            packets_value_list = []

            # Check what situation of output we have - 5 or 4 items
            if len(packets) == 5:
                packets_key_list = packets_key_list5
            else:
                packets_key_list = packets_key_list4

            for line in packets:
                for key in packets_key_list:
                    if key in line:
                        packets_value_list.append(line.replace(key, "").strip())
            packets_dict = dict(zip(packets_key_list, packets_value_list))

            return(packets_dict, error, return_code)
        else:
            return (output, error, return_code)
