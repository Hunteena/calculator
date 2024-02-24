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
]


class TestFunctions:
    @pytest.mark.parametrize('a, b', test_data)
    def test_mul(self, a, b):
        expected_result = a * b
        assert mul(a, b) == expected_result

    @pytest.mark.parametrize('a, b', test_data)
    def test_div(self, a, b):
        a, b = float(a), float(b)
        if b == 0:
            assert div(a, b) == ERROR_TEXT['zero_division']
        elif a == 0:
            assert div(a, b) == 0
        else:
            expected_result = a / b
            precision = INT_PRECISION if a.is_integer() and b.is_integer() else FLOAT_PRECISION
            assert abs(div(a, b) - expected_result) / expected_result <= precision

    @pytest.mark.parametrize('a, b', test_data)
    def test_mod(self, a, b):
        expected_result = a % b if b else ERROR_TEXT['zero_division']
        assert mod(a, b) == expected_result

    @pytest.mark.parametrize('a, b', test_data)
    def test_power(self, a, b):
        a, b = float(a), float(b)
        if b == 0:
            assert power(a, b) == 1
        elif a == 0:
            assert power(a, b) == 0
        elif a < 0:
            assert power(a, b) == ERROR_TEXT['negative_power']
        else:
            expected_result = a ** b
            precision = INT_PRECISION if a.is_integer() and b.is_integer() else FLOAT_PRECISION
            assert abs(power(a, b) - expected_result) / expected_result <= precision

    @pytest.mark.parametrize('a', [0, 4, 3.1415, -1])
    def test_sqrt(self, a):
        a = float(a)
        if a == 0:
            assert sqrt(a) == 0
        elif a < 0:
            assert sqrt(a) == ERROR_TEXT['negative_sqrt']
        else:
            expected_result = a ** 0.5
            precision = INT_PRECISION if a.is_integer() else FLOAT_PRECISION
            assert abs(sqrt(a) - expected_result) / expected_result <= precision

    @pytest.mark.parametrize('s, expected_result', test_data)
    def test_solve(self, s, expected_result):
        pass
