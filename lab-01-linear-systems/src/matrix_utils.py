from math import sqrt



# Копирует матрицу, чтобы другие методы не меняли исходные числа.
def copy_matrix(matrix):
    result = []
    for row in matrix:
        result.append(row[:])
    return result


# Скалярное произведение, перемножаем элементы векторов и складываем.
def dot(first, second):
    result = 0.0
    for index in range(len(first)):
        result += first[index] * second[index]
    return result


# Умножает матрицу на вектор, по одному результату для каждой строки.
def mat_vec(matrix, vector):
    result = []
    for row in matrix:
        result.append(dot(row, vector))
    return result


# Создаёт единичную матрицу, единицы на диагонали, остальные нули.
def identity(size):
    matrix = []
    for row in range(size):
        values = []
        for column in range(size):
            if row == column:
                values.append(1.0)
            else:
                values.append(0.0)
        matrix.append(values)
    return matrix


# Находит самый большой по модулю элемент вектора.
def vector_norm(vector):
    largest = 0.0
    for value in vector:
        if abs(value) > largest:
            largest = abs(value)
    return largest


# Вычисляет длину вектора через сумму квадратов его элементов.
def euclidean_norm(vector):
    total = 0.0
    for value in vector:
        total += value * value
    return sqrt(total)


# Проверяет ответ, вычисляет максимальное отклонение в A*x - b.
def residual(matrix, rhs, solution):
    product = mat_vec(matrix, solution)
    difference = []
    for index in range(len(rhs)):
        difference.append(product[index] - rhs[index])
    return vector_norm(difference)


# Прямой ход подстановки, решаем нижнетреугольную систему сверху вниз.
def forward_substitution(lower, rhs):
    size = len(rhs)
    solution = [0.0] * size
    for row in range(size):
        known = 0.0
        for column in range(row):
            known += lower[row][column] * solution[column]
        solution[row] = (rhs[row] - known) / lower[row][row]
    return solution


# Обратный ход подстановки, решаем верхнетреугольную систему снизу вверх.
def back_substitution(upper, rhs):
    size = len(rhs)
    solution = [0.0] * size
    for row in range(size - 1, -1, -1):
        known = 0.0
        for column in range(row + 1, size):
            known += upper[row][column] * solution[column]
        solution[row] = (rhs[row] - known) / upper[row][row]
    return solution
