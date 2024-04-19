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
            chromosome = self.generate_valid_chromosome()
            population.append(chromosome)
        return population

    def generate_valid_chromosome(self):
        chromosome = [0] * len(self.items)
        items_indices = list(range(len(self.items)))
        random.shuffle(items_indices)  # Randomize item order to ensure diversity
        total_weight = 0
        for i in items_indices:
            if total_weight + self.items[i]['weight'] <= self.capacity:
                chromosome[i] = 1
                total_weight += self.items[i]['weight']
        return chromosome

    def calculate_fitness(self, chromosome):
        total_value = sum(self.items[i]['value'] for i in range(len(chromosome)) if chromosome[i] == 1)
        return total_value

    def select_chromosomes(self, population):
        fitness_values = [self.calculate_fitness(chromosome) for chromosome in population]
        max_fitness = max(fitness_values)
        weights = [f if f > 0 else 0.1 for f in fitness_values]  # Use a small weight for zero fitness to avoid division by zero
        selected_indices = random.choices(range(len(population)), weights=weights, k=2)
        return population[selected_indices[0]], population[selected_indices[1]]

    def crossover(self, parent1, parent2):
        child1, child2 = parent1[:], parent2[:]  # Start with copies of parents
        crossover_point = random.randint(1, len(self.items) - 2)
        child1[crossover_point:], child2[crossover_point:] = parent2[crossover_point:], parent1[crossover_point:]
        return self.generate_valid_chromosome_based_on(child1), self.generate_valid_chromosome_based_on(child2)

    def generate_valid_chromosome_based_on(self, chromosome):
        # Ensure the chromosome is valid with respect to the capacity
        if self.calculate_weight(chromosome) <= self.capacity:
            return chromosome
        return self.generate_valid_chromosome()  # Regenerate if invalid

    def calculate_weight(self, chromosome):
        return sum(self.items[i]['weight'] for i in range(len(chromosome)) if chromosome[i] == 1)

    def mutate(self, chromosome):
        for i in range(len(chromosome)):
            if random.uniform(0, 1) < self.mutation_rate:
                chromosome[i] = 1 - chromosome[i]
        return self.generate_valid_chromosome_based_on(chromosome)  # Ensure validity after mutation

    def get_best(self, population):
        fitness_values = [self.calculate_fitness(chromosome) for chromosome in population]
        max_value = max(fitness_values)
        max_index = fitness_values.index(max_value)
        return population[max_index], max_value

    def solve(self, cut_off_time):
        start_time = time.time()
        population = self.generate_population()
        best_solution, best_quality = self.get_best(population)
        trace = [(time.time() - start_time, best_quality)]  # Initialize trace with the initial best quality

        while time.time() - start_time < cut_off_time:
            parent1, parent2 = self.select_chromosomes(population)
            child1, child2 = self.crossover(parent1, parent2)
            child1 = self.mutate(child1)
            child2 = self.mutate(child2)
            population.extend([child1, child2])
            
            # Sort by fitness and truncate to maintain population size
            population.sort(key=self.calculate_fitness, reverse=True)
            population = population[:self.population_size]

            current_best, current_quality = self.get_best(population)
            if current_quality > best_quality:
                best_solution = current_best
                best_quality = current_quality
                trace.append((time.time() - start_time, best_quality))  # Log improvement

        solution = {'selected_items': best_solution, 'quality': best_quality}
        return solution, trace