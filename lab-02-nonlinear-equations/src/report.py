import json
from math import cos, sin
from pathlib import Path

from .data import LEFT, RIGHT, EPS, MAX_ITERATIONS, START_X, START_Y, DESCENT_STEP
from .data import equation, system_values
from .scalar_methods import bisection, newton, chords, combined, simple_iterations
from .system_methods import newton_system, gradient_descent


def grid(left, right, count):
    return [left + (right - left) * i / (count - 1) for i in range(count)]


def scalar_results():
    methods = [
        (1, 'Половинное деление', bisection(LEFT, RIGHT, EPS, MAX_ITERATIONS), '(b − a) / 2'),
        (2, 'Ньютон', newton(RIGHT, EPS, MAX_ITERATIONS), '|f(x)| / m'),
        (3, 'Секущие', chords(LEFT, RIGHT, EPS, MAX_ITERATIONS), '|f(x)| / m'),
        (4, 'Комбинированный', combined(LEFT, RIGHT, EPS, MAX_ITERATIONS), '(b − a) / 2'),
        (5, 'Простые итерации', simple_iterations(3.0, EPS, MAX_ITERATIONS), 'q · |Δx| / (1 − q)')
    ]
    results = []
    for number, name, result, bound in methods:
        x, history = result
        results.append(dict(number=number, name=name, x=x,
                            iterations=history[-1][0], residual=abs(equation(x)),
                            error=history[-1][3], bound=bound, history=history,
                            values=[equation(row[1]) for row in history]))
    return results


def system_results():
    methods = [(6, 'Ньютон', newton_system), (7, 'Спуск', gradient_descent)]
    results = []
    for number, name, method in methods:
        x, y, history = method(START_X, START_Y, EPS, MAX_ITERATIONS)
        first, second = system_values(x, y)
        results.append(dict(number=number, name=name, x=x, y=y, first=first, second=second,
                            residual=max(abs(first), abs(second)), iterations=history[-1][0],
                            history=history, psi=history[-1][4]))
    return results


def build_report():
    scalar = scalar_results()
    system = system_results()
    xs = grid(LEFT, RIGHT, 601)
    curve = dict(x=xs, y=[equation(x) for x in xs])

    # Кривые F1 = 0 и F2 = 0.
    xs = grid(-2.2, 0.5, 501)
    ys = grid(-1.2, 1.2, 501)
    curves = [dict(x=xs, y=[-cos(2 - x) for x in xs]),
              dict(x=[sin(y + 0.5) - 1 for y in ys], y=ys)]

    # Поверхность Psi(x, y) = F1(x, y)^2 + F2(x, y)^2.
    xs = grid(-2.0, 0.5, 61)
    ys = grid(-1.0, 1.0, 61)
    z = []
    for y in ys:
        row = []
        for x in xs:
            first, second = system_values(x, y)
            row.append(first * first + second * second)
        z.append(row)

    data = dict(scalar=scalar, system=system, eps=EPS, limit=EPS / 2,
                start=[START_X, START_Y], descent_step=DESCENT_STEP,
                curve=curve, curves=curves, surface=dict(x=xs, y=ys, z=z),
                scalar_spread=max(m['x'] for m in scalar) - min(m['x'] for m in scalar),
                system_spread=max(abs(system[0][key] - system[1][key]) for key in ('x', 'y')))
    directory = Path(__file__).parent
    template = (directory / 'report_template.html').read_text(encoding='utf-8')
    parts = {
        '__REPORT_CSS__': (directory / 'report.css').read_text(encoding='utf-8'),
        '__REPORT_JS__': (directory / 'report.js').read_text(encoding='utf-8'),
        '__PLOTLY__': (directory / 'vendor' / 'plotly.min.js').read_text(encoding='utf-8'),
        '__PLOTLY_LICENSE__': (directory / 'vendor' / 'LICENSE.txt').read_text(encoding='utf-8'),
        '__REPORT_DATA__': json.dumps(data, ensure_ascii=False, allow_nan=False),
    }
    for key, value in parts.items():
        template = template.replace(key, value)
    output = directory.parent / 'LR2_comparison.html'
    output.write_text(template, encoding='utf-8')
    print(output)


if __name__ == '__main__':
    build_report()
