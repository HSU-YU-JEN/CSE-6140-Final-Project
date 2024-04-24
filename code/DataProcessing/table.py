import os
import numpy as np
import re

def read_solution_files(directory, prefix):
    max_values = []
    pattern = re.compile(r"^{}(?:[._].*|)\.sol$".format(re.escape(prefix)))
    for filename in os.listdir(directory):
        if pattern.match(filename):  # Use the regex pattern for matching
            with open(os.path.join(directory, filename), 'r') as file:
                max_value = float(file.readline().strip())
                max_values.append(max_value)
    return np.mean(max_values) if max_values else None

def read_trace_files(directory, prefix):
    max_values_times = []
    pattern = re.compile(r"^{}(?:[._].*|)\.trace$".format(re.escape(prefix)))
    for filename in os.listdir(directory):
        if pattern.match(filename):
            with open(os.path.join(directory, filename), 'r') as file:
                max_value = None
                first_time_for_max = None
                for line in file:
                    time, value = line.strip().split(',')
                    value = float(value)
                    time = float(time)
                    # Update the maximum value and time if this value is greater than the current max
                    if max_value is None or value > max_value:
                        max_value = value
                        first_time_for_max = time
                if max_value is not None:
                    max_values_times.append(first_time_for_max)
    # Return the average of the times for the first occurrence of maximum values across all files
    return np.mean(max_values_times) if max_values_times else None


def find_prefixes(directory):
    prefixes = set()
    for filename in os.listdir(directory):
        if filename.endswith(".sol"):
            # This assumes filenames are in the form 'small_1_LS1_xx.sol'
            part = filename.split('_')
            if len(part) > 1:
                prefixes.add('_'.join(part[:2]))  # Adjust this depending on the specific format
    return prefixes

solution_dir = 'Output/solution_files/LS1/large_scale/'  # Adjust the path as needed
trace_dir = 'Output/trace_files/LS1/large_scale/'  # Adjust the path as needed

solution_prefixes = find_prefixes(solution_dir)


# Processing each prefix group separately
for prefix in solution_prefixes:
    solution_files_path = solution_dir
    trace_files_path = trace_dir

    avg_max_value = read_solution_files(solution_files_path, prefix)
    if avg_max_value is not None:
        print(f"Average maximum value for {prefix}: {avg_max_value/3283122:.2f}")
        times_when_max_occurred = read_trace_files(trace_files_path, prefix)
        if times_when_max_occurred is not None:
            print(f"Earliest time to reach max value for {prefix}: {times_when_max_occurred:.2f}")
        else:
            print(f"No max value found in the traces for {prefix}")
    else:
        print(f"No solution files found for {prefix}")
