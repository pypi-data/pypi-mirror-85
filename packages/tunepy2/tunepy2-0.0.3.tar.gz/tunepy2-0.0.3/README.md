[![Build Status](https://travis-ci.org/efortner/tunepy.svg?branch=master)](https://travis-ci.org/efortner/tunepy)
[![Coverage Status](https://coveralls.io/repos/github/efortner/tunepy/badge.svg?branch=master)](https://coveralls.io/github/efortner/tunepy?branch=master)
# tunepy2
Provides a variety of extensible and easy to use bitstring optimizers as well as several machine learning convenience
utilities for model optimization.

## Dependencies
* python >= 3.7
* numpy >= 1.19.2
* scikit-learn >= 0.23.2

## Installation
```
pip install tunepy2
```

## Basic Usage
All bitstring optimizers extend the Abstract Base Class (ABC) [AbstractOptimizer](https://github.com/efortner/tunepy/blob/fe28cfde8f08438d21d9c58d879b24a327b5e737/tunepy2/interfaces/abstract_optimizer.py).
The most basic versions of all optimizers are accessed through static build methods.

### Importing tunepy2
```python
import tunepy2 as tp
```

### Basic Prebuilt Optimizers
* Random Restart Hill Climber ([`tp.new_random_restart_hill_climber`](https://github.com/efortner/tunepy/blob/master/tunepy2/prebuilt/prebuilt_optimizers.py#L16))
* Simulated Annealer ([`tp.new_simulated_annealer`](https://github.com/efortner/tunepy/blob/master/tunepy2/prebuilt/prebuilt_optimizers.py#L78))
* Basic Hill Climber ([`tp.new_hill_climber`](https://github.com/efortner/tunepy/blob/master/tunepy2/prebuilt/prebuilt_optimizers.py#L133))
* Genetic Algorithm ([`tp.new_genetic_optimizer`](https://github.com/efortner/tunepy/blob/master/tunepy2/prebuilt/prebuilt_optimizers.py#L180))

Fitness functions are assumed have an array-like passed in as the first argument and return a fitness value.