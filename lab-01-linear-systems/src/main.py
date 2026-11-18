from .data import standard_system, symmetric_system, tridiagonal_system
from .linear_methods import gauss_elimination, gauss_jordan, solve_lu, simple_iterations
from .matrix_utils import residual
from .special_methods import solve_orthogonalization, solve_square_roots, thomas_method


# Выводит матрицу и правую часть системы.
def print_system(matrix, rhs):
    print("A =")
    for row in matrix:
        line = ""
        for value in row:
            line += f" {value:8.4f}"
        print(line)

    text = "b ="
    for value in rhs:
        text += f" {value:.4f}"
    print(text)
    print()


# Показывает найденный вектор и невязку относительно исходной системы.
def print_result(title, matrix, rhs, solution):
    print(title)
    values = []
    for value in solution:
        if abs(value) < 1e-12:
            value = 0.0
        values.append(f"{value:.8f}")
    print("x =", " ".join(values))
    print(f"Невязка = {residual(matrix, rhs, solution):.2e}")
    print()


# Выполняет семь методов решения СЛАУ, вариант 11.
def main():
    print("Лабораторная работа 1, вариант 11, задания 1-7")
    print()

    matrix, rhs = standard_system()
    print("Задания 1-3 и 5")
    print_system(matrix, rhs)

    solution = gauss_elimination(matrix, rhs)
    print_result("1. Метод Гаусса", matrix, rhs, solution)

    solution = gauss_jordan(matrix, rhs)
    print_result("2. Метод Жордана-Гаусса", matrix, rhs, solution)

    solution = solve_lu(matrix, rhs)
    print_result("3. LU-разложение", matrix, rhs, solution)

    symmetric, symmetric_rhs = symmetric_system()
    print("Задание 4")
    print_system(symmetric, symmetric_rhs)

    solution = solve_square_roots(symmetric, symmetric_rhs)
    print_result("4. Метод квадратных корней", symmetric, symmetric_rhs, solution)

    solution = solve_orthogonalization(matrix, rhs)
    print_result("5. Метод ортогонализации", matrix, rhs, solution)

    tridiagonal, tridiagonal_rhs = tridiagonal_system()
    print("Задание 6")
    print_system(tridiagonal, tridiagonal_rhs)

    solution = thomas_method(tridiagonal, tridiagonal_rhs)
    print_result("6. Метод прогонки", tridiagonal, tridiagonal_rhs, solution)

    print("Задание 7")
    print_system(matrix, rhs)

    solution, B, c, q, history, error_bound = simple_iterations(
        matrix, rhs, eps=1e-6, max_iterations=10000, tau=0.1
    )

    print("B = I - 0.1*A")
    for row in B:
        text = ""
        for value in row:
            text += f" {value:8.4f}"
        print(text)

    print("c = 0.1*b")
    text = ""
    for value in c:
        text += f" {value:.5f}"
    print(text)
    print()

    print("Последовательные приближения:")
    for iteration, values, bound in history:
        line = f"k={iteration:3d}:"
        for value in values:
            line += f" {value: .8f}"
        if bound is not None:
            line += f"  оценка={bound:.2e}"
        print(line)

    print()
    print_result("7. Метод простых итераций", matrix, rhs, solution)
    print(f"tau = 0.1; q = {q:.6f}; q < 1")
    print(f"Точность = 1e-6; итераций = {len(history) - 1}")
    print(f"Апостериорная оценка погрешности = {error_bound:.3e}")

