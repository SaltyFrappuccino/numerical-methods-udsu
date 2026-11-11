from math import cos, log, pi, sin, sqrt


EPS = 1e-8
MAX_ITERATIONS = 1000
LEFT = 2.0
RIGHT = 4.0
START_X = -1.0
START_Y = 0.0
DESCENT_STEP = 0.25


# Задания 1-5, левая часть уравнения варианта 11.
def equation(x):
    return -log(x) + 0.2 * x * x - 1.0


# Задания 2-5 и 8, производная уравнения.
def derivative(x):
    return -1.0 / x + 0.4 * x


# Задание 5, выражение x = sqrt(5 * (ln(x) + 1)).
def iteration_function(x):
    return sqrt(5.0 * (log(x) + 1.0))


# Задание 5, производная функции итерации для оценки сходимости.
def iteration_derivative(x):
    return 5.0 / (2.0 * x * iteration_function(x))


# Задания 6-8, левые части двух уравнений варианта 11.
def system_values(x, y):
    first = sin(-x + pi / 2.0 + 2.0) + y
    second = cos(-y + pi / 2.0 - 0.5) - x - 1.0
    return first, second


# Задания 6-7, матрица частных производных системы.
def jacobian(x, y):
    return [
        [-cos(-x + pi / 2.0 + 2.0), 1.0],
        [-1.0, sin(-y + pi / 2.0 - 0.5)]
    ]
