from typing import Union

from operations import add, sub, mul, div, mod, power, sqrt, solve


# TODO Необходимо сохранять историю (ввод/вывод)
# TODO Копирование в буфер обмена по клавишам ctrl+c результата вычислений


def main(task: list) -> Union[float, str]:
    if len(task) == 1:
        try:
            return float(task[0])
        except ValueError:
            return "Невозможно вычислить, проверьте ввод данных"

    try:
        a, oper, b, *c = task
    except ValueError:
        return "Невозможно вычислить, проверьте ввод данных"

    if "=" in c:
        return solve(task)
    elif c:
        return "Невозможно вычислить, проверьте ввод данных"

    if b == "1/2":
        return sqrt(a)

    try:
        a = float(a)
    except ValueError:
        return f"{a} должно быть числом"
    try:
        b = float(b)
    except ValueError:
        return f"{b} должно быть числом"

    func = {"+": add, "-": sub, "*": mul, "/": div, "%": mod, "^": power}.get(oper)
    if func:
        return func(a, b)
    else:
        return f"{oper} должно быть оператором"


if __name__ == "__main__":
    while True:
        print("Введите пример:")
        input_data = input().strip()
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
                  "Чтобы получить эту справку, введите 'help' или просто нажмите ввод.")
        else:
            print(main(input_data.split(" ")))
