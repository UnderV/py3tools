#!/usr/bin/python3
import subprocess


def Shell_exec(bash_command):
    childProcess = subprocess.Popen(bash_command,
                                    shell=True,
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
    (out, err) = childProcess.communicate()

    # Return byte array converted to uft-8 string
    return(out.decode("utf-8").strip(),
           err.decode("utf-8").strip(),
           childProcess.returncode)
