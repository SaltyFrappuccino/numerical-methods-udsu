from fractions import Fraction
from src.power_method import A


def determinant(matrix):
    a = []
    for row in matrix:
        a.append(row[:])
    result = Fraction(1)
    for i in range(len(a)):
        pivot = i
        while pivot < len(a) and a[pivot][i] == 0:
            pivot += 1
        if pivot == len(a):
            return Fraction(0)
        if pivot != i:
            a[i], a[pivot] = a[pivot], a[i]
            result = -result
        result *= a[i][i]
        for j in range(i + 1, len(a)):
            factor = a[j][i] / a[i][i]
            for k in range(i, len(a)):
                a[j][k] -= factor * a[i][k]
    return result


def main():
    matrix = []
    for row in A:
        matrix.append([Fraction(str(value)) for value in row])
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            assert matrix[i][j] == matrix[j][i]
    print("Матрица симметрична")
    for size in range(1, n + 1):
        minor = []
        for row in matrix[:size]:
            minor.append(row[:size])
        value = determinant(minor)
        print(f"Минор {size}: {value} = {float(value):.10g}")
        assert value > 0

    v = [Fraction(1)] * n
    columns = [v]
    for k in range(1, n):
        next_v = []
        for row in matrix:
            value = Fraction(0)
            for j in range(n):
                value += row[j] * v[j]
            next_v.append(value)
        v = next_v
        columns.append(v)
    krylov = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(columns[j][i])
        krylov.append(row)
    value = determinant(krylov)
    print("det K =", value)
    assert value != 0
    print("Условия сходимости для начального вектора проверены.")


if __name__ == "__main__":
    main()
