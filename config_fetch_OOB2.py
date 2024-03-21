import paramiko
from dotenv import load_dotenv
import os
from datetime import datetime
import time
from concurrent.futures import ThreadPoolExecutor

# Load environment variables
load_dotenv()
USERNAME = os.getenv('SWITCH_USERNAME')
PASSWORD = os.getenv('SWITCH_PASSWORD')
OUTPUT_PATH_OOB = os.getenv('OUTPUT_PATH_OOB')

# Initialize an in-memory list to hold log messages
log_messages = []

def add_log_message(message):
    # Directly append the message to the in-memory log
    log_messages.append(message + "\n")

def start_logging():
    # Mark the start of logging with a timestamp
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    log_messages.append(f"######### Script Start: {start_time} ########\n")

def end_logging():
    # Mark the end of the script run
    end_time = datetime.now().strftime('%H:%M')
    log_messages.append(f"######### Run end: {end_time} ########\n")
    # Write everything to the log file
    write_log_to_file()

def write_log_to_file():
    full_log = "".join(log_messages)
    log_filename = os.path.join(OUTPUT_PATH_OOB, "!script_logs.txt")
    with open(log_filename, 'a') as log_file:
        log_file.write(full_log)
    # Clear log_messages for the next run
    log_messages.clear()

def get_switch_output(switch):
    filename = os.path.join(OUTPUT_PATH_OOB, f"{switch}_{datetime.now().strftime('%Y%m%d')}.txt")
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(switch, username=USERNAME, password=PASSWORD, look_for_keys=False)

        channel = client.invoke_shell()
        channel.send('term len 0\n')
        time.sleep(1)
        channel.send('show run\n')
        time.sleep(2)  
        channel.send('show version\n')
        time.sleep(2)  

        output = ""
        while True:
            if channel.recv_ready():
                output += channel.recv(65535).decode('utf-8')
                time.sleep(1)
            else:
                break

        with open(filename, 'w') as file:
            file.write(output)
        add_log_message(f"Output saved to {filename}")
    except Exception as e:
        add_log_message(f"Failed to connect or execute command on {switch}: {e}")
    finally:
        if client:
            client.close()

def main():
    start_logging()  # Start logging
    switches = []
    with open(os.getenv('SWITCH_LIST'), 'r') as file:
        switches = file.read().splitlines()

    # Execute get_switch_output function in parallel
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(get_switch_output, switches)

    end_logging()  # End logging and write to file

if __name__ == "__main__":
    main()
