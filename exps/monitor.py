import subprocess
from subprocess import PIPE
import time

# Define a function that runs the command and returns the output string
def get_nvlink_bandwidth():
  # Run the command and capture the output
  output = subprocess.run(["nvidia-smi", "nvlink", "-gt", "d"], stdout=PIPE, stderr=PIPE, universal_newlines=True)
  # Check if the command was successful
  if output.returncode == 0:
    # Return the output string
    return output.stdout
  else:
    # Raise an exception with the error message
    raise RuntimeError(output.stderr)

tx_key = 'tx'
rx_key = 'rx'

def get_counter_values(output_nvlink: str):
    lines = output_nvlink.splitlines()
    current_gpu = -1
    counter_values = {}

    for line in lines:
        if 'GPU' in line:
            current_gpu += 1
            if current_gpu not in counter_values:
                counter_values[current_gpu] = {tx_key: [], rx_key: []}

        if 'Link' in line:
            line = line.strip()
            parts = line.split()
            counter_val = int(parts[4])
            if 'Tx' in line:
                counter_values[current_gpu][tx_key].append(counter_val)
            if 'Rx' in line:
                counter_values[current_gpu][rx_key].append(counter_val)

    return counter_values

def print_data(current_values, init_counter_values, key_type):
    for gpu in current_values:
        nvlin_id = 0
        for x, y in zip(init_counter_values[gpu][key_type], current_values[gpu][key_type]):
            print('GPU {}/{}, link {}, {} KB'.format(gpu, key_type, nvlin_id, y - x))
            nvlin_id += 1

# Call the function and print the output string
output_string = get_nvlink_bandwidth()
init_counter_values = get_counter_values(output_string)


while True:
    time.sleep(0.05)
    output_string = get_nvlink_bandwidth()
    current_values = get_counter_values(output_string)
    print_data(current_values, init_counter_values, tx_key)
    print_data(current_values, init_counter_values, rx_key)
    
# TODO: 
# 1. How often can we poll?
# 2. Tx/Rx vs time plot.
# 3. WHy not put 12 nvswitches on a board?
# 4. 8 choose 7 measurements 