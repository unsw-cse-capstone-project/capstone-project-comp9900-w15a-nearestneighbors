import numpy as np


parent1 = [1, 2, 3, 4]
parent2 = [11, 12, 13, 14]
result = np.random.choice(np.concatenate([parent1,parent2]), len(parent1) + len(parent2), replace=False)

print(result)