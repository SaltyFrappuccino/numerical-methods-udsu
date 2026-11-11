from .data import (
    DESCENT_STEP,
    EPS,
    LEFT,
    MAX_ITERATIONS,
    RIGHT,
    START_X,
    START_Y,
    iteration_derivative,
)
from .output import print_comparison, print_scalar_result, print_system_result
from .scalar_methods import bisection, chords, combined, newton, simple_iterations
from .system_methods import gradient_descent, newton_system


def main():
    print("Лабораторная работа 2, вариант 11")
    print("f(x) = -ln(x) + 0.2*x*x - 1, отрезок [2, 4]")
    print(f"eps = {EPS:.0e}, предел итераций = {MAX_ITERATIONS}")
    print("Вычисления продолжаются до половины заданного допуска.")
    print("k = 0 обозначает начальное приближение.")
    print()
    scalar_results = []

    x, history = bisection(LEFT, RIGHT, EPS, MAX_ITERATIONS)
    print_scalar_result("1. Половинное деление", history)
    scalar_results.append(["Половинное деление", x, history])

    x, history = newton(RIGHT, EPS, MAX_ITERATIONS)
    print_scalar_result("2. Метод Ньютона", history)
    scalar_results.append(["Ньютон", x, history])

    x, history = chords(LEFT, RIGHT, EPS, MAX_ITERATIONS)
    print_scalar_result("3. Метод секущих, неподвижный конец 4", history)
    scalar_results.append(["Секущие, фиксированный конец", x, history])

    x, history = combined(LEFT, RIGHT, EPS, MAX_ITERATIONS)
    print_scalar_result("4. Комбинированный метод", history)
    scalar_results.append(["Комбинированный", x, history])

    print(f"phi(x) = sqrt(5*(ln(x) + 1)), q = {iteration_derivative(LEFT):.6f}")
    x, history = simple_iterations(LEFT, EPS, MAX_ITERATIONS)
    print_scalar_result("5. Простые итерации", history)
    scalar_results.append(["Простые итерации", x, history])

    print("F1(x, y) = sin(-x + pi/2 + 2) + y")
    print("F2(x, y) = cos(-y + pi/2 - 0.5) - x - 1")
    print(f"Начальное приближение ({START_X:.1f}, {START_Y:.1f})")
    print("Невязка = max(|F1|, |F2|), Psi = F1*F1 + F2*F2")
    print()
    system_results = []

    x, y, history = newton_system(START_X, START_Y, EPS, MAX_ITERATIONS)
    print_system_result("6. Метод Ньютона для системы", history)
    system_results.append(["Ньютон для системы", x, y, history])

    print(f"Начальный пробный шаг спуска = {DESCENT_STEP}")
    x, y, history = gradient_descent(START_X, START_Y, EPS, MAX_ITERATIONS)
    print_system_result("7. Метод спуска с делением шага", history)
    system_results.append(["Спуск", x, y, history])

    print_comparison(scalar_results, system_results)
