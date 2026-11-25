# ЛР2, задание 5. Метод простых итераций. Вариант 11.

# Преобразуем f(x)=0 к виду x=phi(x)=sqrt(5*(ln(x)+1)).
# Проверяем phi([2,4]) в [2,4] и q=max |phi'|<1.
# Начинаем с x0=3, повторяем x_(k+1)=phi(x_k), формула (24).
# Остановка по апостериорной оценке q/(1-q)*|x_(k+1)-x_k|.

from math import log, sqrt


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


def iteration_function(x):
    # Из f(x) = 0 выражаем x: x = sqrt(5*(ln(x)+1)).
    return sqrt(5.0 * (log(x) + 1.0))


def iteration_derivative(x):
    # Производная phi'(x). Нужна для оценки коэффициента сжатия q.
    return 5.0 / (2.0 * x * iteration_function(x))


def simple_iterations(x, eps, max_iterations):
    # phi'(x) положительна и убывает на [2,4],
    # поэтому q = max |phi'(x)| = phi'(2) ≈ 0.429613.
    q = iteration_derivative(LEFT)
    # Проверяем условие сжатия для нашего варианта.
    if not 0.0 < q < 1.0:
        raise ValueError("Условие сходимости не выполнено")
    # Начальное приближение должно принадлежать отрезку.
    if not LEFT <= x <= RIGHT:
        raise ValueError("Начальное приближение вне отрезка")
    # Проверяем phi(2). Функция phi возрастает, поэтому достаточно проверить оба конца.
    if not LEFT <= iteration_function(LEFT) <= RIGHT:
        raise ValueError("Функция итераций выходит за отрезок слева")
    # Проверяем phi(4), чтобы phi отображала весь [2,4] в себя.
    if not LEFT <= iteration_function(RIGHT) <= RIGHT:
        raise ValueError("Функция итераций выходит за отрезок справа")

    # До первой итерации нет двух приближений. Оцениваем начальную
    # ошибку через |f(x0)|/m, где m = f'(2) = 0.3.
    initial_error = abs(equation(x)) / derivative(LEFT)
    # Записываем начальное приближение и его невязку с оценкой ошибки.
    history = [[0, x, abs(equation(x)), initial_error]]

    # Выполняем собственно итерации, начиная с номера 1.
    for iteration in range(1, max_iterations + 1):
        # Основная формула (24): x_(k+1) = phi(x_k).
        x_next = iteration_function(x)
        # Контролируем принадлежность нового приближения отрезку.
        if not LEFT <= x_next <= RIGHT:
            raise RuntimeError("Простые итерации вышли за отрезок")

        # Находим разность двух соседних приближений по модулю.
        difference = abs(x_next - x)
        # Апостериорная верхняя оценка погрешности: q/(1-q) * |x_(k+1)-x_k|.
        error = q * difference / (1.0 - q)
        # Невязка исходного уравнения |f(x_next)|, не ошибка по x.
        residual = abs(equation(x_next))
        # Запоминаем новый x и обе меры точности.
        history.append([iteration, x_next, residual, error])

        # Останавливаемся по верхней оценке, а не только по невязке.
        # eps/2 — дополнительный запас относительно eps.
        if error <= eps / 2.0:
            return x_next, history

        # Новое приближение становится текущим для следующего шага.
        x = x_next

    # Предел итераций исчерпан, заданная точность не достигнута.
    raise RuntimeError("Простые итерации, превышен предел итераций")


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
    print(f"phi(x) = sqrt(5*(ln(x) + 1)), x0 = 3, q = {iteration_derivative(LEFT):.6f}")
    x, history = simple_iterations(3.0, EPS, MAX_ITERATIONS)
    print_scalar_result("5. Простые итерации", history)


if __name__ == "__main__":
    main()
