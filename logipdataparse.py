import re
import requests
import os

def parseIP(filepath,regex = r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}'):
    """Simple Regex funtion to return all IP addresses in a file to a set.

    Args:
        filepath (path): location of logs containing IP address
        regex (regular expression): Regex expression used to find IP addresses Defaults to r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}'.

    Returns:
        Set: a set of all ip addresses found
    """
    # Simplified regex to match any 4 numbers separated by dots
    ip_addresses = []

    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            # Find all occurrences of this simple pattern
            matches = re.findall(regex, line)
            if matches:
                print(f"Found IPs: {matches}")  # Debugging: Display matched IPs
                ip_addresses.extend(matches)

    return set(ip_addresses)

def get_location(ip_address):
    """Using API to get the IP address location
    https://www.freecodecamp.org/news/how-to-get-location-information-of-ip-address-using-python/

    Args:
        ipaddress (string) : IPv4 address

    Returns:
        JSON information such as the IP, City, Region, and Country
    """
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
    }
    return location_data

def get_locations_fromlogs(filepath):
    """Used to get the IP addresses from a file and return location data to a file in the working directory.

    Args:
        filepath (path): _file path containing IP addresses

    Returns:
        Array: Returns a array of all locations
    """
    locations = []
    ips = parseIP(filepath)
    for ip in ips:
        location = get_location(ip)
        print(location)
        locations += location
    with open('locations.txt','w') as file:
        for location in locations:
            file.write(f'{location}\n')
    return locations


def main():
    """Prompt the user for a path and export the location information to the screen and to a file
    """
    # Get the file path from the user
    file_path = input("Please enter the file path: ")

    # Check if the file exists
    if os.path.isfile(file_path):
        print("The file exists.")
    else:
        print("The file does not exist.")
        get_locations_fromlogs(file_path)


# If the file is being ran as main
if __name__ == "__main__":
    main()
