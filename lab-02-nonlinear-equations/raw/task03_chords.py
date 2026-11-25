# ЛР2, задание 3. Метод секущих (хорд). Вариант 11.

# Формула (20): x_(k+1)=x_k-f(x_k)*(b-x_k)/(f(b)-f(x_k)).
# Правый конец b=4 неподвижен, начинаем с a=2.
# f'>0 и f''>0 на [2,4], на концах разные знаки.
# Производная нужна только для оценки погрешности |f(x)|/m.

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
    x, history = chords(LEFT, RIGHT, EPS, MAX_ITERATIONS)
    print_scalar_result("3. Метод секущих, неподвижный конец 4", history)


if __name__ == "__main__":
    main()
