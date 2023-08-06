import numpy as np


def get_best_genome(genomes):
    best_fitness = float('-inf')
    best_genome = None
    for genome in genomes:
        if genome.fitness > best_fitness:
            best_genome = genome
    return best_genome


def transform_bitstring_to_layers_tuple(bitstring):
    flat_array = np.sum(bitstring, axis=0)
    return flat_array[flat_array > 0]
