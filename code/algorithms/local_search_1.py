import random
import time

class LocalSearch1:
    def __init__(self, items, capacity, seed, population_size=10000, mutation_rate=0.01):
        random.seed(seed)
        self.items = items
        self.capacity = capacity
        self.population_size = population_size
        self.mutation_rate = mutation_rate

    def generate_individual(self):
        """Generates a random individual based on the number of items."""
        individual = []
        for item in self.items:
            if random.random() < 0.5:  # Adjust probability as necessary to improve initial feasibility
                individual.append(1)
            else:
                individual.append(0)
        return individual

    def fitness(self, individual):
        """Calculates the fitness of an individual as its total value, penalizing those that exceed capacity."""
        total_value = sum(item['value'] * gene for item, gene in zip(self.items, individual))
        total_weight = sum(item['weight'] * gene for item, gene in zip(self.items, individual))
        if total_weight > self.capacity:
            return 0  
        return total_value

    def selection(self, population, fitnesses):
        """Selects parents for crossover based on their fitness."""
        selected = random.choices(population, weights=fitnesses, k=2)
        return selected

    def crossover(self, parent1, parent2):
        """Performs a single point crossover between two parents."""
        point = random.randint(1, len(parent1) - 1)
        return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]

    def mutate(self, individual):
        """Mutates an individual by flipping each gene with a probability equal to the mutation rate."""
        return [gene if random.random() > self.mutation_rate else 1-gene for gene in individual]

    def solve(self, cut_off_time):
        start_time = time.time()
        population = [self.generate_individual() for _ in range(self.population_size)]
        trace = []
        best_individual, best_fitness = None, -1

        while time.time() - start_time < cut_off_time:
            fitnesses = [self.fitness(ind) for ind in population]
            new_population = []
            for _ in range(self.population_size // 2):
                parents = self.selection(population, fitnesses)
                offspring1, offspring2 = self.crossover(parents[0], parents[1])
                new_population.extend([self.mutate(offspring1), self.mutate(offspring2)])

            population = new_population
            current_best_fitness = max(fitnesses)
            if current_best_fitness > best_fitness:
                best_fitness = current_best_fitness
                best_individual = population[fitnesses.index(best_fitness)]
                trace.append((time.time() - start_time, best_fitness))

        solution = {'selected_items': best_individual, 'quality': best_fitness}
        return solution, trace
