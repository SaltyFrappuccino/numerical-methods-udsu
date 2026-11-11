from .data import equation, system_values


# Задания 1-5, вывод приближений, невязки и оценки погрешности x.
def print_scalar_result(title, history):
    print(title)
    print("  k              x        |f(x)|      Оценка ошибки x")
    for row in history:
        iteration, x, residual, error = row
        print(f"{iteration:3d} {x:14.8f} {residual:13.3e} {error:19.3e}")

    print(f"Ответ x = {history[-1][1]:.8f}")
    print("Итераций =", len(history) - 1)
    print()


# Задания 6-7, вывод приближений и невязок двух уравнений.
def print_system_result(title, history):
    print(title)
    print("  k              x              y      Невязка          Psi       Шаг")
    for row in history:
        iteration, x, y, residual, psi, step = row
        print(
            f"{iteration:3d} {x:14.8f} {y:14.8f} "
            f"{residual:12.3e} {psi:12.3e} {step:9.5f}"
        )

    x = history[-1][1]
    y = history[-1][2]
    first, second = system_values(x, y)
    print(f"Ответ x = {x:.8f}, y = {y:.8f}")
    print(f"F1 = {first:.3e}, F2 = {second:.3e}")
    print("Итераций =", len(history) - 1)
    print()


# Задание 8, сравнение результатов скалярных методов и методов для системы.
def print_comparison(scalar_results, system_results):
    print("8. Сравнение результатов")
    print("Уравнение")
    print("Метод                       Итераций              x      Невязка    Оценка ошибки x")
    smallest = scalar_results[0][1]
    largest = smallest
    for name, x, history in scalar_results:
        residual = abs(equation(x))
        error = history[-1][3]
        iterations = len(history) - 1
        print(
            f"{name:28s} {iterations:7d} {x:14.8f} "
            f"{residual:12.3e} {error:18.3e}"
        )
        if x < smallest:
            smallest = x
        if x > largest:
            largest = x
    print(f"Разброс ответов = {largest - smallest:.3e}")
    print()

    print("Система")
    print("Метод                       Итераций              x              y      Невязка")
    for name, x, y, history in system_results:
        first, second = system_values(x, y)
        residual = max(abs(first), abs(second))
        iterations = len(history) - 1
        print(
            f"{name:28s} {iterations:7d} {x:14.8f} "
            f"{y:14.8f} {residual:12.3e}"
        )
    difference_x = abs(system_results[0][1] - system_results[1][1])
    difference_y = abs(system_results[0][2] - system_results[1][2])
    print(f"Различие ответов = {max(difference_x, difference_y):.3e}")
