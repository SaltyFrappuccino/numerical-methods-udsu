from math import isfinite

from .data import DESCENT_STEP, jacobian, system_values


# Задание 6, Ньютон решает линейную систему для поправок к x и y.
def newton_system(x, y, eps, max_iterations):
    history = []
    step = 0.0

    for iteration in range(max_iterations + 1):
        if not isfinite(x) or not isfinite(y):
            raise RuntimeError("Ньютон для системы, получены бесконечные значения")
        first, second = system_values(x, y)
        residual = max(abs(first), abs(second))
        psi = first * first + second * second
        history.append([iteration, x, y, residual, psi, step])
        if residual <= eps / 2.0:
            return x, y, history
        if iteration == max_iterations:
            break

        matrix = jacobian(x, y)
        j11 = matrix[0][0]
        j12 = matrix[0][1]
        j21 = matrix[1][0]
        j22 = matrix[1][1]
        determinant = j11 * j22 - j12 * j21
        if abs(determinant) < 1e-14:
            raise ValueError("Определитель матрицы Якоби слишком мал")

        delta_x = (-first * j22 + j12 * second) / determinant
        delta_y = (j21 * first - j11 * second) / determinant
        x = x + delta_x
        y = y + delta_y
        step = 1.0

    raise RuntimeError("Ньютон для системы, превышен предел итераций")


# Задание 7, спуск уменьшает сумму квадратов невязок вдоль антиградиента.
def gradient_descent(x, y, eps, max_iterations):
    history = []
    step = 0.0

    for iteration in range(max_iterations + 1):
        if not isfinite(x) or not isfinite(y):
            raise RuntimeError("Метод спуска, получены бесконечные значения")
        first, second = system_values(x, y)
        residual = max(abs(first), abs(second))
        psi = first * first + second * second
        history.append([iteration, x, y, residual, psi, step])
        if residual <= eps / 2.0:
            return x, y, history
        if iteration == max_iterations:
            break

        matrix = jacobian(x, y)
        grad_x = 2.0 * (first * matrix[0][0] + second * matrix[1][0])
        grad_y = 2.0 * (first * matrix[0][1] + second * matrix[1][1])
        if grad_x == 0.0 and grad_y == 0.0:
            raise RuntimeError("Стационарная точка с ненулевой невязкой")

        step = DESCENT_STEP
        while True:
            next_x = x - step * grad_x
            next_y = y - step * grad_y
            next_first, next_second = system_values(next_x, next_y)
            next_psi = next_first * next_first + next_second * next_second
            if next_psi < psi:
                break
            step = step / 2.0
            if step < 1e-14:
                raise RuntimeError("Не удалось уменьшить сумму квадратов невязок")

        x = next_x
        y = next_y

    raise RuntimeError("Метод спуска, превышен предел итераций")
