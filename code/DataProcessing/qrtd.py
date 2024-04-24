import numpy as np
import matplotlib.pyplot as plt
import os
import glob

def load_data(directory, file_pattern, optimal_value):
    # List all trace files in the directory
    file_paths = glob.glob(os.path.join(directory, file_pattern))
    all_data = []

    for file_path in file_paths:
        # Load time and values from each file
        data = np.loadtxt(file_path, delimiter=',')
        all_data.append(data)

    return all_data

def calculate_qrtd(all_data, optimal_value, quality_percents):
    # Find the maximum time to create a common time scale
    max_time = max(max(data[:, 0]) for data in all_data)
    min_time = min(min(data[:, 0][data[:, 0] > 0]) for data in all_data)  # ignore zero time
    time_points = np.logspace(np.log10(min_time), np.log10(max_time), 500)
    qrtd_curves = {q: [] for q in quality_percents}
    for time in time_points:
        for q in quality_percents:

            quality_threshold = optimal_value * (1 - q / 100)
            count_meeting_quality = 0
            for data in all_data:
                
                relevant_values = data[data[:, 0] <= time, 1]
                if relevant_values.size > 0:  # Check if there are any values
                    max_value = np.max(relevant_values)
                    if max_value >= quality_threshold:
                        count_meeting_quality += 1
                else:  # If there are no values, handle accordingly
                    # For example, you might want to assume the run did not meet the quality
                    # or you might want to handle this differently depending on your data
                    pass
            # Calculate the fraction of runs meeting the quality threshold by this time
            fraction_meeting_quality = count_meeting_quality / len(all_data)
            qrtd_curves[q].append(fraction_meeting_quality)

    return time_points, qrtd_curves

def plot_qrtd(time_points, qrtd_curves):
    plt.figure(figsize=(10, 6))
    for q, fractions in qrtd_curves.items():
        plt.semilogx(time_points, fractions, label=f'{q}%')
    plt.title('Qualified Runtime Distribution (QRTD) for GA Algorithm (large_3)')
    plt.xlabel('Run-time [CPU sec]')
    plt.ylabel('P(solve)')
    plt.legend()
    plt.grid(True, which="both", linestyle='--')
    plt.xlim(10, 1800)
    plt.ylim(0, 1)
    plt.show()

# Define the directory, file pattern, and optimal value
directory = 'Output/trace_files/LS1/large_scale/'
file_pattern = 'large_3_LS1_1800_*'
optimal_value = 28857
quality_percents = [40, 45, 50, 55, 60]  # Different quality levels in percentage

# Load and process the data
all_data = load_data(directory, file_pattern, optimal_value)
time_points, qrtd_curves = calculate_qrtd(all_data, optimal_value, quality_percents)

# Plot the QRTD curve
plot_qrtd(time_points, qrtd_curves)
