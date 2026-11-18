from .matrix_utils import (
    back_substitution,
    copy_matrix,
    forward_substitution,
    identity,
)


# Метод Гаусса, зануляем элементы под диагональю, затем находим x обратным ходом.
def gauss_elimination(matrix, rhs):
    a = copy_matrix(matrix)
    b = rhs[:]
    size = len(a)

    for column in range(size):
        pivot_row = column
        for row in range(column + 1, size):
            if abs(a[row][column]) > abs(a[pivot_row][column]):
                pivot_row = row

        if abs(a[pivot_row][column]) < 1e-14:
            raise ValueError("Матрица вырождена")

        if pivot_row != column:
            saved_row = a[column]
            a[column] = a[pivot_row]
            a[pivot_row] = saved_row

            saved_value = b[column]
            b[column] = b[pivot_row]
            b[pivot_row] = saved_value

        for row in range(column + 1, size):
            factor = a[row][column] / a[column][column]
            for index in range(column, size):
                a[row][index] -= factor * a[column][index]
            b[row] -= factor * b[column]
            a[row][column] = 0.0

    return back_substitution(a, b)


# Жордан-Гаусс, зануляем элементы и над, и под диагональю, получаем ответ сразу.
def gauss_jordan(matrix, rhs):
    a = copy_matrix(matrix)
    b = rhs[:]
    size = len(a)

    for column in range(size):
        pivot_row = column
        for row in range(column + 1, size):
            if abs(a[row][column]) > abs(a[pivot_row][column]):
                pivot_row = row

        if abs(a[pivot_row][column]) < 1e-14:
            raise ValueError("Матрица вырождена")

        if pivot_row != column:
            saved_row = a[column]
            a[column] = a[pivot_row]
            a[pivot_row] = saved_row

            saved_value = b[column]
            b[column] = b[pivot_row]
            b[pivot_row] = saved_value

        pivot = a[column][column]
        for index in range(size):
            a[column][index] /= pivot
        b[column] /= pivot

        for row in range(size):
            if row == column:
                continue
            factor = a[row][column]
            for index in range(size):
                a[row][index] -= factor * a[column][index]
            b[row] -= factor * b[column]
            a[row][column] = 0.0

    return b


# LU-разложение, представляем матрицу как произведение нижней и верхней треугольных.
def lu_decomposition(matrix):
    size = len(matrix)
    lower = identity(size)
    upper = []
    for row in range(size):
        upper.append([0.0] * size)

    for row in range(size):
        for column in range(row, size):
            known = 0.0
            for index in range(row):
                known += lower[row][index] * upper[index][column]
            upper[row][column] = matrix[row][column] - known

        if abs(upper[row][row]) < 1e-14:
            raise ValueError("LU-разложение требует перестановки строк")

        for next_row in range(row + 1, size):
            known = 0.0
            for index in range(row):
                known += lower[next_row][index] * upper[index][row]
            lower[next_row][row] = (matrix[next_row][row] - known) / upper[row][row]

    return lower, upper


# Решение через LU, сначала прямой ход для L, затем обратный для U.
def solve_lu(matrix, rhs):
    lower, upper = lu_decomposition(matrix)
    y = forward_substitution(lower, rhs)
    return back_substitution(upper, y)

# Решает СЛАУ методом простых итераций по формулам x_next = B*x + c.
def simple_iterations(matrix, rhs, eps=1e-6, max_iterations=10000, tau=0.1):
    size = len(rhs)

    B = []
    for i in range(size):
        row = []
        for j in range(size):
            if i == j:
                value = 1.0 - tau * matrix[i][j]
            else:
                value = 0.0 - tau * matrix[i][j]
            row.append(value)
        B.append(row)

    c = []
    for i in range(size):
        c.append(tau * rhs[i])

    q = 0.0
    for row in B:
        row_sum = 0.0
        for value in row:
            row_sum = row_sum + abs(value)
        if row_sum > q:
            q = row_sum

    if q >= 1.0:
        raise ValueError("Норма B >= 1: достаточное условие сходимости не выполнено")

    x = [0.0] * size
    history = [(0, x[:], None)]

    for iteration in range(1, max_iterations + 1):
        x_next = []
        for i in range(size):
            value = 0.0
            for j in range(size):
                value = value + B[i][j] * x[j]
            value = value + c[i]
            x_next.append(value)

        difference = 0.0
        for i in range(size):
            change = abs(x_next[i] - x[i])
            if change > difference:
                difference = change

        error_bound = q / (1.0 - q) * difference
        x = x_next
        history.append((iteration, x[:], error_bound))

        if error_bound <= eps:
            return x, B, c, q, history, error_bound

    raise RuntimeError("Метод простых итераций не достиг заданной точности")

