from math import sqrt

# ЛР1, задание 14, вариант 11.
# Для симметричной положительно определённой матрицы
# используем данные задания 4 при m = 10.
A = [
    [26.0, 1.3, 0.0, 2.2, 0.0],
    [1.3, 2.6, 0.78, 0.0, 1.1],
    [0.0, 0.78, 10.0, -0.78, 5.5],
    [2.2, 0.0, -0.78, 2.6, -0.26],
    [0.0, 1.1, 5.5, -0.26, 26.0]
]

# Допуск для невязки и ограничение числа итераций
EPS = 1e-8
MAX_ITERATIONS = 10000


def mat_vec(matrix, vector):
    # Умножаем матрицу на вектор.
    # Каждый элемент результата — сумма произведений
    # элементов очередной строки на компоненты вектора.
    result = []

    for i in range(len(matrix)):
        value = 0.0

        for j in range(len(vector)):
            value = value + matrix[i][j] * vector[j]

        result.append(value)

    return result


def normalize(vector):
    # Находим евклидову длину вектора.
    squared_sum = 0.0

    for value in vector:
        squared_sum = squared_sum + value ** 2

    length = sqrt(squared_sum)

    # Нулевой вектор нельзя нормировать.
    if length == 0.0:
        raise ValueError("Нулевой вектор")

    # Делим каждую компоненту на длину.
    # Новый вектор имеет длину 1 и прежнее направление.
    result = []

    for value in vector:
        result.append(value / length)

    return result


def eigen_residual(matrix, eigenvalue, vector):
    # Проверяем равенство A*x = lambda*x.
    product = mat_vec(matrix, vector)
    residual = 0.0

    for i in range(len(vector)):
        # Модуль разности соответствующих компонент.
        difference = abs(product[i] - eigenvalue * vector[i])

        # Сохраняем максимальную компоненту невязки.
        if difference > residual:
            residual = difference

    return residual


def power_method(matrix, eps, max_iterations):
    # Начальный ненулевой вектор.
    z = [1.0] * len(matrix)
    z = normalize(z)

    history = []

    for iteration in range(1, max_iterations + 1):
        # Главная формула степенного метода: y = A*z.
        y = mat_vec(matrix, z)

        # Выбираем компоненту старого вектора z,
        # имеющую наибольший модуль, чтобы не делить
        # на ноль или на очень маленькое число.
        index = 0

        for i in range(len(z)):
            if abs(z[i]) > abs(z[index]):
                index = i

        # Оцениваем собственное значение по отношению
        # соответствующих компонент (с учётом знака).
        eigenvalue = y[index] / z[index]

        # Нормируем новый вектор, чтобы числа не росли.
        z = normalize(y)

        # Проверяем, насколько точно выполняется
        # равенство A*z = lambda*z.
        residual = eigen_residual(matrix, eigenvalue, z)

        # Сохраняем все приближения для последующего вывода.
        history.append([iteration, eigenvalue, z, residual])

        # Останавливаемся по заданному допуску невязки.
        # Это не апостериорная оценка ошибки собственных значений.
        if residual <= eps:
            return eigenvalue, z, history

    raise RuntimeError("Превышено число итераций")


def shifted_matrix(matrix, eigenvalue):
    # Строим B = A - lambda_max*I.
    # Вне диагонали элементы не меняются.
    B = []

    for i in range(len(matrix)):
        row = []

        for j in range(len(matrix)):
            if i == j:
                value = matrix[i][j] - eigenvalue
            else:
                value = matrix[i][j]

            row.append(value)

        B.append(row)

    return B


def print_result(title, eigenvalue, vector, history):
    # Выводим последовательные приближения.
    print(title)
    print("Итерация | Собственное значение | Невязка")

    for iteration, value, approximation, residual in history:
        # Для краткости: первые пять, каждая сотая и последняя.
        # Все промежуточные векторы доступны в history.
        if iteration <= 5 or iteration % 100 == 0 or iteration == len(history):
            print(iteration, f"{value:.10f}", f"{residual:.3e}")

    print("Собственное значение:", eigenvalue)
    print("Собственный вектор:", vector)
    print("Количество итераций:", len(history))
    print("Невязка исходной матрицы:", eigen_residual(A, eigenvalue, vector))
    print()


def main():
    print("Допуск невязки:", EPS)

    # Первый запуск: ищем максимальное по модулю
    # собственное значение исходной матрицы A.
    lambda_max, vector_max, history_max = power_method(A, EPS, MAX_ITERATIONS)

    # Строим сдвинутую матрицу B = A - lambda_max*I.
    B = shifted_matrix(A, lambda_max)

    # Второй запуск того же метода: ищем максимальное
    # по модулю собственное значение матрицы B.
    mu, vector_min, history_min = power_method(B, EPS, MAX_ITERATIONS)

    # Возвращаем сдвиг и получаем минимальное значение A.
    # Собственный вектор при сдвиге сохраняется.
    lambda_min = lambda_max + mu

    print_result("Максимальное собственное значение", lambda_max, vector_max, history_max)
    print_result("Минимальное собственное значение (в истории значения для B)", lambda_min, vector_min, history_min)


if __name__ == "__main__":
    main()
