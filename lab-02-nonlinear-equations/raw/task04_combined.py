# ЛР2, задание 4. Комбинированный метод. Вариант 11.

# Формула (22): левую границу уточняем методом секущих, правую —
# методом Ньютона. Корень остаётся между границами.
# Для нашего f на [2,4] выполняются f'>0, f''>0, f(2)<0<f(4).
# Приближение — середина отрезка, оценка ошибки — половина его длины.

from math import log


# Исходные параметры варианта 11.
EPS = 1e-8
MAX_ITERATIONS = 1000
LEFT = 2.0
RIGHT = 4.0


def equation(x):
    # Левая часть исходного уравнения. log(x) — натуральный логарифм.
    return -log(x) + 0.2 * x * x - 1.0


def derivative(x):
    # Первая производная f'(x). На [2, 4] положительна и возрастает.
    return -1.0 / x + 0.4 * x


def combined(left, right, eps, max_iterations):
    # Проверяем смену знака: исходный отрезок должен содержать корень.
    if equation(left) * equation(right) > 0.0:
        raise ValueError("На концах отрезка нет смены знака")
    # Сохраняем середины отрезков, невязки и оценки ошибок.
    history = []

    # На каждом шаге сужаем отрезок с двух сторон.
    for iteration in range(max_iterations + 1):
        # В качестве ответа используем середину текущего отрезка.
        middle = (left + right) / 2.0
        # Проверяем исходное уравнение в этой точке.
        value = equation(middle)
        # Верхняя оценка ошибки середины — половина длины отрезка.
        error = (right - left) / 2.0
        # Если вычислили ноль, останавливаемся без дальнейшего сужения.
        if value == 0.0:
            error = 0.0
        # Записываем результаты итерации.
        history.append([iteration, middle, abs(value), error])
        # Проверяем точность приближения.
        if error <= eps / 2.0:
            return middle, history
        # Не превышаем установленное число шагов.
        if iteration == max_iterations:
            break

        # Вычисляем f на обеих текущих границах.
        left_value = equation(left)
        right_value = equation(right)
        # Знаменатель формулы метода секущих.
        denominator = right_value - left_value
        # Производная на правом конце для метода Ньютона.
        slope = derivative(right)
        # Защищаем оба деления от почти нулевого знаменателя.
        if abs(denominator) < 1e-14 or abs(slope) < 1e-14:
            raise ValueError("Знаменатель комбинированного метода слишком мал")

        # Формула (22): левую границу уточняем хордой.
        new_left = left - left_value * (right - left) / denominator
        # Правую границу уточняем касательной Ньютона.
        new_right = right - right_value / slope
        # Обновляем обе границы только после их вычисления.
        left = new_left
        right = new_right

    # Сообщаем, если вычисления не достигли допуска.
    raise RuntimeError("Комбинированный метод, превышен предел итераций")


def print_scalar_result(title, history):
    print(title)
    print("  k              x        |f(x)|      Оценка ошибки x")
    # Выводим все сохранённые строки истории.
    for row in history:
        # Номер, приближение x, невязка и верхняя оценка ошибки.
        iteration, x, residual, error = row
        print(f"{iteration:3d} {x:14.8f} {residual:13.3e} {error:19.3e}")

    # Окончательный ответ — x из последней строки истории.
    print(f"Ответ x = {history[-1][1]:.8f}")
    # Не считаем начальную строку с номером 0.
    print("Итераций =", len(history) - 1)
    print()


def main():
    print("Лабораторная работа 2, вариант 11")
    print(f"eps = {EPS:.0e}, предел итераций = {MAX_ITERATIONS}")
    x, history = combined(LEFT, RIGHT, EPS, MAX_ITERATIONS)
    print_scalar_result("4. Комбинированный метод", history)


if __name__ == "__main__":
    main()
