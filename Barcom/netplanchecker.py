import subprocess
import time
import os
import sys 

# Constants
WAIT_TIME_S = 300 # Time between each network connectivity check
PING_HOST = "8.8.8.8" # Host used to determine network connectivity
PING_COUNT = "4" # Number of pings
YAMLFILE = "file.yaml" # Yaml file name
CUSTOMPATH = '/home/user/' # file path to store the yaml file
NETPLANPATH = '/etc/netplan/' # Default netplan path


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
    pingcount = output.count(host)
    print(f"Ping count {pingcount-3}")
    # Return the count
    return pingcount


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
        print(f"Option1 moviong file {YAMLFILE} to {custom_file_path}")
        subprocess.run(['mv', netplan_file_path, custom_file_path])
        subprocess.run(['reboot'])

    # If the file is not yet configured then do the configuration
    elif os.path.isfile(custom_file_path):
        print(f"Option2 moving file {YAMLFILE} to {netplan_file_path}")
        subprocess.run(['mv', custom_file_path, netplan_file_path])
        subprocess.run(['netplan', 'apply'])
        subprocess.run(['reboot'])
    # if the files are in the wrong location or dont exist no actions would be performed
    return

def cron_creator():
    # Locate the Python interpreter
    python_bin_path = sys.executable

    # Get the full path of the current script
    script_path = os.path.abspath(__file__)

    # Construct the cron command to check
    cron_command = f"@reboot {python_bin_path} {script_path}"

    # Check if the cron job already exists
    existing_crontab = os.popen('crontab -l').read()

    if cron_command in existing_crontab:
        print("Cron job already exists.")
    else:
        # Add the cron job
        os.system(f'(crontab -l ; echo "{cron_command}") | crontab -')
        print(f"Cron job added to run {script_path} at system startup using {python_bin_path}.")

# Main funtion
def main():
    cron_creator()
    # Wait X amount of time
    time.sleep(WAIT_TIME_S)
    # First network connectivity test
    if (int(PING_COUNT) + 3) != ping_host_count(PING_HOST):
        print("First Fail")
        # Wait x time if failed
        time.sleep(WAIT_TIME_S)
        # Second network connectivity test
        if (int(PING_COUNT) + 3) != ping_host_count(PING_HOST):
            print("Second Fail executing logic option")
            # If failed run logic 
            logic()
    else:
        print("Online")
    return


# This block runs when the script is executed directly
if __name__ == '__main__':
    main()
