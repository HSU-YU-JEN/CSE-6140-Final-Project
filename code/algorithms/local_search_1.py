import random
import time

class LocalSearch1:
    def __init__(self, items, capacity, seed, population_size=1000, mutation_rate=0.01):
        self.seed = seed
        random.seed(seed)
        self.items = items
        self.capacity = capacity
        self.population_size = population_size
        self.mutation_rate = mutation_rate

    def generate_population(self):
        population = []
        for _ in range(self.population_size):
            genes = [0, 1]
            chromosome = []
            for _ in range(len(self.items)):
                chromosome.append(random.choice(genes))
            population.append(chromosome)
        return population

    def calculate_fitness(self, chromosome):
        total_weight = 0
        total_value = 0
        for i in range(len(chromosome)):
            if chromosome[i] == 1:
                total_weight += self.items[i]['weight']
                total_value += self.items[i]['value']
        if total_weight > self.capacity:
            return 0
        else:
            return total_value

    def select_chromosomes(self, population):
        fitness_values = [self.calculate_fitness(chromosome) for chromosome in population]
        total_fitness = sum(max(0, f) for f in fitness_values)  # Only sum positive fitness values
        if total_fitness > 0:
            fitness_proportions = [f / total_fitness for f in fitness_values if f > 0]
        else:
            fitness_proportions = [1 / len(population)] * len(population)  # Uniform distribution if all fitnesses are zero
        selected_indices = random.choices(range(len(population)), weights=fitness_proportions, k=2)
        return population[selected_indices[0]], population[selected_indices[1]]


    def crossover(self, parent1, parent2):
        crossover_point = random.randint(0, len(self.items) - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2

    def mutate(self, chromosome):
        for i in range(len(chromosome)):
            if random.uniform(0, 1) < self.mutation_rate:
                chromosome[i] = 1 - chromosome[i]
        return chromosome


    def get_best(self, population):
        fitness_values = [self.calculate_fitness(chromosome) for chromosome in population]
        max_value = max(fitness_values)
        max_index = fitness_values.index(max_value)
        return population[max_index], max_value

    def solve(self, cut_off_time):
        start_time = time.time()
        population = self.generate_population()
        best_solution, best_quality = self.get_best(population)
        trace = []

        while time.time() - start_time < cut_off_time:
            parent1, parent2 = self.select_chromosomes(population)
            child1, child2 = self.crossover(parent1, parent2)
            if random.uniform(0, 1) < self.mutation_rate:
                child1 = self.mutate(child1)
            if random.uniform(0, 1) < self.mutation_rate:
                child2 = self.mutate(child2)
            population = [child1, child2] + population[2:]

            current_best, current_quality = self.get_best(population)
            if current_quality > best_quality:
                best_solution = current_best
                best_quality = current_quality
                trace.append((time.time() - start_time, best_quality))

        solution = {'selected_items': best_solution, 'quality': best_quality}
        return solution, trace
