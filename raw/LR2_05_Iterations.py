# -*- coding: utf-8 -*-
"""
ЛР2, задание №5, вариант 11. ПРОСТЫЕ ИТЕРАЦИИ ДЛЯ ОДНОГО КОРНЯ.

КОРОТКАЯ ШПАРГАЛКА ДЛЯ ЗАЩИТЫ
1. Ищем x из f(x) = -ln(x) + 0.2*x^2 - 1 = 0 на отрезке [2, 4].
2. Преобразуем: x = phi(x) = sqrt(5*(ln(x)+1)).
3. Проверяем сходимость: q = max|phi'(x)| = phi'(2) < 1,
   а phi([2,4]) входит внутрь [2,4].
4. Начинаем с x0 = 3, повторяем x_next = phi(x) (формула (24)).
5. После итерации считаем апостериорную верхнюю оценку ошибки:
       error = q/(1-q)*abs(x_next-x)
6. Если error <= eps/2, возвращаем корень. Дополнительно считаем
   невязку abs(f(x)): она НЕ равна ошибке по x.

Собраны реальные функции из нашего src/data.py и src/scalar_methods.py.
Математика и порядок операций оставлены как в интегрированном архиве ЛР2.
"""

from math import log, sqrt  # Нужны только стандартные ln и квадратный корень.

# Значения из src/data.py; LEFT и RIGHT — границы изоляции корня.
EPS = 1e-8
MAX_ITERATIONS = 1000
LEFT = 2.0
RIGHT = 4.0


def equation(x):
    # Исходная функция f(x), корень которой ищем: f(x) = 0.
    return -log(x) + 0.2 * x * x - 1.0


def derivative(x):
    # Производная f'(x) = -1/x + 0.4*x.
    # На [2,4] она положительна и возрастает, её минимум f'(2)=0.3.
    return -1.0 / x + 0.4 * x


def iteration_function(x):
    # Функция phi(x) после преобразования f(x)=0 к x=phi(x):
    # -ln(x)+0.2*x^2-1=0  =>  x^2=5*(ln(x)+1).
    # Берём положительный корень, потому что ищем x на [2,4].
    return sqrt(5.0 * (log(x) + 1.0))


def iteration_derivative(x):
    # Производная phi'(x), нужна для оценки сходимости q.
    # Не путать с derivative(x) — производной исходной f(x).
    return 5.0 / (2.0 * x * iteration_function(x))


def simple_iterations(x, eps, max_iterations):
    # На [2,4] phi'(x) > 0 и убывает. Поэтому максимальный
    # модуль производной — именно phi'(LEFT), а не случайная точка.
    q = iteration_derivative(LEFT)

    # Для гарантированной сходимости нужно 0 < q < 1.
    if not 0.0 < q < 1.0:
        raise ValueError("Условие сходимости не выполнено")

    # Начальное приближение обязано быть на заданном отрезке.
    if not LEFT <= x <= RIGHT:
        raise ValueError("Начальное приближение вне отрезка")

    # Убеждаемся, что phi отображает весь отрезок [2,4] в себя.
    # Достаточно проверить концы, так как phi возрастает на [2,4].
    if not LEFT <= iteration_function(LEFT) <= RIGHT:
        raise ValueError("Функция итераций выходит за отрезок слева")
    if not LEFT <= iteration_function(RIGHT) <= RIGHT:
        raise ValueError("Функция итераций выходит за отрезок справа")

    # До первой итерации двух приближений ещё нет, поэтому оцениваем
    # ошибку x0 через невязку f(x0) и минимальную производную f'(2)=0.3:
    # |x0 - истинный корень| <= |f(x0)| / min|f'(x)|.
    initial_error = abs(equation(x)) / derivative(LEFT)

    # История: [номер итерации, x, невязка |f(x)|, верхняя оценка ошибки].
    # Первая строка относится к начальному приближению (итерация 0).
    history = [[0, x, abs(equation(x)), initial_error]]

    # Цикл начинает настоящие итерации с номера 1.
    for iteration in range(1, max_iterations + 1):

        # ГЛАВНАЯ ФОРМУЛА учебника (24): x_(n+1) = phi(x_n).
        x_next = iteration_function(x)

        # Страховка: новое приближение должно остаться на [2,4].
        if not LEFT <= x_next <= RIGHT:
            raise RuntimeError("Простые итерации вышли за отрезок")

        # Расстояние между двумя последовательными приближениями.
        difference = abs(x_next - x)

        # АПОСТЕРИОРНАЯ ОЦЕНКА: по полученным двум приближениям
        # гарантируем, что |x_next - истинный корень| <= error.
        error = q * difference / (1.0 - q)

        # Невязка исходного уравнения. В идеале f(корень) = 0.
        residual = abs(equation(x_next))

        # Сохраняем все данные для объяснения итераций преподавателю.
        history.append([iteration, x_next, residual, error])

        # Условие остановки. eps/2 — более строгий запас точности
        # из нашего исходного кода. Можно было бы использовать eps.
        if error <= eps / 2.0:
            return x_next, history

        # Старое приближение заменяем новым и делаем следующий шаг.
        x = x_next

    # Если 1000 шагов оказалось недостаточно, не выдаём ложный успех.
    raise RuntimeError("Простые итерации, превышен предел итераций")


def main():
    # Именно x0=3 используется при запуске задания №5 в нашем src/main.py.
    start_x = 3.0
    x, history = simple_iterations(start_x, EPS, MAX_ITERATIONS)

    print("ЛР №2, задание №5, вариант 11")
    print("Метод простых итераций")
    print("f(x) = -ln(x) + 0.2*x^2 - 1")
    print("phi(x) = sqrt(5*(ln(x)+1))")
    print(f"x0 = {start_x}, отрезок = [{LEFT}, {RIGHT}], eps = {EPS}")
    print(f"q = phi'(2) = {iteration_derivative(LEFT):.9f}")
    print()
    print("  k             x         |f(x)|       оценка ошибки")

    # Выводим ВСЕ приближения из history, как в полном проекте.
    for iteration, value, residual, error in history:
        print(f"{iteration:3d}  {value:14.10f}  {residual:14.9e}  {error:14.9e}")

    print()
    print(f"Найденный корень: x = {x:.10f}")
    print(f"Количество итераций: {history[-1][0]}")
    print(f"Апостериорная оценка: {history[-1][3]:.12e}")
    print(f"Невязка исходного уравнения: {abs(equation(x)):.12e}")


if __name__ == "__main__":
    main()
