# ЛР2, задание 8. Сравнение результатов. Вариант 11.
#
# Сначала решаем одно уравнение пятью методами, затем систему двумя.
# Сравниваем число уточнений, невязки и оценки ошибок (для уравнения).
# Для системы верхняя граница ошибки координат не вычисляется.
# Невязка и разброс ответов — разные показатели, они не заменяют
# верхнюю оценку погрешности.
#
# Ниже — исходные функции всех семи методов и функция сравнения.
# Для защиты задания 8 основной интерес представляют main()
# и print_comparison(); остальные функции нужны для получения данных.

from math import cos, isfinite, log, pi, sin, sqrt


# Исходные параметры варианта 11.
EPS = 1e-8
MAX_ITERATIONS = 1000
LEFT = 2.0
RIGHT = 4.0
START_X = -1.0
START_Y = 0.0
DESCENT_STEP = 0.25


def equation(x):
    # Левая часть исходного уравнения. log(x) — натуральный логарифм.
    return -log(x) + 0.2 * x * x - 1.0


def derivative(x):
    # Первая производная f'(x). На [2, 4] положительна и возрастает.
    return -1.0 / x + 0.4 * x


def iteration_function(x):
    # Из f(x) = 0 выражаем x: x = sqrt(5*(ln(x)+1)).
    return sqrt(5.0 * (log(x) + 1.0))


def iteration_derivative(x):
    # Производная phi'(x). Нужна для оценки коэффициента сжатия q.
    return 5.0 / (2.0 * x * iteration_function(x))


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


def bisection(left, right, eps, max_iterations):
    # Вычисляем значения f на двух концах исходного отрезка.
    left_value = equation(left)
    right_value = equation(right)
    # Если знаки одинаковые, условие метода половинного деления не подтверждено.
    if left_value * right_value > 0:
        raise ValueError("На концах отрезка нет смены знака")
    # Если левый конец уже является корнем, возвращаем его.
    if left_value == 0.0:
        return left, [[0, left, 0.0, 0.0]]
    # То же самое для правого конца.
    if right_value == 0.0:
        return right, [[0, right, 0.0, 0.0]]

    # История: [номер уточнения, x, невязка, верхняя оценка ошибки].
    history = []
    # Строка 0 соответствует середине исходного отрезка до его сужения.
    for iteration in range(max_iterations + 1):
        # Вычисляем середину отрезка: c = (a+b)/2.
        middle = (left + right) / 2.0
        # Вычисляем f(c), чтобы определить знак и невязку.
        value = equation(middle)
        # Корень находится внутри отрезка, значит ошибка середины не больше половины его длины.
        error = (right - left) / 2.0
        # Если при вычислении получили точный ноль, дополнительное уточнение не нужно.
        if value == 0.0:
            error = 0.0
        # Записываем приближение, |f(c)| и оценку погрешности.
        history.append([iteration, middle, abs(value), error])
        # Останавливаемся по верхней оценке. eps/2 — запас точности.
        if error <= eps / 2.0:
            return middle, history
        # Ограничение числа уточнений.
        if iteration == max_iterations:
            break
        # Проверяем, что отрезок ещё можно делить при машинном округлении.
        if middle == left or middle == right:
            raise RuntimeError("Деление отрезка остановилось из-за округления")

        # Смена знака слева от середины: оставляем [left, middle].
        if left_value * value < 0.0:
            right = middle
        # Иначе оставляем [middle, right].
        else:
            left = middle
            # Запоминаем f нового левого конца.
            left_value = value

    # Если допуск не достигнут, сообщаем об этом.
    raise RuntimeError("Половинное деление, превышен предел итераций")


def newton(x, eps, max_iterations):
    # m = min |f'(x)| на [2,4] = f'(2) = 0.3.
    minimum_derivative = derivative(LEFT)
    # Храним номер итерации, приближение, невязку и оценку ошибки.
    history = []

    # Начинаем с x0 = 4, номер начальной строки — 0.
    for iteration in range(max_iterations + 1):
        # Проверяем, что приближение остаётся в области, где действует оценка погрешности.
        if x < LEFT or x > RIGHT:
            raise RuntimeError("Ньютон вышел за отрезок [2, 4]")
        # Вычисляем f(x) в текущей точке.
        value = equation(x)
        # Верхняя оценка ошибки: |x - корень| <= |f(x)| / m.
        error = abs(value) / minimum_derivative
        # Сохраняем результаты текущего шага.
        history.append([iteration, x, abs(value), error])
        # Если оценка меньше половины допуска, возвращаем ответ.
        if error <= eps / 2.0:
            return x, history
        # Не выполняем шаг сверх ограничения.
        if iteration == max_iterations:
            break

        # Находим f'(x) в текущей точке — наклон касательной.
        slope = derivative(x)
        # Защита от деления на нулевую или слишком малую производную.
        if abs(slope) < 1e-14:
            raise ValueError("Производная слишком мала для деления")
        # Формула Ньютона (17): x_(k+1) = x_k - f(x_k)/f'(x_k).
        x = x - value / slope

    # Сообщаем, если за допустимое число шагов точность не достигнута.
    raise RuntimeError("Ньютон, превышен предел итераций")


def chords(left, right, eps, max_iterations):
    # Начинаем с левого конца a = 2, правый конец b = 4 неподвижен.
    x = left
    # Значение f(b) постоянно на всех шагах.
    right_value = equation(right)
    # Минимальный модуль производной на [2,4] равен 0.3.
    minimum_derivative = derivative(LEFT)
    # Проверяем смену знака на исходном отрезке.
    if equation(left) * right_value > 0.0:
        raise ValueError("На концах отрезка нет смены знака")
    # Если неподвижный конец уже является корнем, возвращаем его.
    if right_value == 0.0:
        return right, [[0, right, 0.0, 0.0]]
    # История приближений, невязок и оценок погрешности.
    history = []

    # Итерации метода секущих с неподвижным концом.
    for iteration in range(max_iterations + 1):
        # Проверяем, что x остаётся внутри отрезка.
        if x < LEFT or x > RIGHT:
            raise RuntimeError("Метод хорд вышел за отрезок [2, 4]")
        # Вычисляем f(x_k).
        value = equation(x)
        # Оцениваем погрешность через невязку: |f(x)|/m.
        error = abs(value) / minimum_derivative
        # Сохраняем текущие результаты.
        history.append([iteration, x, abs(value), error])
        # Останавливаемся при достижении допуска с запасом.
        if error <= eps / 2.0:
            return x, history
        # Ограничиваем число итераций.
        if iteration == max_iterations:
            break

        # Разность f(b) - f(x_k) в знаменателе формулы хорды.
        denominator = right_value - value
        # Проверяем, что делитель не слишком мал.
        if abs(denominator) < 1e-14:
            raise ValueError("Знаменатель формулы хорд слишком мал")
        # Формула (20): пересечение хорды с осью X.
        # Производную при вычислении нового x не используем.
        x = x - value * (right - x) / denominator

    # Допуск не достигнут за выделенное число шагов.
    raise RuntimeError("Метод хорд, превышен предел итераций")


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


def simple_iterations(x, eps, max_iterations):
    # phi'(x) положительна и убывает на [2,4],
    # поэтому q = max |phi'(x)| = phi'(2) ≈ 0.429613.
    q = iteration_derivative(LEFT)
    # Проверяем условие сжатия для нашего варианта.
    if not 0.0 < q < 1.0:
        raise ValueError("Условие сходимости не выполнено")
    # Начальное приближение должно принадлежать отрезку.
    if not LEFT <= x <= RIGHT:
        raise ValueError("Начальное приближение вне отрезка")
    # Проверяем phi(2). Функция phi возрастает, поэтому достаточно проверить оба конца.
    if not LEFT <= iteration_function(LEFT) <= RIGHT:
        raise ValueError("Функция итераций выходит за отрезок слева")
    # Проверяем phi(4), чтобы phi отображала весь [2,4] в себя.
    if not LEFT <= iteration_function(RIGHT) <= RIGHT:
        raise ValueError("Функция итераций выходит за отрезок справа")

    # До первой итерации нет двух приближений. Оцениваем начальную
    # ошибку через |f(x0)|/m, где m = f'(2) = 0.3.
    initial_error = abs(equation(x)) / derivative(LEFT)
    # Записываем начальное приближение и его невязку с оценкой ошибки.
    history = [[0, x, abs(equation(x)), initial_error]]

    # Выполняем собственно итерации, начиная с номера 1.
    for iteration in range(1, max_iterations + 1):
        # Основная формула (24): x_(k+1) = phi(x_k).
        x_next = iteration_function(x)
        # Контролируем принадлежность нового приближения отрезку.
        if not LEFT <= x_next <= RIGHT:
            raise RuntimeError("Простые итерации вышли за отрезок")

        # Находим разность двух соседних приближений по модулю.
        difference = abs(x_next - x)
        # Апостериорная верхняя оценка погрешности: q/(1-q) * |x_(k+1)-x_k|.
        error = q * difference / (1.0 - q)
        # Невязка исходного уравнения |f(x_next)|, не ошибка по x.
        residual = abs(equation(x_next))
        # Запоминаем новый x и обе меры точности.
        history.append([iteration, x_next, residual, error])

        # Останавливаемся по верхней оценке, а не только по невязке.
        # eps/2 — дополнительный запас относительно eps.
        if error <= eps / 2.0:
            return x_next, history

        # Новое приближение становится текущим для следующего шага.
        x = x_next

    # Предел итераций исчерпан, заданная точность не достигнута.
    raise RuntimeError("Простые итерации, превышен предел итераций")


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


def gradient_descent(x, y, eps, max_iterations):
    # История: номер, x, y, невязка, Psi и использованный параметр шага.
    history = []
    # На начальном приближении перемещения ещё не было.
    step = 0.0

    # Начинаем с исходной точки, затем повторяем шаги спуска.
    for iteration in range(max_iterations + 1):
        # Проверяем, что координаты являются конечными числами.
        if not isfinite(x) or not isfinite(y):
            raise RuntimeError("Метод спуска, получены бесконечные значения")
        # Вычисляем значения F1(x,y), F2(x,y).
        first, second = system_values(x, y)
        # Максимальная невязка исходной системы.
        residual = max(abs(first), abs(second))
        # Целевая функция Psi = F1^2 + F2^2.
        # Psi = 0 тогда и только тогда, когда оба уравнения выполнены.
        psi = first * first + second * second
        # Записываем текущее приближение и шаг, которым пришли к нему.
        history.append([iteration, x, y, residual, psi, step])
        # Остановка по невязке, а не по верхней оценке ошибки координат.
        if residual <= eps / 2.0:
            return x, y, history
        # Ограничение количества итераций.
        if iteration == max_iterations:
            break

        # Берём частные производные F1 и F2 из матрицы Якоби.
        matrix = jacobian(x, y)
        # Частная производная Psi по x: 2*F1*dF1/dx + 2*F2*dF2/dx.
        grad_x = 2.0 * (first * matrix[0][0] + second * matrix[1][0])
        # Частная производная Psi по y: 2*F1*dF1/dy + 2*F2*dF2/dy.
        grad_y = 2.0 * (first * matrix[0][1] + second * matrix[1][1])
        # Градиент равен нулю, точка стационарная. Если допуск ещё не
        # достигнут, направление спуска отсутствует.
        if grad_x == 0.0 and grad_y == 0.0:
            raise RuntimeError("Стационарная точка с ненулевой невязкой")

        # На каждой итерации начинаем подбор с пробного шага 0.25.
        step = DESCENT_STEP
        # Внутренний цикл подбора шага (стр. 30 учебника).
        while True:
            # Формула (28): движемся по антиградиенту.
            # step — множитель градиента, а не само расстояние перемещения.
            next_x = x - step * grad_x
            next_y = y - step * grad_y
            # Вычисляем исходные функции в пробной новой точке.
            next_first, next_second = system_values(next_x, next_y)
            # Считаем Psi для пробного приближения.
            next_psi = next_first * next_first + next_second * next_second
            # Если целевая функция уменьшилась, принимаем шаг.
            # break завершает только подбор шага, а не внешний цикл.
            if next_psi < psi:
                break
            # Если убывания нет, уменьшаем пробный шаг вдвое и повторяем.
            step = step / 2.0
            # Защита от бесконечного уменьшения шага при машинном округлении.
            if step < 1e-14:
                raise RuntimeError("Не удалось уменьшить сумму квадратов невязок")

        # Принимаем новую точку, затем переходим к следующей итерации.
        x = next_x
        y = next_y

    # Предел итераций исчерпан, необходимая невязка не достигнута.
    raise RuntimeError("Метод спуска, превышен предел итераций")


def print_comparison(scalar_results, system_results):
    print("8. Сравнение результатов")
    print("Уравнение")
    print("Метод                       Итераций              x      Невязка    Оценка ошибки x")
    # Изначально считаем первый найденный корень минимумом и максимумом.
    smallest = scalar_results[0][1]
    largest = smallest
    # Сравниваем пять методов решения одного уравнения.
    for name, x, history in scalar_results:
        # Вычисляем невязку исходного уравнения |f(x)|.
        residual = abs(equation(x))
        # Верхняя оценка погрешности из последней строки истории метода.
        error = history[-1][3]
        # Число уточнений без начальной строки 0.
        iterations = len(history) - 1
        print(
            f"{name:28s} {iterations:7d} {x:14.8f} "
            f"{residual:12.3e} {error:18.3e}"
        )
        # Ищем минимальный среди найденных корней.
        if x < smallest:
            smallest = x
        # Ищем максимальный среди найденных корней.
        if x > largest:
            largest = x
    # Разброс показывает согласованность ответов, но не ошибку относительно точного корня.
    print(f"Разброс ответов = {largest - smallest:.3e}")
    print()

    print("Система")
    print("Метод                       Итераций              x              y      Невязка")
    # Отдельно сравниваем методы решения системы.
    for name, x, y, history in system_results:
        # Подставляем решение каждого метода в оба исходных уравнения.
        first, second = system_values(x, y)
        # Максимальная невязка. Верхние оценки ошибок координат здесь не вычисляются.
        residual = max(abs(first), abs(second))
        # Число уточнений без начальной строки 0.
        iterations = len(history) - 1
        print(
            f"{name:28s} {iterations:7d} {x:14.8f} "
            f"{y:14.8f} {residual:12.3e}"
        )
    # Разность решений Ньютона и спуска по координате x.
    difference_x = abs(system_results[0][1] - system_results[1][1])
    # Разность по координате y.
    difference_y = abs(system_results[0][2] - system_results[1][2])
    # Максимальная из двух разностей характеризует согласованность решений.
    print(f"Различие ответов = {max(difference_x, difference_y):.3e}")


def main():
    print("Лабораторная работа 2, вариант 11")
    print(f"eps = {EPS:.0e}, предел итераций = {MAX_ITERATIONS}")
    print()

    # Сохраняем результаты пяти методов решения уравнения.
    # Каждая запись: название, корень x, история вычислений.
    scalar_results = []

    # Задание 1. Половинное деление на [2,4].
    x, history = bisection(LEFT, RIGHT, EPS, MAX_ITERATIONS)
    scalar_results.append(["Половинное деление", x, history])

    # Задание 2. Ньютон с правого конца отрезка.
    x, history = newton(RIGHT, EPS, MAX_ITERATIONS)
    scalar_results.append(["Ньютон", x, history])

    # Задание 3. Секущие с неподвижным правым концом.
    x, history = chords(LEFT, RIGHT, EPS, MAX_ITERATIONS)
    scalar_results.append(["Секущие, фиксированный конец", x, history])

    # Задание 4. Комбинированный метод.
    x, history = combined(LEFT, RIGHT, EPS, MAX_ITERATIONS)
    scalar_results.append(["Комбинированный", x, history])

    # Задание 5. Простые итерации с x0=3.
    x, history = simple_iterations(3.0, EPS, MAX_ITERATIONS)
    scalar_results.append(["Простые итерации", x, history])

    # Для системы в каждой записи дополнительно есть координата y.
    system_results = []

    # Задание 6. Ньютон для системы, начальная точка (-1,0).
    x, y, history = newton_system(START_X, START_Y, EPS, MAX_ITERATIONS)
    system_results.append(["Ньютон для системы", x, y, history])

    # Задание 7. Метод спуска из той же начальной точки.
    x, y, history = gradient_descent(START_X, START_Y, EPS, MAX_ITERATIONS)
    system_results.append(["Спуск", x, y, history])

    # Задание 8. Передаём полученные данные в функцию сравнения.
    print_comparison(scalar_results, system_results)


if __name__ == "__main__":
    main()
