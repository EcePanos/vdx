import random

# Define the problem-specific variables
input = [5, 4, 7]
ground_truth = 5
num_experts = 3  # Number of experts or voters
population_size = 20  # Number of chromosomes in each generation
max_generations = 100  # Maximum number of generations
mutation_rate = 0.1  # Probability of mutation
fitness_threshold = 0.99  # Termination condition based on fitness

# Define the fitness function
def calculate_fitness(chromosome):
    # Calculate the fitness as the difference between the average of the
    # input, weighed by the chromosome, and the ground truth
    votes = [input[i] * chromosome[i] for i in range(num_experts)]
    average = sum(votes) / sum(chromosome)
    return 1 - abs(average - ground_truth) / ground_truth

# Initialize the population
def initialize_population():
    population = []
    for _ in range(population_size):
        chromosome = [random.uniform(0, 1) for _ in range(num_experts)]
        population.append(chromosome)
    return population

# Select parents using tournament selection
def tournament_selection(population, tournament_size):
    parents = []
    for _ in range(2):  # Select 2 parents for reproduction
        tournament = random.sample(population, tournament_size)
        tournament.sort(key=lambda x: calculate_fitness(x), reverse=True)
        parents.append(tournament[0])
    return parents

# Perform crossover between parents to produce offspring
def crossover(parents):
    offspring = []
    parent1, parent2 = parents
    crossover_point = random.randint(1, num_experts - 1)
    offspring.append(parent1[:crossover_point] + parent2[crossover_point:])
    offspring.append(parent2[:crossover_point] + parent1[crossover_point:])
    return offspring

# Perform mutation on offspring
def mutate(offspring):
    mutated_offspring = []
    for chromosome in offspring:
        mutated_chromosome = []
        for gene in chromosome:
            if random.random() < mutation_rate:
                mutated_chromosome.append(random.uniform(0, 1))
            else:
                mutated_chromosome.append(gene)
        mutated_offspring.append(mutated_chromosome)
    return mutated_offspring

# Main genetic algorithm function
def genetic_algorithm_weighted_voting():
    population = initialize_population()
    best_chromosome = None
    best_fitness = 0.0
    generation = 0

    while generation < max_generations:
        offspring = []
        while len(offspring) < population_size:
            parents = tournament_selection(population, 3)
            new_offspring = crossover(parents)
            mutated_offspring = mutate(new_offspring)
            offspring.extend(mutated_offspring)

        population = offspring
        generation += 1

        # Evaluate fitness of the new population
        for chromosome in population:
            fitness = calculate_fitness(chromosome)
            if fitness > best_fitness:
                best_fitness = fitness
                best_chromosome = chromosome

            if fitness >= fitness_threshold:
                return best_chromosome, best_fitness, generation

    return best_chromosome, best_fitness, generation

# Run the genetic algorithm
best_chromosome, best_fitness, generations = genetic_algorithm_weighted_voting()
output = sum([input[i] * best_chromosome[i] for i in range(num_experts)]) / sum(best_chromosome)

# Print the results
print("Best Chromosome:", best_chromosome)
print("Best Fitness:", best_fitness)
print("Generations:", generations)
print("Output:", output)
