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
            value, weight = map(int, file.readline().strip().split())
            items.append({'value': value, 'weight': weight})

    return items, capacity


def save_solution(filename, method, cutoff, seed, solution):
    """
    Saves the solution to a .sol file following the project's naming conventions.
    """
    sol_filename = f"output/solution_files/{method}/{filename}_{method}_{cutoff}_{seed}.sol"
    with open(sol_filename, 'w') as f:
        f.write(f"{solution['quality']}\n")
        f.write(",".join(map(str, solution['selected_items'])))


def save_trace(filename, method, cutoff, seed, trace):
    """
    Saves the solution trace to a .trace file following the project's naming conventions.
    """
    trace_filename = f"output/trace_files/{method}/{filename}_{method}_{cutoff}_{seed}.trace"
    with open(trace_filename, 'w') as f:
        for timestamp, quality in trace:
            f.write(f"{timestamp},{quality}\n")