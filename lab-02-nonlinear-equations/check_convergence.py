from src.data import EPS, MAX_ITERATIONS, START_X, START_Y, jacobian
from src.system_methods import newton_system


def main():
    x, y, history = newton_system(START_X, START_Y, EPS, MAX_ITERATIONS)
    for row in history[:4]:
        k, x, y, residual, psi, step = row
        j = jacobian(x, y)
        determinant = j[0][0] * j[1][1] - j[0][1] * j[1][0]
        print(f"k={k}: ({x:.12f}, {y:.12f}), det J={determinant:.12f}")
        if k < 2:
            assert abs(determinant) > 1e-14
    x2, y2 = history[2][1:3]
    x3, y3 = history[3][1:3]
    correction = max(abs(x3 - x2), abs(y3 - y2))
    distance = min(x2 + 0.3, 0.1 - x2, y2 - 0.3, 0.8 - y2)
    bound = 0.04 / (1.0 - 0.04)
    print("Норма поправки d2:", correction)
    print("Расстояние до границы D:", distance)
    print("Верхняя граница суммы поправок:", bound)
    assert -0.105 < x2 < -0.104 and 0.523 < y2 < 0.525
    assert correction < 0.04 and bound < distance
    print("Численные предпосылки выполнены. Аналитическое доказательство в README.md.")


if __name__ == "__main__":
    main()
