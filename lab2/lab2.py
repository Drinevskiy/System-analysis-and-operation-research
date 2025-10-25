import numpy as np
from typing import Tuple, List

def resource_allocation(A: np.ndarray) -> Tuple[float, List[int], np.ndarray, np.ndarray]:
    if A.ndim != 2:
        raise ValueError("Матрица A должна быть двумерной")
        
    P = A.shape[0] - 1
    Q = A.shape[1] - 1

    B = np.zeros((P + 1, Q + 1))
    C = np.zeros((P + 1, Q + 1), dtype=int)

    for q in range(Q + 1):
        B[1][q] = A[1][q]
        C[1][q] = q

    for p in range(2, P + 1):
        for q in range(Q + 1):
            max_benefit = -10000
            best_i = -1
            for i in range(q + 1):
                current_benefit = A[p][i] + B[p - 1][q - i]
                if current_benefit > max_benefit:
                    max_benefit = current_benefit
                    best_i = i
            B[p][q] = max_benefit
            C[p][q] = best_i

    distribution = [0] * P
    q_rest = Q
    for p in range(P, 0, -1):
        resources_for_p = C[p][q_rest]
        distribution[p - 1] = resources_for_p
        q_rest -= resources_for_p
        
    return B[P][Q], distribution, B, C

A = np.array([
    [0, 0, 0, 0], 
    [0, 1, 2, 3], 
    [0, 0, 1, 2], 
    [0, 2, 2, 3]  
])

max_benefit, optimal_distribution, B, C = resource_allocation(A)

print("Матрица B (Максимальные прибыли на каждом шаге):")
print(B)
print("\nМатрица C (Оптимальное количество ресурсов для агента p на каждом шаге):")
print(C)

print(f"Максимальная суммарная прибыль: {max_benefit}")
print("Оптимальное распределение ресурсов:")
for i, resources in enumerate(optimal_distribution):
    print(f"  Агенту {i + 1} выделено: {resources} единиц ресурсов")