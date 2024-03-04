import logging

import pyperclip

from operations import add, sub, mul, div, mod, power, sqrt, solve, InvalidInputError

LOG_FILE = 'calculator.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    encoding='utf-8',
    filename=LOG_FILE,
)


def main(*task: str) -> str:
    if len(task) == 1:
        try:
            return str(float(task[0]))
        except ValueError:
            raise InvalidInputError

    try:
        a, oper, b, *c = task
    except ValueError:
        raise InvalidInputError

    if len(c) == 2 and c[0] == "=":
        name, result = solve(a, oper, b, *c)
        return f"{name} = {result}"
    elif c:
        raise InvalidInputError

    try:
        a = float(a)
    except ValueError:
        raise InvalidInputError(f"{a} должно быть числом")

    if b == "1/2":
        return str(sqrt(a))

    try:
        b = float(b)
    except ValueError:
        raise InvalidInputError(f"'{b}' должно быть числом")

    func = {"+": add, "-": sub, "*": mul, "/": div, "%": mod, "^": power}.get(oper)
    if func:
        return str(func(a, b))
    else:
        raise InvalidInputError(f"'{oper}' должно быть оператором")


def get_log(s: str) -> None:
    try:
        n = int(s)
    except ValueError:
        raise InvalidInputError("Укажите количество операций для вывода, например, 'h 5'")
    if n == 0:
        raise InvalidInputError("Укажите количество операций для вывода, например, 'h 5'")
    with open(LOG_FILE) as log:
        lines = log.readlines()
    for line in lines[-2*n:]:
        print(line, end='')


if __name__ == "__main__":
    print("Введите пример или простое уравнение, разделяя числа и операторы пробелами.\n"
          "Чтобы получить справку, просто нажмите ввод.")
    result = ''
    while True:
        try:
            input_data = input("Введите пример или команду: ").strip()
        except KeyboardInterrupt as e:
            try:
                pyperclip.copy(result)
                print("Последний результат скопирован в буфер обмена.")
            except pyperclip.PyperclipException:
                print("Для выполнения копирования в буфер обмена на Linux необходимо установить xsel:\n"
                      "'sudo apt-get install xsel'")
            continue
        if input_data == "exit":
            print("Калькулятор завершил работу.")
            break
        elif input_data in ("", "help"):
            print("Введите пример или простое уравнение, разделяя числа и операторы пробелами.\n"
                  "Возможные операции:\n"
                  "    + сложение,\n"
                  "    - вычитание,\n"
                  "    * умножение,\n"
                  "    / деление,\n"
                  "    % остаток от деления,\n"
                  "    ^ возведение в целую степень,\n"
                  "    ^ 1/2 извлечение квадратного корня,\n"
                  "    решение простых уравнений с одним неизвестным, например, 2 + x = 14.\n"
                  "Для завершения работы введите 'exit'.\n"
                  "Чтобы увидеть последние n операций, введите 'h <n>'.\n"
                  "Чтобы получить эту справку, просто нажмите ввод или введите пустую строку.")
        elif input_data.startswith('h'):
            try:
                get_log(input_data[1:])
            except InvalidInputError as e:
                print(e.message)
        else:
            logging.info(f">>> {input_data}")
            try:
                result = main(*input_data.split())
            except InvalidInputError as e:
                result = e.message
            print(result)
            logging.info(result)
