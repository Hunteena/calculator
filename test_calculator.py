import pytest

from calculator import main
from operations import mul, div, mod, power, sqrt, INT_PRECISION, FLOAT_PRECISION, solve, InvalidInputError

test_data = [
    (123456, 789),
    (-123456, 789),
    (123456, -789),
    (-123456, -789),
    (123.456, 78.9),
    (123.456, -78.9),
    (-123.456, 78.9),
    (-123.456, -78.9),
    (1, 1000000),
    (0, 3.1415),
    (3.1415, 0),
    (0, 0),
    (100001, 20),
    (101, 20),
    (0.123456, 0.00789),
    (1, 10000000.01),
    (1, 1000000001),
    (1.2, -4),
    (123456, 7)
]


@pytest.mark.parametrize('a, b', test_data)
def test_mul(a, b):
    if a == 0 or b == 0:
        result = mul(a, b) == 0
    else:
        a, b = float(a), float(b)
        expected_result = a * b
        precision = INT_PRECISION if a.is_integer() and b.is_integer() else FLOAT_PRECISION
        result = abs(mul(a, b) - expected_result) / expected_result <= precision

    assert result is True


@pytest.mark.parametrize('a, b', test_data)
def test_div(a, b):
    a, b = float(a), float(b)
    if b == 0:
        with pytest.raises(InvalidInputError):
            div(a, b)
    elif a == 0:
        assert div(a, b) == 0
    else:
        expected_result = a / b
        precision = INT_PRECISION if a.is_integer() and b.is_integer() else FLOAT_PRECISION
        assert abs(div(a, b) - expected_result) / expected_result <= precision


@pytest.mark.parametrize('a, b', test_data)
def test_mod(a, b):
    if b == 0:
        with pytest.raises(InvalidInputError):
            mod(a, b)
    else:
        expected_result = a % b
        assert mod(a, b) == expected_result


@pytest.mark.parametrize('a, b', test_data[2:])
def test_power(a, b):
    a, b = float(a), float(b)
    if not b.is_integer() or a == 0 and b < 0:
        with pytest.raises(InvalidInputError):
            power(a, b)
    elif b == 0:
        assert power(a, b) == 1
    elif a == 0:
        assert power(a, b) == 0
    else:
        try:
            expected_result = a ** b
            precision = INT_PRECISION if a.is_integer() and b.is_integer() else FLOAT_PRECISION
            assert abs(power(a, b) - expected_result) / expected_result <= precision
        except OverflowError:
            assert power(a, b) == float('inf')
        except ZeroDivisionError:
            assert power(a, b) == 0


@pytest.mark.parametrize('a, b', test_data[:2])
def test_power_too_big(a, b):
    a, b = float(a), float(b)
    with pytest.raises(InvalidInputError):
        power(a, b)


@pytest.mark.parametrize('a', [0, 4, 3.1415, -1])
def test_sqrt(a):
    a = float(a)
    if a == 0:
        assert sqrt(a) == 0
    elif a < 0:
        with pytest.raises(InvalidInputError):
            sqrt(a)
    else:
        expected_result = a ** 0.5
        precision = INT_PRECISION if a.is_integer() else FLOAT_PRECISION
        assert abs(sqrt(a) - expected_result) / expected_result <= precision


@pytest.mark.parametrize('equation, expected_result', [
    ('1 + x = 3', 2),
    ('3 - x = 1', 2),
    ('2 * x = 6', 3),
    ('6 / x = 3', 2),
    ('x + 1 = 3', 2),
    ('x - 1 = 3', 4),
    ('x * 2 = 6', 3),
    ('x / 2 = 3', 6),
    ('x / 0 = 7', None),
])
def test_solve(equation, expected_result):
    a, oper, b, eq, c = equation.split()
    print(oper, b)
    if oper == '/' and b.isdigit() and int(b) == 0:
        with pytest.raises(InvalidInputError):
            solve(*equation.split())
    else:
        _, result = solve(*equation.split())
        assert result == expected_result


@pytest.mark.parametrize('task, expected_result', [
    ('120 + 5', '125.0'),
    ('1 + x = 3', 'x = 2.0'),
])
def test_main(task, expected_result):
    assert main(*task.split()) == expected_result


@pytest.mark.parametrize('task', [
    'x',
    'x / 0 =',
    '8 & 0',
    'x - y = 0',
    'x * 5 - 8 = 0',
])
def test_main_errors(task):
    with pytest.raises(InvalidInputError):
        main(*task.split())
