#!/usr/bin/python3
from py3tools.shell_exec import shell_exec

def ping(ip_address, ping_count):
    if not isinstance(ping_count, str): # Check if ping_count is not string
        ping_count = str(ping_count) # Convert to string if variable is not string

    (output, error, return_code) = shell_exec("ping -c "+ping_count+" "+ip_address)
    return (output, error, return_code)
