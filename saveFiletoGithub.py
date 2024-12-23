import os
import glob
import requests
import base64
import socket


file_path = '' 

# Get the device hostname
hostname = socket.gethostname()

# GitHub API Token and repository details
token = ''
repo = ''
owner = ''
dest_path = f'' 


with open(file_path, 'rb') as file:
    content = base64.b64encode(file.read()).decode('utf-8')

# GitHub API endpoint
url = f'https://api.github.com/repos/{owner}/{repo}/contents/{dest_path}'

# Data for the API request
data = {
    'message': f'Add OpenVPN configuration for {hostname}',
    'committer': {
        'name': 'Sam',
        'email': 'svaldez@barcoment.com'
    },
    'content': content,
    'branch': 'main'  # Specify the branch if different
}

# Headers with the authentication token
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

# Make the PUT request to upload the file
response = requests.put(url, json=data, headers=headers)

# Print the response from GitHub (success or failure)
print(response.json())
