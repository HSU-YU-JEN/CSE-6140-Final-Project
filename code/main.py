import sys
from utils.utils import load_dataset, save_solution, save_trace
from algorithms.branch_and_bound import BranchAndBound
from algorithms.approximation import ApproximationAlgorithm
from algorithms.local_search_1 import LocalSearch1
from algorithms.local_search_2 import LocalSearch2

# Assume that utils and algorithms are in the same directory as main.py or adjust sys.path accordingly.

def main():
    # Check the number of command-line arguments
    if len(sys.argv) not in [5, 6]:
        print("Usage: python main.py <dataset_path> <algorithm> <cut_off_time> <random_seed>")
        print("The <random_seed> is optional and only needed for LS1 and LS2 algorithms.")
        sys.exit(1)

    dataset_path, algorithm_choice, cut_off_time = sys.argv[1:4]
    random_seed = None

    if algorithm_choice in ['LS1', 'LS2']:
        if len(sys.argv) == 6:
            random_seed = int(sys.argv[5])
        else:
            print("Error: LS1 and LS2 algorithms require a random seed.")
            sys.exit(1)
    elif len(sys.argv) == 5:
        print("Error: BnB and Approx algorithms do not require a random seed.")
        sys.exit(1)

    # Convert cut_off_time to int
    cut_off_time = int(cut_off_time)

    # Load dataset
    items, capacity = load_dataset(dataset_path)

    # Select and run the algorithm
    solution = trace = None
    if algorithm_choice == 'BnB':
        algorithm = BranchAndBound(items, capacity)
        solution, trace = algorithm.solve(cut_off_time)

    elif algorithm_choice == 'Approx':
        algorithm = ApproximationAlgorithm(items, capacity)
        solution, trace = algorithm.solve(cut_off_time)

    elif algorithm_choice == 'LS1':
        algorithm = LocalSearch1(items, capacity, random_seed)
        solution, trace = algorithm.solve(cut_off_time)

    elif algorithm_choice == 'LS2':
        algorithm = LocalSearch2(items, capacity, random_seed)
        solution, trace = algorithm.solve(cut_off_time)
        
    else:
        print(f"Error: Unknown algorithm choice '{algorithm_choice}'.")
        print("Valid options are: BnB, Approx, LS1, LS2.")
        sys.exit(1)

    # Save output files
    save_solution(dataset_path, algorithm_choice, cut_off_time, random_seed, solution)
    save_trace(dataset_path, algorithm_choice, cut_off_time, random_seed, trace)

if __name__ == "__main__":
    main()
