from back import Game
from typing import Tuple, Dict, List
from request_yes_no import RequestYesNo
from response import Response
from file_worker import files, ConfigJson
from print_table import print_table
from consts import (
    Action,
    FieldsValues,
    NUMBERS,
    Msg,
    ResponseMsgNums,
)


class Visual:
    def __init__(self):
        window_width, window_height = 1, 1
        self.__window_size: Tuple[int, int] = (window_width, window_height)
        self.__game: Game
        self.__msg: Msg = Msg()
        self.__style: Dict[int, str] = {}
        self.__upload_config()

    def __upload_config(self):
        conf = files.get_config()
        self.__msg.translate_lang(conf[ConfigJson.language])
        FieldsValues.set_symbols()
        self.__style = FieldsValues.symbols[conf[ConfigJson.style]]

    def start(self):
        while True:
            variants = {1: self.__msg.new_game,
                        2: self.__msg.settings,
                        3: self.__msg.exit}
            data = [[num, item] for num, item in variants.items()]
            print_table(
                data,
                column_lengths=[1, len(max(variants.values(), key=len))],
                vertical_lines={1: False},
                is_last_table=True
            )
            resp = Response.get_user_input(variants.keys(),
                                           self.__msg.invalid_input)
            if variants[resp] == self.__msg.new_game:
                while True:
                    self.__launch_game()
                    # Запрос на повтор игры
                    if RequestYesNo.get_request(
                            self.__msg.request_restart_game,
                            self.__msg
                    ) == RequestYesNo.no:
                        break
            elif variants[resp] == self.__msg.settings:
                self.__set_settings()
            else:
                break

    def __set_settings(self):
        while True:
            data = [[self.__msg.language, self.__msg.actual_language],
                    [self.__msg.style, " ".join(i for i in self.__style.values())]]

            prev_row = print_table(
                data,
                vertical_lines={1: True},
                column_lengths=[None, 11],
                is_last_table=False
            )
            variants = {1: self.__msg.edit_language,
                        2: self.__msg.edit_style,
                        3: self.__msg.back_to_menu}
            data = [[num, item] for num, item in variants.items()]
            print_table(
                data,
                prev_table_last_row=prev_row,
                vertical_lines={1: True},
                is_last_table=True
            )
            resp = Response.get_user_input(variants.keys(),
                                           self.__msg.invalid_input)
            if variants[resp] == self.__msg.edit_language:
                self.__msg.set_language()
            elif variants[resp] == self.__msg.edit_style:
                self.get_response()
            elif variants[resp] == self.__msg.back_to_menu:
                files.save_config(self.__msg.actual_language,
                                  FieldsValues.get_idx_for_config(
                                        self.__style))
                return

    def __create_header(self) -> List[str]:
        headers = {
            self.__msg.title_not_checked_cells: self.__game.not_checked_count,
            self.__msg.title_mines: self.__game.mine_count,
            self.__msg.title_flags: self.__game.flag_count,
        }
        headers = [f'{header}: {value}' for (header, value) in headers.items()]
        return headers

    def __launch_game(self) -> None:
        while True:
            try:
                field_height, field_width = map(int, input(
                    self.__msg.request_field_size
                ).split()[:2])
                if field_width <= 0 or field_height <= 0:
                    raise Exception()
                break
            except:
                print(self.__msg.invalid_input_field_size)

        while True:
            try:
                mine_count = int(input(
                    f"{self.__msg.request_mine_count}"
                    f"[1, {field_width * field_height - 1}]: "
                ).split()[0])
                if mine_count <= 0 or mine_count >= field_width * field_height:
                    raise Exception()
                break
            except:
                print(self.__msg.invalid_input_mine_count)

        self.__game = Game(field_width, field_height, mine_count)
        # self.__print_autosize_based()

        data, style = [["№"]], self.__style | NUMBERS
        data[0] += [str(i) for i in range(1, self.__game.field_width + 1)]
        for num, row in enumerate(self.__game.front_field, 1):
            data.append([num] + [style[elem] for elem in row])

        prev_row = print_table([self.__create_header()],
                               vertical_lines={1: False, 2: False},
                               is_last_table=False)
        print_table(
            data,
            prev_table_last_row=prev_row,
            column_lengths=[None] + [len(str(self.__game.field_width))] * self.__game.field_width,
            vertical_lines={1: True},
            horizontal_lines={1: True}
        )

        while True:
            response = self.__make_turn()
            if response.message_num != ResponseMsgNums.repeat:
                #self.__print_autosize_based()

                for num, row in enumerate(self.__game.front_field, 1):
                    data[num] = [num] + [style[elem] for elem in row]
                prev_row = print_table(
                    [self.__create_header()],
                    vertical_lines={1: False, 2: False},
                    is_last_table=False
                )
                print_table(
                    data,
                    prev_table_last_row=prev_row,
                    column_lengths=[None] + [len(str(self.__game.field_width))] * self.__game.field_width,
                    vertical_lines={1: True},
                    horizontal_lines={1: True},
                    indents=[(True, True, "^")] + [(True, False, ">")] * self.__game.field_width
                )

            if response.message_num is not None:
                print(response.get_message(self.__msg))
            if not response.is_continues:
                break

    def __make_turn(self) -> Response:
        _input = input(f"\n{self.__msg.request_position}").split()[:3]
        try:
            if _input[0] == Action.action_all_open:
                return self.__game.make_turn(-1, -1, Action.int_action_all_open)
            if _input[0] == Action.action_all_flag:
                return self.__game.make_turn(-1, -1, Action.int_action_all_flag)
            row_idx = int(_input[0])
            column_idx = int(_input[1])
            operation = _input[2]
            if operation == Action.action_open:
                operation = Action.int_action_check
            elif operation == Action.action_flag:
                operation = Action.int_action_flag
            elif operation == Action.action_deflag:
                operation = Action.int_action_deflag
            else:
                raise Exception()
        except:
            print(self.__msg.invalid_input)
            return Response(True, ResponseMsgNums.repeat)
        row_idx -= 1
        column_idx -= 1
        if not self.__game.is_cell_in_field(row_idx, column_idx):
            print(self.__msg.invalid_position)
            return Response(True, ResponseMsgNums.repeat)
        cell_value = self.__game.front_field[row_idx][column_idx]
        if (cell_value == FieldsValues.not_checked and
            operation != Action.int_action_deflag) or (
                cell_value == FieldsValues.flag and
                operation == Action.int_action_deflag):
            return self.__game.make_turn(row_idx, column_idx, operation)
        else:
            print(self.__msg.invalid_operation)
        return Response(True, ResponseMsgNums.repeat)

    @staticmethod
    def __make_rformat(length: int) -> str:
        return '{:>' + str(length) + '}'

    def __print_autosize_based(self) -> None:  # Для маленьких
        headers = self.__create_header()
        title = f"┃ {' │ '.join(item for item in headers)} ┃"
        above_title = f"┏━{'━┯━'.join('━' * len(item) for item in headers)}━┓"
        under_title_lst = list(
                      f"┣━{'━┷━'.join('━' * len(item) for item in headers)}━┛"
                      )

        title_len = len(title)
        row_ind_len = len(str(self.__game.field_height))
        col_ind_len = len(str(self.__game.field_width))
        table_len = 1 + row_ind_len + 1 + self.__game.field_width * (
            col_ind_len + 1) + 2

        # Случай, когда длина title <= столбца номеров строк, не обрабатывается
        under_title_lst[row_ind_len + 1] = (
            "┿" if under_title_lst[row_ind_len + 1] == '┷' else '┯')

        if table_len < title_len:
            under_title_lst[table_len - 1] = (
                "╈" if under_title_lst[table_len - 1] == '┷' else '┳')
            under_title = ''.join(under_title_lst)
        elif table_len == title_len:
            under_title_lst[-1] = '┫'
            under_title = ''.join(under_title_lst)
        else:
            under_title_lst[-1] = '┻'
            under_title_lst.append('━' * (table_len - title_len - 1))
            under_title = f"{''.join(under_title_lst)}┓"

        print(above_title)
        print(title)
        print(under_title)

        row_format = self.__make_rformat(row_ind_len)
        col_format = self.__make_rformat(col_ind_len)
        col_inds = range(1, self.__game.field_width + 1)
        print(f"┃{row_format.format('№')}│ "
              f"{' '.join(col_format.format(ind) for ind in col_inds)} ┃")
        print(f"┠{'─' * row_ind_len}┼{'─' * (table_len - row_ind_len - 3)}┨")
        for i, row in enumerate(self.__game.front_field, 1):
            print(
                f"┃{row_format.format(i)}│",
                ' '.join((self.__style | NUMBERS)[elem] for elem in row) + ' ┃'
            )
        print(f"┗{'━' * row_ind_len}┷{'━' * (table_len - row_ind_len - 3)}┛")

    def get_response(self) -> None:
        symbol_types = [self.__msg.set_number,
                        (FieldsValues.not_checked, self.__msg.not_checked_name),
                        (FieldsValues.empty, self.__msg.empty_name),
                        (FieldsValues.flag, self.__msg.flag_name),
                        (FieldsValues.wrong_flag, self.__msg.wrong_flag_name),
                        (FieldsValues.mine, self.__msg.mine_name),
                        (FieldsValues.explosion, self.__msg.explosion_name),
                        ]
        data = [[symbol_types[0]]]
        data[0] += [i for i in FieldsValues.symbols]
        for code, name in symbol_types[1:]:
            data.append([name] + [FieldsValues.symbols[idx][code]
                                  for idx in FieldsValues.symbols])
        vert_line = {1: True}
        vert_line.update({i: False for i in range(2, len(FieldsValues.symbols) + 1)})
        print_table(data,
                    column_lengths=[None] + [1] * len(FieldsValues.symbols),
                    vertical_lines=vert_line,
                    horizontal_lines={1: True}
                    )
        while True:
            try:
                response = int(input().split()[0])
            except:
                print(self.__msg.invalid_input)
                continue
            if response in FieldsValues.symbols:
                self.__style = FieldsValues.symbols[response]
                return
            else:
                print(self.__msg.invalid_input)
