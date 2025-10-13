import numpy as np
import math
from lab1.simplex_method import start_simplex_method


def create_gomory_cut(Q_k, x_B_k, x_N_indices, n_total):
    fractional_coeffs = []
    for coeff in Q_k:
        fractional_part = coeff - math.floor(coeff)
        fractional_coeffs.append(fractional_part)
    
    fractional_rhs = x_B_k - math.floor(x_B_k)
    
    full_coeffs = np.zeros(n_total)
    for i, var_idx in enumerate(x_N_indices):
        full_coeffs[var_idx] = fractional_coeffs[i]
        
    cut_coeffs = fractional_coeffs
    
    rhs = fractional_rhs
    
    print("Отсекающее ограничение Гомори:")
    equation_parts = []
    for i in range(n_total):
        coeff = full_coeffs[i]
        if abs(coeff) < 1e-10: 
            coeff_str = "0"
        else:
            coeff_str = f"{coeff:.4f}"
        equation_parts.append(f"{coeff_str}·x{i+1}")
    
    equation = " + ".join(equation_parts) + " - s"
    equation += f" = {f"{fractional_rhs:.4f}"}"
    print(equation)
    return np.array(cut_coeffs), rhs

def restriction_of_gomori(c, A, b):
    result = start_simplex_method(c, A, b)
    if isinstance(result, str):
        print(result) 
    else:
        x, B, A_new, b_new = result 

    if np.isscalar(B):
        B = np.array([B])
    elif isinstance(B, list):
        B = np.array(B)

    j0 = -1
    x_i_selected = 0
    for index, x_i in enumerate(x):
        if not x_i.is_integer():
            j0 = index
            x_i_selected = x_i
            break
    if j0 == -1:
        print(x)
        return
    if j0 in B:
        indices_in_B = np.where(B == j0)[0]
        if len(indices_in_B) > 0:
            k = indices_in_B[0]

    n = A_new.shape[1] 
    j_nb = [i for i in range(n) if all(bi != i for bi in B)] 
    A_B = A[:, B]
    A_N = A[:, j_nb]
    try:
        A_B_inv = np.linalg.inv(A_B)
    except np.linalg.LinAlgError:
        print("Матрица A_B вырождена, обратной матрицы не существует")
        return
    Q = A_B_inv @ A_N
    l = Q[k, :]
    cut_coeffs, rhs = create_gomory_cut(l, x_i_selected, j_nb, n)

examples = [
    (np.array([0, 1, 0, 0], dtype=float),
     np.array([[3, 2, 1, 0], 
               [-3, 2, 0, 1]], dtype=float), 
     np.array([6, 0], dtype=float)),
]

for c, A, b in examples:
    restriction_of_gomori(c, A, b)
    