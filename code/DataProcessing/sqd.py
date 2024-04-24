import numpy as np
import matplotlib.pyplot as plt
import os
import glob

def load_data(directory, file_pattern):
    # List all trace files in the directory
    file_paths = glob.glob(os.path.join(directory, file_pattern))
    all_data = []

    for file_path in file_paths:
        # Load time and values from each file
        data = np.loadtxt(file_path, delimiter=',')
        all_data.append(data)

    return all_data

def calculate_sqd(all_data, optimal_value, fixed_times):
    # Collect all values at the fixed times
    all_values_at_times = {time: [] for time in fixed_times}
    for data in all_data:
        for time in fixed_times:
            # Find the best value at or before the fixed time
            relevant_values = data[data[:, 0] <= time, 1]
            if relevant_values.size > 0:
                all_values_at_times[time].append(np.max(relevant_values))
            else:
                # If no solution was found by this time, append a value that indicates no solution.
                # This could be 0 or you could choose to append None or np.nan depending on how you want to handle it.
                all_values_at_times[time].append(np.nan)
    
    sqd_curves = {}
    # Calculate relative quality percentages for the linspace
    min_quality = min([min(values) for values in all_values_at_times.values() if len(values) > 0], default=optimal_value) / optimal_value - 1
    max_quality = max([max(values) for values in all_values_at_times.values() if len(values) > 0], default=optimal_value) / optimal_value - 1
    relative_qualities = np.linspace(min_quality, max_quality, 500)

    for time, values_at_time in all_values_at_times.items():
        sqd_curve = []
        # Ignore runs where no solution was found by this time
        valid_values = [v for v in values_at_time if not np.isnan(v)]
        for rq in relative_qualities:
            rq_threshold = optimal_value * (1 + rq)
            count_meeting_rq = sum(value >= rq_threshold for value in valid_values)
            fraction_meeting_rq = count_meeting_rq / len(valid_values) if valid_values else 0
            sqd_curve.append(fraction_meeting_rq)
        sqd_curves[time] = sqd_curve

    return relative_qualities, sqd_curves


def plot_sqd(relative_qualities, sqd_curves):
    plt.figure(figsize=(10, 6))

    for fixed_time, sqd_curve in sqd_curves.items():
        plt.plot(abs(relative_qualities * 100), sqd_curve, label=f'{fixed_time}s')

    plt.title('Solution Quality Distribution (SQD) at Different Runtimes (GA large_3)')
    plt.xlabel('Relative Solution Quality [%]')
    plt.ylabel('P(solve)')
    plt.legend()
    plt.grid(True, which="both", linestyle='--')
    plt.ylim(0, 1)
    # plt.xlim(5, 15)
    plt.show()

# Define the directory, file pattern, and optimal value
directory = 'Output/trace_files/LS1/large_scale/'
file_pattern = 'large_3_LS1_1800_*'
optimal_value = 28857
fixed_times = [50, 100, 200, 300, 400, 500]  # Fixed times in seconds

# Load and process the data
all_data = load_data(directory, file_pattern)
relative_qualities, sqd_curves = calculate_sqd(all_data, optimal_value, fixed_times)


# Plot the SQD curve
plot_sqd(relative_qualities, sqd_curves)
