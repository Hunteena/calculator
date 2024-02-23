from typing import Union

INT_PRECISION = 0.005
FLOAT_PRECISION = 0.05
PRECISION = 4


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

    products = dict()
    subsum, count = a, 1
    while count <= b:
        products.update({count: subsum})
        subsum += subsum
        count += count

    result, rest = 0, b
    for i in sorted(products.keys(), reverse=True):
        if rest >= i:
            rest -= i
            result += products[i]

    return result


def _to_int(a: float) -> tuple[int, int]:
    """
    Возвращает количество значащих знаков после десятичной точки и число без десятичной точки.
    Пример: _to_int(3.14150) => (4, 31415)
    """
    integer, _, decimal = str(a).partition(".")
    return len(decimal), int(integer + decimal)


def _point_shift(a: float, k: int) -> float:
    """
    Сдвигает десятичную точку в a на k позиций вправо, если k положительное,
    или на |k| влево, если k отрицательное
    """
    if k == 0:
        return a

    integer, _, decimal = str(a).partition(".")

    if k > 0:
        digits_list = list(decimal)
        if k > len(decimal):
            digits_list += ['0' for i in range(k - len(decimal))]
        digits_list[k:] = ['.'] + digits_list[k:]
        decimal = ''.join(digits_list)
    else:
        digits_list = list(integer)
        if abs(k) > len(integer):
            digits_list = ['0' for i in range(abs(k) - len(integer))] + digits_list
        digits_list[len(digits_list)-abs(k):] = ['.'] + digits_list[len(digits_list)-abs(k):]
        integer = ''.join(digits_list)
    return float(integer + decimal)


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
        result = _point_shift(result, -result_decimal_digits)

    if negative:
        return -result
    else:
        return result


def _div_mod(a: float, b: float) -> tuple[int, float]:
    """Для положительных a и b возвращает целую часть частного и остаток от деления"""
    products = dict()
    subsum, count = b, 1
    while subsum <= a:
        products.update({count: subsum})
        subsum += subsum
        count += count

    quotient, remainder = 0, a
    for i in sorted(products.keys(), reverse=True):
        if remainder >= products[i]:
            remainder -= products[i]
            quotient += i

    return quotient, remainder


def div(a: float, b: float) -> Union[float, str]:
    """Деление"""
    if b == 0:
        return "Деление на ноль"
    elif a == 0:
        return 0

    negative = a < 0 < b or a > 0 > b

    integer, remainder = _div_mod(abs(a), abs(b))
    decimal, _ = _div_mod(_point_shift(remainder, PRECISION), abs(b))
    result = float(str(integer) + '.' + str(decimal))

    if negative:
        return -result
    else:
        return result


def mod(a: float, b: float) -> Union[float, str]:
    """Остаток от деления"""
    if b == 0:
        return "Деление на ноль"
    elif a == 0:
        return 0

    _, result = _div_mod(abs(a), abs(b))
    if a < 0 < b or a > 0 > b:
        result -= abs(b)
    if a < 0:
        result = -result
    return result


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
    x, y = 834825.397, 452.3400
    # print(_mul_pos_int(40347590, 5394570))
    # print(_to_int(-0))
    # print(mul(x, y))
    # print(x * y)
    # print(mod(x, y))
    # print(x % y)
    # print(_point_shift(3141, -4))
    print(div(x, y))
    print((x / y))
