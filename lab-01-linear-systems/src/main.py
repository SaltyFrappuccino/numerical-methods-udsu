from .data import standard_system
from .linear_methods import gauss_elimination, gauss_jordan, solve_lu
from .matrix_utils import residual
from .power_method import main as power_main


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


# Выполняет задания 1–3 и 14, вариант 11.
def main():
    print("Лабораторная работа 1, вариант 11, задания 1-3, 14")
    print()

    matrix, rhs = standard_system()
    print("Задания 1-3")
    print_system(matrix, rhs)

    solution = gauss_elimination(matrix, rhs)
    print_result("1. Метод Гаусса", matrix, rhs, solution)

    solution = gauss_jordan(matrix, rhs)
    print_result("2. Метод Жордана-Гаусса", matrix, rhs, solution)

    solution = solve_lu(matrix, rhs)
    print_result("3. LU-разложение", matrix, rhs, solution)

    print("14. Степенной метод")
    power_main()
