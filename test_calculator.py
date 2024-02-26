import pytest

from operations import mul, div, mod, power, sqrt, ERROR_TEXT, INT_PRECISION, FLOAT_PRECISION

test_data = [
    (123456, 789),
    (123456, -789),
    (-123456, 789),
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


class TestFunctions:
    @pytest.mark.parametrize('a, b', test_data)
    def test_mul(self, a, b):
        if a == 0 or b == 0:
            result = mul(a, b) == 0
        else:
            a, b = float(a), float(b)
            expected_result = a * b
            precision = INT_PRECISION if a.is_integer() and b.is_integer() else FLOAT_PRECISION
            result = abs(mul(a, b) - expected_result) / expected_result <= precision

        assert result is True

    @pytest.mark.parametrize('a, b', test_data)
    def test_div(self, a, b):
        a, b = float(a), float(b)
        if b == 0:
            result = div(a, b) == ERROR_TEXT['zero_division']
        elif a == 0:
            result = div(a, b) == 0
        else:
            expected_result = a / b
            precision = INT_PRECISION if a.is_integer() and b.is_integer() else FLOAT_PRECISION
            result = abs(div(a, b) - expected_result) / expected_result <= precision

        assert result is True

    @pytest.mark.parametrize('a, b', test_data)
    def test_mod(self, a, b):
        expected_result = a % b if b else ERROR_TEXT['zero_division']
        assert mod(a, b) == expected_result

    @pytest.mark.parametrize('a, b', test_data)
    def test_power(self, a, b):
        a, b = float(a), float(b)
        if not b.is_integer():
            result = power(a, b) == ERROR_TEXT['not_integer_power']
        elif a == 0 and b < 0:
            result = power(a, b) == ERROR_TEXT['negative_power_of_zero']
        elif b == 0:
            result = power(a, b) == 1
        elif a == 0:
            result = power(a, b) == 0
        else:
            try:
                expected_result = a ** b
                precision = INT_PRECISION if a.is_integer() and b.is_integer() else FLOAT_PRECISION
                result = abs(power(a, b) - expected_result) / expected_result <= precision
            except OverflowError:
                result = power(a, b) == float('inf')
            except ZeroDivisionError:
                result = power(a, b) == 0

        assert result is True

    @pytest.mark.parametrize('a', [0, 4, 3.1415, -1])
    def test_sqrt(self, a):
        a = float(a)
        if a == 0:
            result = sqrt(a) == 0
        elif a < 0:
            result = sqrt(a) == ERROR_TEXT['negative_sqrt']
        else:
            expected_result = a ** 0.5
            precision = INT_PRECISION if a.is_integer() else FLOAT_PRECISION
            result = abs(sqrt(a) - expected_result) / expected_result <= precision

        assert result is True

    @pytest.mark.parametrize('s, expected_result', test_data)
    def test_solve(self, s, expected_result):
        pass
