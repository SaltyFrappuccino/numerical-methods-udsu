from .data import XS, YS
from .least_squares import fit_line, line_value, squared_error


def main():
    """Строит прямую МНК для варианта 11 и проверяет результат."""
    a0, a1, sums = fit_line(XS, YS)
    S0, S1, S2, t0, t1 = sums

    print("ЛР №3, задание №8, вариант 11")
    print("Метод наименьших квадратов")
    print()
    print(f"S0 = {S0}")
    print(f"S1 = {S1}")
    print(f"S2 = {S2}")
    print(f"t0 = {t0:.6f}")
    print(f"t1 = {t1:.6f}")
    print()
    print("Нормальная система:")
    print(f"{S0}*a0 + {S1}*a1 = {t0:.6f}")
    print(f"{S1}*a0 + {S2}*a1 = {t1:.6f}")
    print()
    print(f"a0 = {a0:.9f}")
    print(f"a1 = {a1:.9f}")
    print(f"Q1(x) = {a0:.9f} + ({a1:.9f})*x")
    print()
    print(" x       y          Q1(x)       Q1(x)-y     (Q1(x)-y)^2")

    for i in range(len(XS)):
        x = XS[i]
        y = YS[i]
        Q = line_value(x, a0, a1)
        difference = Q - y
        print(f"{x:2}  {y:9.5f}  {Q:12.8f}  {difference:12.8f}  {difference**2:14.9f}")

    S = squared_error(XS, YS, a0, a1)
    print()
    print(f"Сумма квадратов отклонений: S = {S:.9f}")

    first = S0 * a0 + S1 * a1 - t0
    second = S1 * a0 + S2 * a1 - t1

    if abs(first) > 1e-10 or abs(second) > 1e-10:
        raise ArithmeticError("Проверка нормальной системы не пройдена")

    print("Проверка нормальной системы пройдена")
