import os
import numpy as np
import matplotlib.pyplot as plt
import re

def read_last_time(directory, prefix):
    running_times = []
    pattern = re.compile(r"^{}(?:[._].*|)\.trace$".format(re.escape(prefix)))
    for filename in os.listdir(directory):
        if pattern.match(filename):
            with open(os.path.join(directory, filename), 'r') as file:
                last_time = None
                for line in file:
                    time, value = line.strip().split(',')
                    last_time = float(time)
                if last_time is not None:
                    running_times.append(last_time)
    return running_times


def plot_running_times(directory, prefixes):
    data = []
    labels = []
    for prefix in prefixes:
        times = read_last_time(directory, prefix)
        if times:
            data.append(times)
            labels.append(prefix)
    
    if data:
        plt.figure(figsize=(10, 6))
        plt.boxplot(data, labels=labels)
        plt.title('Running Time Boxplot (Hill Climbing)')
        plt.ylabel('Running Time (seconds)')
        plt.xlabel('Dataset')
        plt.grid(True)
        plt.show()
    else:
        print("No data to plot.")

solution_dir = 'Output/solution_files/LS2/large_scale/'  # Adjust the path as needed
trace_dir = 'Output/trace_files/LS2/large_scale/'  # Adjust the path as needed

# We focus only on the 'large_1' and 'large_3' prefixes
plot_running_times(trace_dir, ['large_1', 'large_3'])
