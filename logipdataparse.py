import csv
import re
import json
import requests


"""
Author: Samuel Valdez
Date: 09/21/2024
Version:  1.0
"""

def opertaionRows(filepath,operation: str,userId:str):
    """When reviewing a CSV for M365 Audit logs you can use this to filter by user and operation.

    Args:
        filepath : Filepath of audit logs
        operation (str): Operation name as in the file(not case senstive)
        userId (str): User Id as in the file(not case senstive)

    Returns:
        2 demininal array: contains each row that matchs the user and operation in a array.
    """
    OPERATIONCOLUMN = 3
    USERIDCOLUMN = 4
    operationRows = []
    with open(filepath,newline='') as logfiledcsv:
        logreader = csv.reader(logfiledcsv)
        for row in logreader:
            if row[OPERATIONCOLUMN].lower() == operation.lower() and row[USERIDCOLUMN].lower() == userId.lower():
                operationRows.append(row)
    return operationRows


def sessionParser(auditData):
    """Session Parser which gets the sessions for a Json Auditdata

    Args:
        auditData (Json): Json Data for the microsoft perview audit log

    Returns:
        string: session ID
    """
    sessionid = ""
    jsondata = json.loads(auditData)
    for data in jsondata["DeviceProperties"]:
        if (data.get("Name")) == "SessionId":
            sessionid = data.get("Value")
    return sessionid

def clientIPParsing(auditData):
    """Returns the Client IP from JSON data

    Args:
        auditData (JSON): Returns client data from microsoft perview audit log

    Returns:
        string: Client IP
    """
    jsondata = json.loads(auditData)
    return jsondata.get("ClientIP")

def ipLookup(ip:int):
    """Returns a key pair value of a ip and the location data in a list

    Args:
        ip (Ip address): Public IP address being search

    Returns:
        dictonary: {ip:[city,region,country]}
    """
    response = requests.get(f'https://ipapi.co/{ip}/json/').json()
    # Getting location data as a list
    location_data = [
        response.get("city"),
        response.get("region"),
        response.get("country_name")
    ]
    # Returning as a key pair value
    return {str(ip): location_data}

def getSessionInformation(filepath, userID):
    #Audit data
    AUDITDATACOLUMN = 5
    # Get the mathching rows
    opertation = 'UserLoggedIn'
    matchingrows = opertaionRows(filepath, opertation,userID)

    # Get the session ID's & Ip's
    sessionIds  = set() # Using set to remove duplicate sessions and store them for use
    ipAddresses = set() # Using set to remove duplicate IP addresses and store for use
    IpLocations = {} # Used to store all the IP address and location informatoin in a dictonary
    sessioninformation = {} # Used to store all the Sessions and IP and location infromation associate with each one.

    # Getting every session and IP address
    for row in matchingrows:
        sessionIds.add(sessionParser(row[AUDITDATACOLUMN]))
        ipAddresses.add(clientIPParsing(row[AUDITDATACOLUMN]))

    # add IP locations in a dictonary
    for ip in ipAddresses:
        IpLocations.update(ipLookup(ip))
    
    # Go though each session
    for session in sessionIds:
        sessionips = set() # Resets on each session
        # Find the session in the row and sess if it is the same session and add ip to sessionIps
        for row in matchingrows:
            rowsession = sessionParser(row[AUDITDATACOLUMN])
            if rowsession == session:
                sessionips.add(clientIPParsing(row[AUDITDATACOLUMN]))
        # for all ip addressies in a session add a key:value pair being Ip:location information to the iplocationdic
        iplocationdic = {}
        # For each ip add the locatoin and ip infromation to a set
        for ip in sessionips:
            if ip in IpLocations:
                iplocationdic[ip] = IpLocations[ip]
        # For eacg session add the session and its IP and location information to a dictionary
        sessioninformation[session] = iplocationdic
    
    # Return session infomration
    return sessioninformation

def main():
    print("Lets get this login information")
    filepath = r"{}".format(input("Please Enter Purview audit filepath: "))
    userID = input("Please enter UserID to get login information from: ")
    sessionsinfo = getSessionInformation(filepath, userID)
    for session, ip_data in sessionsinfo.items():
        print(f"session: {session}")
        for ip, location in ip_data.items():
            city, state, country = location
            print(f"  IP Address: {ip}")
            print(f"    City: {city}")
            print(f"    State: {state}")
            print(f"    Country: {country}")
        print()

if __name__ == "__main__":
    main()
