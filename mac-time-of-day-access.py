
import json
import subprocess
from collections import OrderedDict
from datetime import datetime

HOSTAPD_PATH = '/etc/hostapd/'
HOSTAPD_ACCEPT_PATH = HOSTAPD_PATH + '/hostapd.accept'
MAC_TIME_FILTER_PATH = HOSTAPD_PATH + '/mac-time-filter.json'


def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end


if __name__ == '__main__':
    with open(HOSTAPD_ACCEPT_PATH, 'r') as file:
        # List of lines (OrderedDict.fromkeys autoatically removes duplicated lines)
        lines = list(OrderedDict.fromkeys(file.readlines()))

    with open(MAC_TIME_FILTER_PATH, 'r') as file:
        acl = json.load(file)  # Mac Time Filter

    # Access Control List (ACL) iterator
    update_file = False
    for mac, slots in acl.items():
        # Get index and line of line containing mac substring in lines
        for i, line in enumerate(lines):
            if mac in line:
                break
        else:
            i = None
        
        allowed = False
        for slot in slots:
            # MAC is allowed
            if time_in_range(datetime.strptime(slot[0], '%H:%M:%S').time(), datetime.strptime(slot[1], '%H:%M:%S').time(), datetime.now().time()):
                allowed = True
                if i != None:
                    if line[0] == '-':
                        lines[i] = line[1:]  # MAC wasn't allowed
                        update_file = True
                else:
                    lines.append(mac)  # MAC was missing
                    update_file = True
                break
        
        if not allowed:  # MAC isn't allowed
            if i != None and line[0] != '-':  # MAC was allowed, disallow
                lines[i] = '-'+line
                update_file = True

    if update_file:  # Update file only if needed
        with open(HOSTAPD_ACCEPT_PATH, 'w') as file:
            file.writelines(lines)
        subprocess.run(["sudo", "hostapd_cli", "set", "accept_mac_file", HOSTAPD_ACCEPT_PATH])
