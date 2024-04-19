import random
import time

class LocalSearch2:

    def __init__(self, items, capacity, seed, num_restarts=100):
        self.seed = seed
        random.seed(seed)
        self.items = items
        self.capacity = capacity
        self.num_restarts = num_restarts

    def generate_initial_solution(self):
        """ Generates initial solutions randomly to maintain diversity """
        solution = [0] * len(self.items)
        weight = 0
        value = 0
        item_indices = list(range(len(self.items)))
        random.shuffle(item_indices)  # Shuffle to randomize the insertion order
        for i in item_indices:
            if weight + self.items[i]['weight'] <= self.capacity:
                solution[i] = 1
                weight += self.items[i]['weight']
                value += self.items[i]['value']
        return solution, weight, value

    def find_best_neighbor(self, current_solution, current_weight, current_value):
        """ Iterate over all items and try toggling each to find the best neighbor """
        best_solution = current_solution[:]
        best_value = current_value
        best_weight = current_weight
        for i in range(len(self.items)):
            neighbor_solution = current_solution[:]
            # Toggle the current item
            neighbor_solution[i] = 1 - neighbor_solution[i]
            new_weight = current_weight + (self.items[i]['weight'] if neighbor_solution[i] == 1 else -self.items[i]['weight'])
            new_value = current_value + (self.items[i]['value'] if neighbor_solution[i] == 1 else -self.items[i]['value'])

            if new_weight <= self.capacity and new_value > best_value:
                best_solution = neighbor_solution[:]
                best_value = new_value
                best_weight = new_weight
        return best_solution, best_weight, best_value

    def solve(self, cut_off_time):
        best_global_solution = []
        best_global_value = 0
        best_global_weight = 0
        trace = []
        start_time = time.time()

        for _ in range(self.num_restarts):
            current_solution, current_weight, current_value = self.generate_initial_solution()
            trace.append((time.time() - start_time, current_value))  

            while time.time() - start_time < cut_off_time:
                new_solution, new_weight, new_value = self.find_best_neighbor(current_solution, current_weight, current_value)
                if new_value > current_value:
                    current_solution = new_solution
                    current_weight = new_weight
                    current_value = new_value
                    trace.append((time.time() - start_time, current_value)) 
                else:
                    break 

            if current_value > best_global_value:
                best_global_solution = current_solution
                best_global_value = current_value
                best_global_weight = current_weight

        solution = {'selected_items': best_global_solution, 'quality': best_global_value}
        return solution, trace
