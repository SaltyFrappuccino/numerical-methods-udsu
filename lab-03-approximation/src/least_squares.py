def fit_line(xs, ys):
    """Находит коэффициенты Q₁(x) = a₀ + a₁x методом наименьших квадратов."""
    if len(xs) != len(ys) or len(xs) < 2:
        raise ValueError("Нужно как минимум две пары координат x и y")

    S0 = len(xs)
    S1 = sum(xs)
    S2 = sum(x**2 for x in xs)
    t0 = sum(ys)
    t1 = sum(xs[i] * ys[i] for i in range(S0))

    factor = S1 / S0
    left = S2 - factor * S1
    right = t1 - factor * t0

    if abs(left) < 1e-12:
        raise ValueError("Коэффициенты прямой нельзя определить: недостаточно разных x")

    a1 = right / left
    a0 = (t0 - S1 * a1) / S0

    return a0, a1, (S0, S1, S2, t0, t1)


def line_value(x, a0, a1):
    """Вычисляет значение найденной прямой при заданном x."""
    return a0 + a1 * x


def squared_error(xs, ys, a0, a1):
    """Вычисляет сумму квадратов отклонений прямой от табличных точек."""
    S = 0.0

    for i in range(len(xs)):
        Q = line_value(xs[i], a0, a1)
        difference = Q - ys[i]
        S += difference**2

    return S
