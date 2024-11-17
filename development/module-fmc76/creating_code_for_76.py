import sys
import time
import subprocess
import xml.etree.ElementTree as ET

# Define device information
ftd_device = {
    "host": "192.168.1.15",       # replace with your FTD IP
    "username": "admin",          # replace with your username
    "password": "admin",          # replace with your password
}

param_1 = sys.argv[1]
param_2 = sys.argv[2]
quarantine_seconds = 60

# Parse the quarantine_seconds from instance.conf
'''tree = ET.parse("instance.conf")
quarantine_seconds = int(tree.find("./config/string[@name='quarantine_seconds']").text)
'''
def run_ssh_command_with_password(command):
    """Execute a command in an SSH session with password."""
    try:
        # Open an SSH session
        ssh_command = f"ssh -o StrictHostKeyChecking=no {ftd_device['username']}@{ftd_device['host']}"
        process = subprocess.Popen(
            ssh_command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Prepare the sequence of commands
        input_data = f"{ftd_device['password']}\n"  # send the password once
        input_data += f"{command}\n"  # send the actual command
        input_data += "exit\n"  # close the SSH session

        # Communicate with the process (send password and command)
        stdout, stderr = process.communicate(input_data)

        if process.returncode != 0:
            raise Exception(stderr)

        return stdout.strip()

    except Exception as e:
        print(f"Error executing SSH command: {e}")
        return None

def execute_shun_commands():
    """Execute shun and no shun commands, including the quarantine period."""
    try:
        # Execute the shun command
        print("Sending 'shun' command...")
        shun_output = run_ssh_command_with_password(f"shun {param_2}")
        print(f"Shun output:\n{shun_output}")

        # Wait for the quarantine period
        print(f"Waiting for {quarantine_seconds} seconds...")
        time.sleep(quarantine_seconds)

        # Execute the no shun command
        print("\nSending 'no shun' command...")
        no_shun_output = run_ssh_command_with_password(f"no shun {param_2}")
        print(f"End of quarantine output:\n{no_shun_output}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Execute the commands
execute_shun_commands()
