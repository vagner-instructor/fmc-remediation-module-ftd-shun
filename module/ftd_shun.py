#!/usr/bin/env python
"""
Cisco Firepower Management Center (FMC) Remediation module for Temporary Shun
Author: Vagner Silva
Credits: Chetankumar Phulpagare - fmc-remediation-module-xdr
"""

import sys
import time
import xml.etree.ElementTree as ET
import requests
import paramiko

param_1 = sys.argv[1]
param_2 = sys.argv[2]

# Read Firewall Details from instance.conf
tree = ET.parse("instance.conf")
quarantine_time = int(tree.find("./config/string[@name='quarantine_time']").text)
firewall_ip = tree.find("./config/string[@name='firewall_ip']").text
firewall_username = tree.find("./config/string[@name='firewall_username']").text
firewall_password = tree.find("./config/string[@name='firewall_password']").text
firewall_port = tree.find("./config/string[@name='firewall_port']").text

ftd_device = {
    "host": firewall_ip,       # replace with your FTD IP
    "username": firewall_username,          # replace with your username
    "password": firewall_password,          # replace with your password
    "port": firewall_port,                   # default SSH port
    "secret": firewall_password   # if enable mode is needed
}

try:
    # Initialize SSH client
    ssh_client = paramiko.SSHClient()
#    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.set_missing_host_key_policy(paramiko.RejectPolicy())

    # Connect to the device
    ssh_client.connect(
        hostname=ftd_device["host"],
        port=ftd_device["port"],
        username=ftd_device["username"],
        password=ftd_device["password"]
    )

    # Start an interactive shell session
    remote_conn = ssh_client.invoke_shell()

      # Send shun command
    time.sleep(1)  
    remote_conn.send("shun " + param_2 + "\n")
    time.sleep(2)
    output = remote_conn.recv(65535).decode("utf-8")
    print("\nShun output:")
    print(output)


    # Wait for quarantine period
    time.sleep(quarantine_time)

    # Send no shun command
    remote_conn.send("no shun " + param_2 + "\n")
    time.sleep(2)
    output = remote_conn.recv(65535).decode("utf-8")
    print("\nEnd Of Quarantine of " + str(quarantine_time) + " seconds:")
    print(output)

    # Close the connection
    ssh_client.close()

except Exception as e:
    print(f"An error occurred: {e}")
