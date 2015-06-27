#!/usr/bin/python3
from py3tools.shell_exec import shell_exec

class LvmClass():
    def __init__(self):
        self.reload()

    def reload(self):
        # Getting data about Physical Volumes
        (pv_output, pv_error, pv_return_code) = shell_exec("pvs --units b --nosuffix --separator ';' -o pv_all 2>/dev/null")
        if pv_return_code != 0:
            raise ValueError(pv_error, pv_return_code)

        pv_output_line_array = pv_output.split('\n') # Split output by 'newline'
        pv_keys = pv_output_line_array[0].strip().split(';') # First output line split by ';'
        pv_output_line_array.pop(0) # Delete first line from output array

        self.pv_dict = [] # Create dictionary array.
        for line in pv_output_line_array:
            self.pv_dict.append(dict(zip(pv_keys,line.strip().split(";")))) # Fill dictionary with key value

        # Getting data about Volume Groups
        (vg_output, vg_error, vg_return_code) = shell_exec("vgs --units b --nosuffix --separator ';' -o vg_all 2>/dev/null")
        if vg_return_code != 0:
            raise ValueError(vg_error, vg_return_code)

        vg_output_line_array = vg_output.split('\n') # Split output by 'newline'
        vg_keys = vg_output_line_array[0].strip().split(';') # First output line split by ';'
        vg_output_line_array.pop(0) # Delete first line from output array

        self.vg_dict = [] # Create dictionary array.
        for line in vg_output_line_array:
            self.vg_dict.append(dict(zip(vg_keys,line.strip().split(";")))) # Fill dictionary with key value

        # Getting data about Logical Volumes
        (lv_output, lv_error, lv_return_code) = shell_exec("lvs --units b --nosuffix --separator ';' -o lv_all 2>/dev/null")
        if lv_return_code != 0:
            raise ValueError(lv_error, lv_return_code)

        lv_output_line_array = lv_output.split('\n') # Split output by 'newline'
        lv_keys = lv_output_line_array[0].strip().split(';') # First output line split by ';'
        lv_output_line_array.pop(0) # Delete first line from output array

        self.lv_dict = [] # Create dictionary array.
        for line in lv_output_line_array:
            self.lv_dict.append(dict(zip(lv_keys,line.strip().split(";")))) # Fill dictionary with key value

        return True

    def vg_exists(self, vg_name):
        for item in self.vg_dict:
            if item["VG"] == vg_name:
                return True
        return False

    def lv_exists(self, vg_name, lv_name): # Check if Logical Volume exists
        for item in self.lv_dict:
            if item["Path"] == '/dev/'+vg_name+'/'+lv_name:
                return True
        return False

    def get_vg_free_space(self, vg_name): # Size in bytes
        for item in self.vg_dict:
            if item["VG"] == vg_name:
                return item["VFree"]
        return False

    def get_lv_attr(self, vg_name, lv_name): # Get Logical Volume's attributes
        for item in self.lv_dict:
            if item["Path"] == '/dev/'+vg_name+'/'+lv_name:
                return item["Attr"]
        return False

    def get_vg_attr(self, vg_name): # Get Volume Group's attributes
        for item in self.vg_dict:
            if item["VG"] == vg_name:
                return item["Attr"]
        return False

    def has_lv_snapshot(self, vg_name, lv_name): # Check if Logical Volume has snapshots
        if self.lv_exists(vg_name, lv_name):
            if self.get_lv_attr(vg_name, lv_name)[0] == 'o' or self.get_lv_attr(vg_name, lv_name)[0] == 'O':
                return True
        return False

    def is_snapshot(self, vg_name, lv_name): # Check if lv_name is snapshot
        for item in self.lv_dict:
            if item["Path"] == '/dev/'+vg_name+'/'+lv_name:
                if item["Origin"] and item["Attr"][0] == 's':
                    return True
        return False

    def is_lv_in_use(self, vg_name, lv_name): # Check if Logical Volume/Snapshot in use (for example - it is monted or opened)
        if self.lv_exists(vg_name, lv_name): # Check if Logical Volume exists
            if self.get_lv_attr(vg_name, lv_name)[5] == 'o':
                return True
        return False

    def create_lv(self, vg_name, lv_name, lv_size): # lv_size should be in bytes
        if not isinstance(lv_size, str): # Check if snap_size is string
            lv_size = str(lv_size) # Convert to string if variable is integer

        if self.vg_exists(vg_name): # Check if Volume Group exists
            if int(self.get_vg_free_space(vg_name)) > int(lv_size): # Check free space on Volume Group
                if not self.lv_exists(vg_name, lv_name): # Logical Volume should not exist
                    (output, error, return_code) = shell_exec("lvcreate -L "+lv_size+"B -n "+lv_name+" /dev/"+vg_name)
                    if return_code == 0:
                        self.reload() # Read new data
                        return True
        return False

    def create_snapshot(self, vg_name, lv_name, snap_name, snap_size): # snap_size should be in bytes, integer or string
        if not isinstance(snap_size, str): # Check if snap_size is string
            snap_size = str(snap_size) # Convert to string if variable is integer

        if self.vg_exists(vg_name): # Check if Volume Group exists
            if int(self.get_vg_free_space(vg_name)) > int(snap_size): # Check free space on Volume Group
                if self.lv_exists(vg_name, lv_name): # Check if Logical Volume exists
                    if not self.lv_exists(vg_name, snap_name): # Snapshot should not already exist
                        (output, error, return_code) = shell_exec("lvcreate -L "+snap_size+"B -s -n "+snap_name+" /dev/"+vg_name+"/"+lv_name)
                        if return_code == 0:
                            self.reload() # Read new data
                            return True
        return False

    def delete_snapshot(self, vg_name, lv_name): # lv_name is snapshot name
        if self.is_snapshot(vg_name, lv_name): # Check that Logical Volume is snapshot
            if not self.is_lv_in_use(vg_name, lv_name): # Logical Volume should not be in use
                (output, error, return_code) = shell_exec("lvremove /dev/"+vg_name+"/"+lv_name+"  --force")
                if return_code == 0:
                    self.reload() # Read new data
                    return True
        return False

    def delete_lv(self, vg_name, lv_name): # Delete Logical Volume
        if self.lv_exists(vg_name, lv_name): # Check if Logical Volume exists
            if not self.has_lv_snapshot(vg_name, lv_name): # Logical Volume should have no snapshots
                if not self.is_lv_in_use(vg_name, lv_name): # Logical Volume should not be in use
                    (output, error, return_code) = shell_exec("lvremove /dev/"+vg_name+"/"+lv_name+"  --force")
                    if return_code == 0:
                        self.reload() # Read new data
                        return True
        return False
