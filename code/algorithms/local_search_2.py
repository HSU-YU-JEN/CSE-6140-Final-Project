import random
import time

class LocalSearch2:

    def __init__(self, items, capacity, seed):
        self.seed = seed
        random.seed(seed)
        self.items = items
        self.capacity = capacity

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
        best_solution = current_solution[:]
        best_value = current_value
        best_weight = current_weight
        for i in range(len(self.items)):
            neighbor_solution = current_solution[:]
            neighbor_solution[i] = 1 - neighbor_solution[i]
            if neighbor_solution[i] == 1:
                neighbor_weight = current_weight + self.items[i]['weight']  # Adding item
                neighbor_value = current_value + self.items[i]['value']      # Adding item
            else:
                neighbor_weight = current_weight - self.items[i]['weight']  # Removing item
                neighbor_value = current_value - self.items[i]['value']     # Removing item

            if neighbor_weight <= self.capacity and neighbor_value > best_value:
                best_solution = neighbor_solution[:]
                best_value = neighbor_value
                best_weight = neighbor_weight
        return best_solution, best_weight, best_value

    def solve(self, cut_off_time):
        best_global_solution = []
        best_global_value = 0
        best_global_weight = 0
        trace = []
        start_time = time.time()

        while time.time() - start_time < cut_off_time:
            current_solution, current_weight, current_value = self.generate_initial_solution()
            trace.append((time.time() - start_time, current_value))  
            while True:
                new_solution, new_weight, new_value = self.find_best_neighbor(current_solution, current_weight, current_value)
                if new_value > current_value and new_weight <= self.capacity:
                    current_solution = new_solution
                    current_weight = new_weight
                    current_value = new_value
                else:
                    break
            if current_value > best_global_value and current_weight <= self.capacity:
                best_global_solution = current_solution
                best_global_value = current_value
                best_global_weight = current_weight
                trace.append((time.time() - start_time, new_value))

        solution = {'selected_items': best_global_solution, 'quality': best_global_value}
        return solution, trace