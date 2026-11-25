# ЛР2, задание 2. Метод Ньютона (касательных). Вариант 11.

# Формула (17): x_(k+1) = x_k - f(x_k)/f'(x_k).
# На [2,4] f'>0, f''=1/x^2+0.4>0, f(4)>0.
# По теореме §3.3 выбираем x0=4, так как f(4)*f''(4)>0.
# Оценка ошибки |f(x)|/m, где m=f'(2)=0.3.

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
    x, history = newton(RIGHT, EPS, MAX_ITERATIONS)
    print_scalar_result("2. Метод Ньютона", history)


if __name__ == "__main__":
    main()
