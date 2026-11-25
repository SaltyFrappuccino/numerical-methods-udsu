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
