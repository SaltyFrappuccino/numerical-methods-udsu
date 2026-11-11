from .data import standard_system, symmetric_system, tridiagonal_system
from .linear_methods import gauss_elimination, gauss_jordan, solve_lu
from .matrix_utils import residual
from .special_methods import solve_orthogonalization, solve_square_roots, thomas_method


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


def main():
    print("Лабораторная работа 1, вариант 11, задания 1-6")
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
