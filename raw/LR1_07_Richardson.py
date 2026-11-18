# -*- coding: utf-8 -*-
"""
ЛР1, задание №7, вариант 11. ПРОСТЫЕ ИТЕРАЦИИ ДЛЯ СЛАУ (РИЧАРДСОН).

КОРОТКАЯ ШПАРГАЛКА ДЛЯ ЗАЩИТЫ
1. Дана система из пяти линейных уравнений A*x = b.
2. По §1.6 учебника преобразуем её к x = B*x + c.
3. Выбираем S = tau*I (стационарный метод Ричардсона), tau = 0.1.
   Так как I*A=A и I*b=b: B = I-tau*A, c = tau*b.
4. Проверяем q = ||B||_infinity = максимальная сумма модулей элементов
   строки B. Получаем q = 0.973 < 1 — достаточное условие сходимости.
5. Начинаем с x^(0) = (0,0,0,0,0). Повторяем x_next = B*x + c.
6. Считаем difference = max_i|x_next[i]-x[i]| и верхнюю оценку
   error_bound = q/(1-q)*difference. При error_bound <= eps останавливаемся.
7. Проверяем исходную систему невязкой ||A*x-b||_infinity.

Собрана настоящая функция из нашего src/linear_methods.py вместе
с исходной системой из src/data.py и проверкой из src/matrix_utils.py.
"""


def standard_system():
    # Исходная система Ax=b для варианта 11 и задания №7.
    # Каждая строка matrix — коэффициенты одного из пяти уравнений.
    matrix = [
        [2.6, 1.3, 0.0, 0.5, 0.0],
        [1.3, 2.6, 0.78, 0.0, 0.25],
        [0.0, 0.78, 10.0, -0.78, 1.25],
        [0.52, 0.0, -0.78, 2.6, -0.26],
        [0.0, 0.26, 1.3, -0.26, 2.6],
    ]

    # Правые части пяти уравнений.
    # ВАЖНО: третий элемент именно -10.4472, как в нашем архиве.
    rhs = [-2.262, -1.534, -10.4472, 0.3952, -2.5844]
    return matrix, rhs


def simple_iterations(matrix, rhs, eps=1e-6, max_iterations=10000, tau=0.1):
    # Число неизвестных = число уравнений = 5.
    size = len(rhs)

    # ГОТОВИМ ПРЕОБРАЗОВАНИЕ: B = I - tau*A, c = tau*b.
    # Исходный учебник задаёт B = I-S*A, c=S*b; мы выбрали S=tau*I.
    B = []
    for i in range(size):               # Перебираем строки B.
        row = []                         # Создаём новую строку.
        for j in range(size):           # Перебираем её столбцы.
            if i == j:
                # На главной диагонали единичной матрицы I стоит 1.
                value = 1.0 - tau * matrix[i][j]
            else:
                # В остальных элементах единичной матрицы I стоит 0.
                value = 0.0 - tau * matrix[i][j]
            row.append(value)           # Добавляем элемент в строку B.
        B.append(row)                   # Добавляем строку в матрицу B.

    # Теперь считаем c = tau*b, умножая каждый элемент rhs на tau.
    c = []
    for i in range(size):
        c.append(tau * rhs[i])

    # ПРОВЕРКА СХОДИМОСТИ: q = ||B||_infinity < 1.
    # Норма — максимальная сумма МОДУЛЕЙ элементов одной строки.
    q = 0.0
    for row in B:                       # Смотрим очередную строку B.
        row_sum = 0.0                    # Её сумма пока нулевая.
        for value in row:
            row_sum = row_sum + abs(value)  # Модули нужны для нормы.
        if row_sum > q:
            q = row_sum                 # Сохраняем наибольшую сумму.

    # Если q>=1, это достаточное условие не даёт гарантии сходимости.
    if q >= 1.0:
        raise ValueError("Норма B >= 1: достаточное условие сходимости не выполнено")

    # Выбираем x^(0) — пять нулей. Это наше первое ПРЕДПОЛОЖЕНИЕ.
    x = [0.0] * size

    # История итераций для преподавателя.
    # На шаге 0 оценки ещё нет, поэтому сохраняем None.
    history = [(0, x[:], None)]

    # Повторяем основную формулу x^(k+1) = B*x^(k) + c.
    for iteration in range(1, max_iterations + 1):
        x_next = []

        # Вычисляем пять компонентов НОВОГО приближения по очереди.
        for i in range(size):
            value = 0.0                 # Сумма произведений в i-й строке.
            for j in range(size):
                # Каждый элемент B[i][j] умножаем на СТАРЫЙ x[j].
                value = value + B[i][j] * x[j]
            # К результату умножения строки B на x прибавляем c[i].
            value = value + c[i]
            x_next.append(value)        # Новая i-я неизвестная готова.

        # Все компоненты x_next уже посчитаны из старого x.
        # Теперь находим наибольшую разницу между новым и старым.
        difference = 0.0
        for i in range(size):
            change = abs(x_next[i] - x[i])
            if change > difference:
                difference = change

        # АПОСТЕРИОРНАЯ ВЕРХНЯЯ ОЦЕНКА ОШИБКИ из §1.6:
        # ||x_next - точное решение||_infinity <= error_bound.
        error_bound = q / (1.0 - q) * difference

        # Сохраняем новое приближение в x для следующей итерации.
        x = x_next

        # Копия x[:] нужна, чтобы история хранила отдельный вектор.
        history.append((iteration, x[:], error_bound))

        # Как только гарантированная оценка ошибки <= eps, заканчиваем.
        if error_bound <= eps:
            return x, B, c, q, history, error_bound

    raise RuntimeError("Метод простых итераций не достиг заданной точности")


# Ниже — вспомогательные функции проверки из src/matrix_utils.py.
def dot(first, second):
    # Скалярное произведение двух векторов: сумма попарных произведений.
    result = 0.0
    for index in range(len(first)):
        result += first[index] * second[index]
    return result


def mat_vec(matrix, vector):
    # Умножение матрицы на вектор: каждую строку умножаем на vector.
    result = []
    for row in matrix:
        result.append(dot(row, vector))
    return result


def vector_norm(vector):
    # Бесконечная норма вектора — максимальный модуль его элемента.
    largest = 0.0
    for value in vector:
        if abs(value) > largest:
            largest = abs(value)
    return largest


def residual(matrix, rhs, solution):
    # Проверяем ИСХОДНУЮ систему A*x=b, а не только преобразованную.
    product = mat_vec(matrix, solution)  # Левые части пяти уравнений A*x.
    difference = []
    for index in range(len(rhs)):
        difference.append(product[index] - rhs[index])  # Компоненты A*x-b.
    return vector_norm(difference)       # Наибольшая невязка по модулю.


def main():
    matrix, rhs = standard_system()  # Берём настоящую A и b из варианта 11.

    # Вызываем наш метод — имя и набор возвращаемых значений сохранены.
    solution, B, c, q, history, error_bound = simple_iterations(
        matrix, rhs, eps=1e-6, max_iterations=10000, tau=0.1
    )

    print("ЛР №1, задание №7, вариант 11")
    print("Стационарный метод Ричардсона")
    print("B = I - 0.1*A")
    for row in B:
        # Матрица B построена ПРОГРАММОЙ, не введена готовыми числами.
        text = ""
        for value in row:
            text += f" {value:8.4f}"
        print(text)

    print("c = 0.1*b")
    print(" ".join(f"{value:.5f}" for value in c))
    print(f"q = {q:.9f} (< 1, сходимость гарантирована)")
    print()
    print("Последовательные приближения:")

    # Показываем все приближения; каждое содержит пять неизвестных.
    for iteration, values, bound in history:
        line = f"k={iteration:3d}:"
        for value in values:
            line += f" {value: .8f}"
        if bound is not None:
            line += f"  оценка={bound:.9e}"
        print(line)

    print()
    print("Ответ:", [round(value, 8) for value in solution])
    print("Количество итераций:", history[-1][0])
    print(f"Верхняя оценка ошибки: {error_bound:.12e}")
    print(f"Невязка исходной системы: {residual(matrix, rhs, solution):.12e}")


if __name__ == "__main__":
    main()
