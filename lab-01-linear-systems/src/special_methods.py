from math import sqrt

from .matrix_utils import back_substitution, dot, euclidean_norm


# Метод квадратных корней, раскладываем симметричную матрицу на S^T * D * S.
def square_roots_decomposition(matrix):
    size = len(matrix)
    upper = []
    for row in range(size):
        upper.append([0.0] * size)
    signs = [0.0] * size

    for row in range(size):
        diagonal = matrix[row][row]
        for index in range(row):
            diagonal -= signs[index] * upper[index][row] ** 2

        if abs(diagonal) < 1e-14:
            raise ValueError("Метод квадратных корней: малый ведущий элемент")

        if diagonal > 0:
            signs[row] = 1.0
        else:
            signs[row] = -1.0
        upper[row][row] = sqrt(abs(diagonal))

        for column in range(row + 1, size):
            known = 0.0
            for index in range(row):
                known += signs[index] * upper[index][row] * upper[index][column]
            upper[row][column] = (matrix[row][column] - known) / (signs[row] * upper[row][row])

    return upper, signs


# Решаем систему после разложения, сначала идём сверху вниз, потом снизу вверх.
def solve_square_roots(matrix, rhs):
    upper, signs = square_roots_decomposition(matrix)
    size = len(rhs)
    y = [0.0] * size

    for row in range(size):
        known = 0.0
        for column in range(row):
            known += upper[column][row] * signs[column] * y[column]
        y[row] = (rhs[row] - known) / (upper[row][row] * signs[row])

    return back_substitution(upper, y)


# Ортогонализация, делаем векторы взаимно перпендикулярными и находим решение.
def solve_orthogonalization(matrix, rhs):
    size = len(matrix)
    rows = []
    for index in range(size):
        row = matrix[index][:]
        row.append(-rhs[index])
        rows.append(row)

    last_row = [0.0] * (size + 1)
    last_row[-1] = 1.0
    rows.append(last_row)
    basis = []

    for row in rows:
        vector = row[:]
        for previous in basis:
            projection = dot(vector, previous)
            for index in range(len(vector)):
                vector[index] -= projection * previous[index]

        length = euclidean_norm(vector)
        if length < 1e-14:
            raise ValueError("При ортогонализации получен нулевой вектор")

        for index in range(len(vector)):
            vector[index] /= length
        basis.append(vector)

    result = []
    last = basis[-1]
    for index in range(size):
        result.append(last[index] / last[-1])
    return result


# Метод прогонки, решаем трёхдиагональную систему прямой и обратной прогонкой.
def thomas_method(matrix, rhs):
    size = len(matrix)
    alpha = [0.0] * size
    beta = [0.0] * size

    if abs(matrix[0][0]) < 1e-14:
        raise ValueError("Прогонка: нулевой знаменатель")
    alpha[0] = -matrix[0][1] / matrix[0][0]
    beta[0] = rhs[0] / matrix[0][0]

    for row in range(1, size):
        lower = matrix[row][row - 1]
        upper = 0.0
        if row < size - 1:
            upper = matrix[row][row + 1]

        denominator = matrix[row][row] + lower * alpha[row - 1]
        if abs(denominator) < 1e-14:
            raise ValueError("Прогонка: нулевой знаменатель")

        alpha[row] = -upper / denominator
        beta[row] = (rhs[row] - lower * beta[row - 1]) / denominator

    solution = [0.0] * size
    solution[-1] = beta[-1]
    for row in range(size - 2, -1, -1):
        solution[row] = alpha[row] * solution[row + 1] + beta[row]
    return solution
