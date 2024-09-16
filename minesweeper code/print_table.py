# ┗ ┫ ┿ ┣ ┷ ┛ ┓ ┃ ┯ ┏ ━ ┻ ┳
from typing import List, Any, Optional, Dict, Tuple


def print_table(
        data: List[List[Any]],
        prev_table_last_row: Optional[List[str]] = None,
        column_lengths: Optional[List[Optional[int]]] = None,
        vertical_lines: Optional[Dict[int, bool]] = None,
        horizontal_lines: Optional[Dict[int, bool]] = None,
        indents: Optional[List[Optional[Tuple[bool, bool, str]]]] = None,
        is_last_table: bool = True,
) -> Optional[List[str]]:
    """
    Оформляет переданные данные в таблицу. Если не все строки таблицы имеют
    одинаковую длину, то они приводятся к длине наибольшей добавлением пустых
    ячеек
    :param data: содержимое ячеек таблицы
    :param prev_table_last_row: (опционально) последняя строка предыдущей
        таблицы, необходимая для корректного соединения таблиц
        (см. аргумент "is_last_table")
    :param column_lengths: (опционально) список, содержащий в себе ширины
        колонок в символах (без учёта отступов, см. аргумент "indents") или
        значение "None", если ширина неизвестна или не требует определённого
        значения. Список необязательно должен охватывать все столбцы
    :param vertical_lines: (опционально) словарь, где: ключ - номер столбца
        (начиная с 1), после которого должна идти вертикальная линия, значение -
        тип линии (True - толстая)
    :param horizontal_lines: (опционально) словарь, где: ключ - номер строки
        (начиная с 1), после которой должна идти горизонтальной линия,
        значение - тип линии (True - толстая)
    :param indents: (опционально) список, содержащий в себе кортеж или значение
        "None", если требуется сохранить стандартное форматирование. Список
        отвечает за расположение данных в столбце. Кортеж состоит из:
        необходимости отступа (в виде пробела) слева, необходимости отступа
        справа, типа выравнивания текста ("^" - по центру, "<" - по левому краю,
        ">" - по правому краю). Стандартное форматирование - (True, True, "^")
    :param is_last_table: последняя ли это таблица, если False, то возвращается
        последняя строка необходимая для аргумента "prev_table_last_row"
    :return: последняя строка таблицы, если аргумент "is_last_table"
        равен False, в противном случае "None"
    """

    if column_lengths is None:
        column_lengths = []
    if vertical_lines is None:
        vertical_lines = dict()
    if horizontal_lines is None:
        horizontal_lines = dict()
    if indents is None:
        indents = []

    for row in range(len(data)):
        for column in range(len(data[row])):
            data[row][column] = str(data[row][column])

    # Проверка матрицы на прямоугольность
    max_len = len(max(data, key=len))
    for row in data:
        len_row = len(row)
        if len_row < max_len:
            row += [""] * (max_len - len_row)

    # Проверка длин колонок
    len_column_lengths = len(column_lengths)
    if len_column_lengths > max_len:
        raise Exception(".")
    elif len_column_lengths < max_len:
        column_lengths += [None] * (max_len - len_column_lengths)

    for key in vertical_lines:
        if key < 1 or key >= max_len:
            raise Exception('Номер столбца в "vertical_lines" '
                            'за пределами допустимых значений')
    for key in horizontal_lines:
        if key < 1 or key >= len(data):
            raise Exception('Номер строки в "horizontal_lines" '
                            'за пределами допустимых значений')

    for column in range(max_len):
        col_len = column_lengths[column]
        if col_len is None:
            max_l = -1
            for row in range(len(data)):
                max_l = max(max_l, len(data[row][column]))
            column_lengths[column] = max_l

    indents = indents[:max_len]
    standart_indent = (True, True, "^")
    for idx in range(len(indents)):
        if not indents[idx]:
            indents[idx] = standart_indent
    if len(indents) < max_len:
        indents += [standart_indent] * (max_len - len(indents))

    horiz_line_bold = "┣"
    line_format = '┃'
    l_brace, r_brace = chr(123), chr(125)

    for item_num, item in enumerate(column_lengths, 1):
        l_indent, r_indent, _formats = indents[item_num - 1]
        horiz_line_bold += (f'{"━" * item}'
                            f'{"━" if l_indent else ""}'
                            f'{"━" if r_indent else ""}')
        if item_num in vertical_lines:
            horiz_line_bold += f'{"╋" if vertical_lines[item_num] else "┿"}'

        line_format += (f'{" " if l_indent else ""}'
                        f'{l_brace}:{_formats}{item}{r_brace}'
                        f'{" " if r_indent else ""}')
        is_bold = vertical_lines.get(item_num)
        if is_bold is not None:
            line_format += f"{'┃' if is_bold else '│'}"
    horizontal_line_slim = f'┠{horiz_line_bold[1:].replace("━", "─").replace("╋", "╂").replace("┿", "┼")}┨'
    horiz_line_bold += "┫"
    line_format += "┃"

    lower_line = f'┗{horiz_line_bold[1:-1].replace("╋", "┻").replace("┿", "┷")}┛'

    if prev_table_last_row:
        prev_table_len = len(prev_table_last_row)
        first_line_len = len(lower_line)
        prev_table_last_row[0] = "┣"

        if first_line_len > prev_table_len:
            prev_table_last_row += f'{lower_line[prev_table_len:-1].replace("┻", "┳").replace("┷", "┯")}┓'
            prev_table_last_row[prev_table_len - 1] = "┻"
        elif first_line_len == prev_table_len:
            prev_table_last_row[-1] = "┫"
        else:
            is_bold = prev_table_last_row[first_line_len - 1]
            if is_bold == "━":
                prev_table_last_row[first_line_len - 1] = "┳"
            else:
                prev_table_last_row[first_line_len - 1] = "╈" if (
                        is_bold == "┷") else "╋"

        for i in range(1, min(first_line_len, prev_table_len) - 1):
            lower_line_i = lower_line[i]
            prev_table_i = prev_table_last_row[i]
            if lower_line_i == "━":
                continue
            if lower_line_i == "┻":
                if prev_table_i == "┻":
                    prev_table_last_row[i] = "╋"
                elif prev_table_i == "┷":
                    prev_table_last_row[i] = "╈"
                else:
                    prev_table_last_row[i] = "┳"
            else:
                if prev_table_i == "┷":
                    prev_table_last_row[i] = "┿"
                elif prev_table_i == "┻":
                    prev_table_last_row[i] = "╇"
                else:
                    prev_table_last_row[i] = "┯"
        first_line = "".join(prev_table_last_row)
    else:
        first_line = f'┏' \
                     f'{horiz_line_bold[1:-1].replace("╋", "┳").replace("┿", "┯")}┓'
    print(first_line)

    for row_num, row in enumerate(data, 1):
        print(line_format.format(*row))
        if row_num in horizontal_lines:
            print(horiz_line_bold if horizontal_lines[row_num]
                  else horizontal_line_slim)

    if is_last_table:
        print(lower_line)
    else:
        return list(lower_line)
