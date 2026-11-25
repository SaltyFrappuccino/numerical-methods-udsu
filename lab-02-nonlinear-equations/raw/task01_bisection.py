# ЛР2, задание 1. Половинное деление. Вариант 11.

# Сохраняем отрезок со сменой знака f. Берём его середину и выбираем
# половину, в которой находится корень. Оценка ошибки — (b-a)/2.
# Для нашего f: f(2)<0, f(4)>0, f непрерывна на [2,4].

from math import log


# Исходные параметры варианта 11.
EPS = 1e-8
MAX_ITERATIONS = 1000
LEFT = 2.0
RIGHT = 4.0


def equation(x):
    # Левая часть исходного уравнения. log(x) — натуральный логарифм.
    return -log(x) + 0.2 * x * x - 1.0


def bisection(left, right, eps, max_iterations):
    # Вычисляем значения f на двух концах исходного отрезка.
    left_value = equation(left)
    right_value = equation(right)
    # Если знаки одинаковые, условие метода половинного деления не подтверждено.
    if left_value * right_value > 0:
        raise ValueError("На концах отрезка нет смены знака")
    # Если левый конец уже является корнем, возвращаем его.
    if left_value == 0.0:
        return left, [[0, left, 0.0, 0.0]]
    # То же самое для правого конца.
    if right_value == 0.0:
        return right, [[0, right, 0.0, 0.0]]

    # История: [номер уточнения, x, невязка, верхняя оценка ошибки].
    history = []
    # Строка 0 соответствует середине исходного отрезка до его сужения.
    for iteration in range(max_iterations + 1):
        # Вычисляем середину отрезка: c = (a+b)/2.
        middle = (left + right) / 2.0
        # Вычисляем f(c), чтобы определить знак и невязку.
        value = equation(middle)
        # Корень находится внутри отрезка, значит ошибка середины не больше половины его длины.
        error = (right - left) / 2.0
        # Если при вычислении получили точный ноль, дополнительное уточнение не нужно.
        if value == 0.0:
            error = 0.0
        # Записываем приближение, |f(c)| и оценку погрешности.
        history.append([iteration, middle, abs(value), error])
        # Останавливаемся по верхней оценке. eps/2 — запас точности.
        if error <= eps / 2.0:
            return middle, history
        # Ограничение числа уточнений.
        if iteration == max_iterations:
            break
        # Проверяем, что отрезок ещё можно делить при машинном округлении.
        if middle == left or middle == right:
            raise RuntimeError("Деление отрезка остановилось из-за округления")

        # Смена знака слева от середины: оставляем [left, middle].
        if left_value * value < 0.0:
            right = middle
        # Иначе оставляем [middle, right].
        else:
            left = middle
            # Запоминаем f нового левого конца.
            left_value = value

    # Если допуск не достигнут, сообщаем об этом.
    raise RuntimeError("Половинное деление, превышен предел итераций")


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
    x, history = bisection(LEFT, RIGHT, EPS, MAX_ITERATIONS)
    print_scalar_result("1. Половинное деление", history)


if __name__ == "__main__":
    main()
