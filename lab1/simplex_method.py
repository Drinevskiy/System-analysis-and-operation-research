import numpy as np

def multiplicate_matrix(q_matrix, a_reverse_matrix, index):
    q_rows, q_cols = q_matrix.shape
    result_matrix = np.zeros((q_rows, q_cols))
    for i in range(q_rows):
        for j in range(q_cols):
            # Диагональный элемент Q матрицы
            result_matrix[i, j] +=  q_matrix[i, i] * a_reverse_matrix[i, j]
            if i != index:
                # i-ый элемент Q матрицы
                result_matrix[i, j] +=  q_matrix[i, index] * a_reverse_matrix[index, j]

    return result_matrix
    
def custom_inverse_matrix(matrix, x, i):
    if matrix.shape[0] != len(x):
        raise ValueError("Размеры вектора x должны соответствовать количеству строк матрицы.")
    if np.linalg.det(matrix) == 0:
        raise np.linalg.LinAlgError("Определитель матрицы равен нулю; матрица не имеет обратной.")
    matrix = np.linalg.inv(matrix)
    l_vector = matrix @ x
    temp = l_vector[i]
    if temp == 0:
        raise ValueError("Матрица не обратима. l[i] = 0")
    l_vector[i] = -1
    l_vector_hat = -1 * l_vector / temp
    e_matrix = np.eye(len(x))
    q_matrix = e_matrix.copy()
    q_matrix[:, i] = l_vector_hat
    return multiplicate_matrix(q_matrix, matrix, i)

def simplex_method(c, A, x, B, firstIter = True, j0 = -1, i = -1):
    # 1
    if firstIter:
        A_B = A[:, B]
        A_B_inverse = np.linalg.inv(A_B)
    else:
        A_B = A[:, B]
        A_B_inverse = custom_inverse_matrix(A_B, A[:, j0], i)
    # 2
    c_B = c[B]
    # 3 вектор потенциалов
    U = c_B @ A_B_inverse
    # 4 вектор оценок
    delta = U @ A - c
    # 5 - 6
    j0 = -1
    for index, value in enumerate(delta):
        if value < 0:
            j0 = index
            break
    if j0 == -1:
        return x, B
    # 7
    z = A_B_inverse @ A[:,j0]
    # 8
    tetta = []
    for index, value in enumerate(z):
        if value > 0:
            tetta_i = x[B[index]] / value  # Индекс B[i] соответствует базисному индексу
        else:
            tetta_i = np.inf
        tetta.append(tetta_i)
    # 9
    tetta0 = min(tetta)
    # 10
    if tetta0 == np.inf:
        return "Целевая функция не ограничена сверху на множестве допустимых планов"
    # 11
    tetta0_index = tetta.index(tetta0)
    j_star = B[tetta0_index]
    # 12
    B[tetta0_index] = j0
    # 13
    x[j0] = tetta0
    for index, value in enumerate(z):
        if tetta0_index != index:
            x[B[index]] = x[B[index]] - tetta0 * value
    x[j_star] = 0
    return simplex_method(c, A, x, B, False, j0, tetta0_index)

def start_simplex_method(c, A, b):
    n = len(c)
    m = len(b)
    # 1
    for index, bi in enumerate(b):
        if bi < 0:
            b[index] = -1 * bi
            A[index, :] = -1 * A[index, :]
    # 2
    c_wave = np.concatenate((np.zeros(n), -1 * np.ones(m)))
    A_wave = np.hstack((A, np.eye(m)))
    # 3
    x_wave = np.concatenate((np.zeros(n), b))
    B_wave = [n + i for i in range(m)]
    # 4

    result = simplex_method(c_wave, A_wave, x_wave, B_wave)
    # Проверка, является ли возвращаемое значение строкой (что указывает на ошибку)
    if isinstance(result, str):
        print(result) 
    else:
        x_wave, B = result 
    # 5
    for i in range(n, n + m):
        if x_wave[i] != 0:
            return "Задача несовместна."
    # 6
    x = x_wave[:n]
    # 7
    while True:
        if all(bi < n for bi in B):
            return x, B, A, b
    # 8    
        j_k = max(B)
        k = B.index(j_k) 
    # 9
        j_nb = [i for i in range(n) if all(bi != i for bi in B)] 
        A_wave_B = A_wave[:,B]
        A_wave_B_inv = np.linalg.inv(A_wave_B)
        l = [(j, A_wave_B_inv @ A_wave[:, j]) for j in j_nb]
    # 10
        found = False 
        for j, l_j in l:
            if(l_j[k] != 0):
                B[k] = j 
                found = True
        if not found:
            index = j_k - n
            A = np.delete(A, index, axis=0)
            b = np.delete(b, index)
            B = np.delete(B, k)
            A_wave = np.delete(A_wave, index, axis=0)
