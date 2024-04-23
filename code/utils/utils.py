import os

def load_dataset(filename):
    """
    Reads a dataset file and returns a list of items and the knapsack capacity.

    Each item is represented as a dictionary with 'value' and 'weight'.
    """
    filename = os.path.join('DATASET', filename)
    items = []
    with open(filename, 'r') as file:

        num_items, capacity = map(int, file.readline().strip().split())
        
        for _ in range(num_items):
            value, weight = map(float, file.readline().strip().split())
            items.append({'value': value, 'weight': weight})

    return items, capacity



def save_solution(filename, method, cutoff, seed, solution):
    """
    Saves the solution to a .sol file following the project's naming conventions.
    """
    
    base_dir = os.path.abspath('Output')
    full_path = os.path.join(base_dir, 'solution_files', method, os.path.dirname(filename))

    # Ensure the entire directory path exists
    os.makedirs(full_path, exist_ok=True)

    # Construct the full path for the solution file
    if method in ['BnB', 'Approx']:
        sol_filename = os.path.join(full_path, f"{os.path.basename(filename)}_{method}_{cutoff}.sol")
    else:
        sol_filename = os.path.join(full_path, f"{os.path.basename(filename)}_{method}_{cutoff}_{seed}.sol")

    # Write the solution file
    with open(sol_filename, 'w') as f:
        f.write(f"{solution['quality']}\n")
        f.write(",".join(map(str, solution['selected_items'])))

    print(f"File written successfully to: {sol_filename}")



def save_trace(filename, method, cutoff, seed, trace):

    base_dir = os.path.abspath('Output')
    full_path = os.path.join(base_dir, 'trace_files', method, os.path.dirname(filename))

    # Ensure the entire directory path exists
    os.makedirs(full_path, exist_ok=True)

    # Construct the full path for the solution file
    if method in ['BnB', 'Approx']:
        trace_filename = os.path.join(full_path, f"{os.path.basename(filename)}_{method}_{cutoff}.trace")
    else:
        trace_filename = os.path.join(full_path, f"{os.path.basename(filename)}_{method}_{cutoff}_{seed}.trace")

    # Write the solution file
    with open(trace_filename, 'w') as f:
        for timestamp, quality in trace:
            f.write(f"{timestamp},{quality}\n")

    print(f"File written successfully to: {trace_filename}")
    
