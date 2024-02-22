INT_PRECISION = 0.005
FLOAT_PRECISION = 0.05


def add(a: float, b: float) -> float:
    """Сложение"""
    return a + b


def sub(a: float, b: float) -> float:
    """Вычитание"""
    return a - b


def _mul_pos_int(a: int, b: int) -> int:
    """Умножение натуральных чисел"""
    if a < b:
        a, b = b, a

    if b == 1:
        return a

    sums = dict()
    subsum, count = a, 1
    while count <= b:
        sums.update({count: subsum})
        subsum += subsum
        count += count

    result, rest = 0, b
    for i in sorted(sums.keys(), reverse=True):
        if rest >= i:
            rest -= i
            result += sums[i]

    return result


def _to_int(a: float) -> tuple[int, int]:
    """
    Возвращает количество значащих знаков после десятичной точки и число без десятичной точки.
    Пример: to_int(3.14150) => (4, 31415)
    """
    integer, _, decimal = str(a).partition(".")
    return len(decimal), int(integer + decimal)


def mul(a: float, b: float) -> float:
    """Умножение"""
    if a == 0 or b == 0:
        return 0

    negative = a < 0 < b or a > 0 > b

    decimal_digits_a, int_a = _to_int(abs(a))
    decimal_digits_b, int_b = _to_int(abs(b))

    result_decimal_digits = decimal_digits_a + decimal_digits_b

    result = _mul_pos_int(int_a, int_b)
    if result_decimal_digits > 0:
        digits_list = list(str(result))
        digits_list[-result_decimal_digits:] = ['.'] + digits_list[-result_decimal_digits:]
        result = float(''.join(digits_list))

    if negative:
        return -result
    else:
        return result


def div(a: float, b: float) -> float:
    """Деление"""
    # TODO использовать только + и -
    return a / b


def mod(a: float, b: float) -> float:
    """Остаток от деления"""
    # TODO использовать только + и -
    return float(a) % float(b)


def power(a: float, b: float) -> float:
    """Возведение в натуральную степень"""
    # TODO использовать только + и -
    return float(a) ** float(b)


def sqrt(a: str) -> float:
    """Извлечение квадратного корня"""
    # TODO использовать только + и -
    return float(a) ** 0.5


def solve(s: list) -> float:
    """Решение простого уравнения с одним неизвестным"""
    # TODO решение простых примеров
    return 0


if __name__ == "__main__":
    x, y = 2.598347, -3.3984759475
    # print(_mul_pos_int(40347590, 5394570))
    # print(_to_int(-0))
    print(mul(x, y))
    print(x * y)
