# ЛР2, задание 6. Метод Ньютона для системы. Вариант 11.

# Составляем матрицу Якоби J и решаем J*delta=-F методом Крамера.
# К текущим x,y прибавляем поправки delta_x, delta_y.
# Начальная точка (-1,0) — центр области возможных решений
# x в [-2,0], y в [-1,1]. Это эвристический выбор, не доказательство
# сходимости. Невырожденность J позволяет вычислить поправки.
# Остановка по максимальной невязке max(|F1|,|F2|).

from math import cos, isfinite, pi, sin


# Исходные параметры варианта 11.
EPS = 1e-8
MAX_ITERATIONS = 1000
START_X = -1.0
START_Y = 0.0


def system_values(x, y):
    # F1(x,y) — левая часть первого уравнения.
    first = sin(-x + pi / 2.0 + 2.0) + y
    # F2(x,y) — левая часть второго уравнения.
    second = cos(-y + pi / 2.0 - 0.5) - x - 1.0
    # Возвращаем две компоненты вектора F(x,y).
    return first, second


def jacobian(x, y):
    # Матрица Якоби J. Первая строка — производные F1 по x и y,
    # вторая строка — производные F2 по x и y.
    return [
        # dF1/dx = -cos(-x+pi/2+2); dF1/dy = 1.
        [-cos(-x + pi / 2.0 + 2.0), 1.0],
        # dF2/dx = -1; dF2/dy = sin(-y+pi/2-0.5).
        [-1.0, sin(-y + pi / 2.0 - 0.5)]
    ]


def newton_system(x, y, eps, max_iterations):
    # История: номер, x, y, невязка, Psi, коэффициент шага.
    history = []
    # Начальная точка: поправку ещё не применяли.
    step = 0.0

    # Начальная запись — итерация 0, далее уточняем пару x, y.
    for iteration in range(max_iterations + 1):
        # Проверяем, что x и y остались конечными числами.
        if not isfinite(x) or not isfinite(y):
            raise RuntimeError("Ньютон для системы, получены бесконечные значения")
        # F1 и F2 — значения левых частей исходной системы.
        first, second = system_values(x, y)
        # Максимальный модуль невязки двух уравнений.
        residual = max(abs(first), abs(second))
        # Сумма квадратов невязок. В Ньютоне используется для вывода, а не для выбора поправок.
        psi = first * first + second * second
        # Сохраняем текущую точку и показатели вычислений.
        history.append([iteration, x, y, residual, psi, step])
        # Останавливаемся по невязке. Это не верхняя оценка ошибки координат.
        if residual <= eps / 2.0:
            return x, y, history
        # Проверяем предел числа итераций.
        if iteration == max_iterations:
            break

        # Строим J — матрицу четырёх частных производных F1 и F2.
        matrix = jacobian(x, y)
        # Извлекаем четыре коэффициента системы J*delta = -F.
        j11 = matrix[0][0]
        j12 = matrix[0][1]
        j21 = matrix[1][0]
        j22 = matrix[1][1]
        # Определитель матрицы Якоби 2×2.
        determinant = j11 * j22 - j12 * j21
        # При почти нулевом определителе поправки ненадёжны.
        # Ненулевой определитель позволяет сделать шаг, но сам по себе
        # не доказывает сходимость из произвольной начальной точки.
        if abs(determinant) < 1e-14:
            raise ValueError("Определитель матрицы Якоби слишком мал")

        # Правило Крамера: заменяем первый столбец J на -F и делим определители.
        delta_x = (-first * j22 + j12 * second) / determinant
        # Правило Крамера: заменяем второй столбец J на -F.
        delta_y = (j21 * first - j11 * second) / determinant
        # Формула Ньютона (19): прибавляем обе вычисленные поправки.
        x = x + delta_x
        y = y + delta_y
        # Полный шаг Ньютона: применяем 100% поправки.
        # Переменная step здесь только для истории, в формулах не участвует.
        step = 1.0

    # Невязка не достигла допуска за отведённое число шагов.
    raise RuntimeError("Ньютон для системы, превышен предел итераций")


def print_system_result(title, history):
    print(title)
    print("  k              x              y      Невязка          Psi       Шаг")
    # Печатаем последовательные приближения x,y и показатели точности.
    for row in history:
        # Разбираем шесть столбцов строки истории.
        iteration, x, y, residual, psi, step = row
        print(
            f"{iteration:3d} {x:14.8f} {y:14.8f} "
            f"{residual:12.3e} {psi:12.3e} {step:9.5f}"
        )

    # Берём x и y из последней строки.
    x = history[-1][1]
    y = history[-1][2]
    # Повторно подставляем найденный ответ в исходные уравнения.
    first, second = system_values(x, y)
    print(f"Ответ x = {x:.8f}, y = {y:.8f}")
    # Показываем значения обеих левых частей: они должны быть близки к нулю.
    print(f"F1 = {first:.3e}, F2 = {second:.3e}")
    # Исключаем из счётчика начальную строку.
    print("Итераций =", len(history) - 1)
    print()


def main():
    print("Лабораторная работа 2, вариант 11")
    print(f"eps = {EPS:.0e}, предел итераций = {MAX_ITERATIONS}")
    x, y, history = newton_system(START_X, START_Y, EPS, MAX_ITERATIONS)
    print_system_result("6. Метод Ньютона для системы", history)


if __name__ == "__main__":
    main()
