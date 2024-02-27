INT_PRECISION = 0.005
FLOAT_PRECISION = 0.05


class InvalidInputError(Exception):
    def __init__(self, message = "Невозможно вычислить, проверьте ввод данных"):
        self.message = message


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
    number, _, exponent = str(a).partition("e")
    if not exponent:
        integer, _, decimal = str(a).partition(".")
        return len(decimal), int(integer + decimal)
    else:
        return 0, int(float(a))


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
        digits_list[len(digits_list) - abs(k):] = ['.'] + digits_list[len(digits_list) - abs(k):]
        integer = ''.join(digits_list)
    return float(integer + decimal)


def mul(a: float, b: float) -> float:
    """Умножение"""
    if a == 0 or b == 0:
        return 0

    decimal_digits_a, int_a = _to_int(abs(a))
    decimal_digits_b, int_b = _to_int(abs(b))

    result_decimal_digits = decimal_digits_a + decimal_digits_b

    result = _mul_pos_int(int_a, int_b)
    if result_decimal_digits > 0:
        result = _point_shift(result, -result_decimal_digits)

    negative = a < 0 < b or a > 0 > b
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


def _exponent(a: float) -> int:
    """Порядок числа"""
    return int(f"{a:e}"[-3:])


def div(a: float, b: float) -> float:
    """Деление"""
    if b == 0:
        raise InvalidInputError("Деление на ноль")
    elif a == 0:
        return 0

    precision = _exponent(a) - _exponent(b)
    if a.is_integer() and b.is_integer():
        precision += _exponent(INT_PRECISION)
    else:
        precision += _exponent(FLOAT_PRECISION)

    if precision >= 0:
        result, _ = _div_mod(abs(a), abs(b))
    else:
        result, _ = _div_mod(_point_shift(abs(a), -precision), abs(b))
        result = _point_shift(result, precision)

    negative = a < 0 < b or a > 0 > b
    result = float(result)
    if negative:
        return -result
    else:
        return result


def mod(a: float, b: float) -> float:
    """Остаток от деления"""
    if b == 0:
        raise InvalidInputError("Деление на ноль")
    elif a == 0:
        return 0

    _, result = _div_mod(abs(a), abs(b))

    negative = a < 0 < b or a > 0 > b
    if negative:
        result -= abs(b)
    if a < 0:
        result = -result
    return result


def power(a: float, b: float) -> float:
    """Возведение в целую степень"""
    if not b.is_integer():
        raise InvalidInputError("Возведение в степень возможно только для целых показателей степени")
    elif a == 0 and b < 0:
        raise InvalidInputError("Возведение в степень возможно только для ненулевого основания")
    elif b == 0:
        return 1
    elif a == 0:
        return 0

    if b < 0:
        a, b = div(1.0, a), abs(b)
    powers = dict()
    product, count = a, 1
    while count <= b:
        powers[count] = product
        product = mul(product, product)
        count += count

    result, rest = 1, b
    for i in reversed(powers.keys()):
        if rest >= i:
            rest -= i
            result = mul(result, powers[i])

    if a < 0:
        return -result
    else:
        return result


def sqrt(a: float) -> float:
    """Извлечение квадратного корня"""
    if a < 0:
        raise InvalidInputError("Извлечение квадратного корня возможно только для неотрицательных чисел")
    x, y = a, 1.0
    precision = INT_PRECISION if a.is_integer() else FLOAT_PRECISION
    while x - y > precision:
        x = div((x + y), 2.0)
        y = div(a, x)
    return x


def solve(*equation: str) -> tuple[str, float]:
    """Решение простого уравнения с одним неизвестным"""
    a, oper, b, eq, c = equation
    a_not_float, b_not_float = False, False
    try:
        a = float(a)
    except ValueError:
        a_not_float = True
    try:
        b = float(b)
    except ValueError:
        b_not_float = True
    if not (a_not_float ^ b_not_float):
        raise InvalidInputError(f"{a} и {b} должны быть переменной и числом")
    try:
        c = float(c)
    except ValueError:
        raise InvalidInputError(f"{c} должно быть числом")

    if b_not_float and oper in ["+", "*"]:
        a, b = b, a
        a_not_float, b_not_float = True, False

    if a_not_float:
        if oper == '/' and b == 0:
            raise InvalidInputError("Деление на ноль")
        inverse_func = {"+": sub, "-": add, "*": div, "/": mul}.get(oper)
        if inverse_func:
            return a, inverse_func(c, b)
        else:
            raise InvalidInputError(f"{oper} должно быть оператором")
    if b_not_float:
        inverse_func = {"-": sub, "/": div}.get(oper)
        if inverse_func:
            return b, inverse_func(a, c)
        else:
            raise InvalidInputError(f"{oper} должно быть оператором")
