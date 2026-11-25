# ЛР2, задание 7. Метод спуска. Вариант 11.

# Минимизируем Psi(x,y)=F1^2+F2^2. Градиент вычисляем через J.
# Формула (28): (x_new,y_new)=(x,y)-alpha*grad(Psi).
# Если Psi не уменьшилась, делим alpha пополам. Начальный шаг 0.25.
# Уменьшение Psi само по себе не гарантирует попадание в корень:
# стационарная точка может иметь ненулевую невязку.
# Поэтому останавливаемся по max(|F1|,|F2|), а не по размеру шага.

from math import cos, isfinite, pi, sin


# Исходные параметры варианта 11.
EPS = 1e-8
MAX_ITERATIONS = 1000
START_X = -1.0
START_Y = 0.0
DESCENT_STEP = 0.25


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
    print(f"Начальный пробный шаг спуска = {DESCENT_STEP}")
    x, y, history = gradient_descent(START_X, START_Y, EPS, MAX_ITERATIONS)
    print_system_result("7. Метод спуска с делением шага", history)


if __name__ == "__main__":
    main()
