import subprocess
import time
import os

# Constants
WAIT_TIME_S = 600 # Time between each network connectivity check
PING_HOST = '8.8.8.8' # Host used to determine network connectivity
PING_COUNT = 4 # Number of pings
YAMLFILE = "Filename.yaml" # Yaml file name
CUSTOMPATH = '/home/user' # file path to store the yaml file
NETPLANPATH = '/etc/netplan' # Default netplan path


def ping_host_count(host):
    """Used to count the amount of times a host appears in a ping command to determine
    network connectivity

    Args:
        host (string): host being pinged

    Returns:
        int: counts the amount of times the host appears in the output
    """
    # Run the ping command and capture its output
    result = subprocess.run(['ping', '-c', PING_COUNT, host], capture_output=True, text=True)

    # Get the standard output from the result
    output = result.stdout

    # Return the count
    return output.count(host)


# Logic of script
def logic():
    """
    Handles the logic for moving and applying Netplan configuration based on the current file locations.

    The function performs the following steps:
    
    1. **Check for Existing Netplan File:**
       - If the Netplan configuration file (`YAMLFILE`) is found at the Netplan path (`NETPLANPATH`), 
         it moves the file to the custom path (`CUSTOMPATH`) and then reboots the system to apply the new configuration.

    2. **Check for Custom File:**
       - If the Netplan configuration file is found at the custom path (`CUSTOMPATH`), it moves the file back 
         to the Netplan path (`NETPLANPATH`), applies the Netplan configuration with `netplan apply`, and reboots the system 
         to apply the changes.

    3. **No Action Taken:**
       - If neither the Netplan file is found at `NETPLANPATH` nor at `CUSTOMPATH`, the function does nothing.

    The function relies on file presence checks and system commands to manage the Netplan configuration and handle 
    system reboots accordingly. It assumes that the user has appropriate permissions to move files and reboot the system.
    """
        
    # File paths being tested to determine current configuration
    netplan_file_path = os.path.join(NETPLANPATH, YAMLFILE)
    custom_file_path = os.path.join(CUSTOMPATH, YAMLFILE)

    # If the file is already in the netplan file then move it out and reboot
    if os.path.isfile(netplan_file_path):
        subprocess.run(['mv', netplan_file_path, custom_file_path])
        subprocess.run(['reboot'])

    # If the file is not yet configured then do the configuration
    elif os.path.isfile(custom_file_path):
        subprocess.run(['mv', custom_file_path, netplan_file_path])
        subprocess.run(['netplan', 'apply'])
        subprocess.run(['reboot'])
    # if the files are in the wrong location or dont exist no actions would be performed
    return


# Main funtion
def main():
    # Wait X amount of time
    time.sleep(WAIT_TIME_S)
    # First network connectivity test
    if (PING_COUNT + 3) != ping_host_count(PING_HOST):
        # Wait x time if failed
        time.sleep(WAIT_TIME_S)
        # Second network connectivity test
        if (PING_COUNT + 3) != ping_host_count(PING_HOST):
            # If failed run logic 
            logic()
    return


# This block runs when the script is executed directly
if __name__ == '__main__':
    main()
