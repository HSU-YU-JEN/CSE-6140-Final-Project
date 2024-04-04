# local_search_1.py
import random
import argparse
import time

# Assuming utils.py contains necessary functions like load_dataset
from utils.utils import load_dataset, save_solution, save_trace

class LocalSearch1:
    def __init__(self, items, capacity, seed, population_size=100, generations=100, mutation_rate=0.01):
        random.seed(seed)
        self.items = items
        self.capacity = capacity
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate

    def generate_individual(self):
        return [random.randint(0, 1) for _ in range(len(self.items))]

    def fitness(self, individual):
        value = sum(item['value'] * gene for item, gene in zip(self.items, individual))
        weight = sum(item['weight'] * gene for item, gene in zip(self.items, individual))
        if weight > self.capacity:
            return 0  # Simple penalty
        return value

    def selection(self, population, fitnesses, k=3):
        selected = random.choices(list(zip(population, fitnesses)), k=k)
        return max(selected, key=lambda x: x[1])[0]

    def crossover(self, parent1, parent2):
        point = random.randint(1, len(parent1) - 1)
        return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]

    def mutate(self, individual):
        return [gene if random.random() > self.mutation_rate else 1-gene for gene in individual]

    def solve(self):
        population = [self.generate_individual() for _ in range(self.population_size)]
        best_fitness_over_time = []
        start_time = time.time()

        for generation in range(self.generations):
            new_population = []
            fitnesses = [self.fitness(ind) for ind in population]
            for _ in range(self.population_size // 2):  # Ensuring population size remains constant
                parent1 = self.selection(population, fitnesses)
                parent2 = self.selection(population, fitnesses)
                offspring1, offspring2 = self.crossover(parent1, parent2)
                new_population.append(self.mutate(offspring1))
                new_population.append(self.mutate(offspring2))
            population = new_population
            best_fitness = max(fitnesses)
            best_fitness_over_time.append((time.time() - start_time, best_fitness))

        best_index = fitnesses.index(max(fitnesses))
        return population[best_index], best_fitness_over_time

def main(filename, cut_off_time, seed):
    items, capacity = load_dataset(filename)
    ga = LocalSearch1(items, capacity, seed)
    best_solution, trace = ga.solve()

    # Save the solution and trace according to the project specifications
    save_solution(filename, 'LS1', cut_off_time, seed, best_solution)
    save_trace(filename, 'LS1', cut_off_time, seed, trace)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Genetic Algorithm for the Knapsack Problem")
    parser.add_argument("-inst", type=str, required=True, help="Dataset filename")
    parser.add_argument("-time", type=int, required=True, help="Cut-off time in seconds")
    parser.add_argument("-seed", type=int, required=True, help="Random seed")
    
    args = parser.parse_args()
    main(args.inst, args.time, args.seed)
