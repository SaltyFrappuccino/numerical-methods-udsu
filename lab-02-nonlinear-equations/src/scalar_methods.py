from .data import (
    LEFT,
    RIGHT,
    derivative,
    equation,
    iteration_derivative,
    iteration_function,
)


# Задание 1, половинное деление сохраняет отрезок со сменой знака.
def bisection(left, right, eps, max_iterations):
    left_value = equation(left)
    right_value = equation(right)
    if left_value * right_value > 0:
        raise ValueError("На концах отрезка нет смены знака")
    if left_value == 0.0:
        return left, [[0, left, 0.0, 0.0]]
    if right_value == 0.0:
        return right, [[0, right, 0.0, 0.0]]

    history = []
    for iteration in range(max_iterations + 1):
        middle = (left + right) / 2.0
        value = equation(middle)
        error = (right - left) / 2.0
        if value == 0.0:
            error = 0.0
        history.append([iteration, middle, abs(value), error])
        if error <= eps / 2.0:
            return middle, history
        if iteration == max_iterations:
            break
        if middle == left or middle == right:
            raise RuntimeError("Деление отрезка остановилось из-за округления")

        if left_value * value < 0.0:
            right = middle
        else:
            left = middle
            left_value = value

    raise RuntimeError("Половинное деление, превышен предел итераций")


# Задание 2, Ньютон находит следующее приближение по касательной.
def newton(x, eps, max_iterations):
    minimum_derivative = derivative(LEFT)
    history = []

    for iteration in range(max_iterations + 1):
        if x < LEFT or x > RIGHT:
            raise RuntimeError("Ньютон вышел за отрезок [2, 4]")
        value = equation(x)
        error = abs(value) / minimum_derivative
        history.append([iteration, x, abs(value), error])
        if error <= eps / 2.0:
            return x, history
        if iteration == max_iterations:
            break

        slope = derivative(x)
        if abs(slope) < 1e-14:
            raise ValueError("Производная слишком мала для деления")
        x = x - value / slope

    raise RuntimeError("Ньютон, превышен предел итераций")


# Задание 3, хорды уточняют левую точку при неподвижном правом конце.
def chords(left, right, eps, max_iterations):
    x = left
    right_value = equation(right)
    minimum_derivative = derivative(LEFT)
    if equation(left) * right_value > 0.0:
        raise ValueError("На концах отрезка нет смены знака")
    if right_value == 0.0:
        return right, [[0, right, 0.0, 0.0]]
    history = []

    for iteration in range(max_iterations + 1):
        if x < LEFT or x > RIGHT:
            raise RuntimeError("Метод хорд вышел за отрезок [2, 4]")
        value = equation(x)
        error = abs(value) / minimum_derivative
        history.append([iteration, x, abs(value), error])
        if error <= eps / 2.0:
            return x, history
        if iteration == max_iterations:
            break

        denominator = right_value - value
        if abs(denominator) < 1e-14:
            raise ValueError("Знаменатель формулы хорд слишком мал")
        x = x - value * (right - x) / denominator

    raise RuntimeError("Метод хорд, превышен предел итераций")


# Задание 4, хорда сдвигает левую границу, касательная сдвигает правую.
def combined(left, right, eps, max_iterations):
    if equation(left) * equation(right) > 0.0:
        raise ValueError("На концах отрезка нет смены знака")
    history = []

    for iteration in range(max_iterations + 1):
        middle = (left + right) / 2.0
        value = equation(middle)
        error = (right - left) / 2.0
        if value == 0.0:
            error = 0.0
        history.append([iteration, middle, abs(value), error])
        if error <= eps / 2.0:
            return middle, history
        if iteration == max_iterations:
            break

        left_value = equation(left)
        right_value = equation(right)
        denominator = right_value - left_value
        slope = derivative(right)
        if abs(denominator) < 1e-14 or abs(slope) < 1e-14:
            raise ValueError("Знаменатель комбинированного метода слишком мал")

        new_left = left - left_value * (right - left) / denominator
        new_right = right - right_value / slope
        left = new_left
        right = new_right

    raise RuntimeError("Комбинированный метод, превышен предел итераций")


# Задание 5, последовательно подставляем x в функцию итерации.
def simple_iterations(x, eps, max_iterations):
    q = iteration_derivative(LEFT)
    if q >= 1.0:
        raise ValueError("Условие сжатия не выполнено")
    error = abs(equation(x)) / derivative(LEFT)
    history = []

    for iteration in range(max_iterations + 1):
        if x < LEFT or x > RIGHT:
            raise RuntimeError("Простые итерации вышли за отрезок [2, 4]")
        value = equation(x)
        history.append([iteration, x, abs(value), error])
        if error <= eps / 2.0:
            return x, history
        if iteration == max_iterations:
            break

        next_x = iteration_function(x)
        error = q * abs(next_x - x) / (1.0 - q)
        x = next_x

    raise RuntimeError("Простые итерации, превышен предел итераций")
