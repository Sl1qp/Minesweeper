from typing import Tuple, List
from random import sample
from response import Response
from consts import (
    NEIGHBORS_SHIFTS,
    FieldsValues,
    Action,
    ResponseMsgNums,
)


# TODO: сделать раздел настроек( при старте игры пишутся ваши настройки:
#       язык - стиль - таб)
#  + добавить возможность редактирования настроек
#       (их можно хранить в ещё одном json файле)


class Game:
    def __init__(self, width: int, height: int, mine_count: int) -> None:
        self.field_width: int = width
        self.field_height: int = height
        self.front_field: List[List[int]] = [
            [FieldsValues.not_checked] * width for _ in range(height)
        ]
        self.__back_field: List[List[int]] = [
            [FieldsValues.empty] * width for _ in range(height)
        ]
        self.mine_count: int = mine_count
        self.flag_count: int = 0
        self.not_checked_count: int = width * height - self.mine_count
        self.__detected_mine_count: int = 0
        self.__is_first_turn: bool = True
    '''
    def __generate_field(self, row_idx: int, column_idx: int) -> None:
        from random import randint
        for _ in range(self.mine_count):
            while True:
                row = randint(0, self.field_height - 1)
                column = randint(0, self.field_width - 1)
                if (row != row_idx or column != column_idx) and (
                        self.__back_field[row][column] != FieldsValues.mine):
                    self.__back_field[row][column] = FieldsValues.mine
                    for shift in NEIGHBORS_SHIFTS:
                        row_ind = row + shift[0]
                        column_ind = column + shift[1]
                        if self.is_cell_in_field(row_ind, column_ind) and (
                                self.__back_field[row_ind][column_ind] != (
                                FieldsValues.mine)):
                            self.__back_field[row_ind][column_ind] += 1
                    break
    '''
    def __generate_field(self, row_idx: int, column_idx: int) -> None:
        crit_num = self.field_width * row_idx + column_idx
        cell_nums = sample(range(self.field_width * self.field_height),
                           k=self.mine_count + 1)
        for cell_num in cell_nums[:-1]:
            if cell_num == crit_num:
                cell_num = cell_nums[-1]
            row = cell_num // self.field_width
            column = cell_num - row * self.field_width
            self.__back_field[row][column] = FieldsValues.mine
            for shift in NEIGHBORS_SHIFTS:
                row_ind = row + shift[0]
                column_ind = column + shift[1]
                if self.is_cell_in_field(row_ind, column_ind) and (
                   self.__back_field[row_ind][column_ind] != FieldsValues.mine):
                    self.__back_field[row_ind][column_ind] += 1

    def is_cell_in_field(self, row_idx, column_idx) -> bool:
        return 0 <= row_idx < self.field_height and (
               0 <= column_idx < self.field_width)

    def make_turn(self, row_idx: int, column_idx: int, operation: int
                  ) -> Response:
        if self.__is_first_turn:
            self.__is_first_turn = False
            self.__generate_field(row_idx, column_idx)

        if operation == Action.int_action_all_open:
            for row_ind in range(self.field_height):
                for col_ind in range(self.field_width):
                    if self.front_field[row_ind][col_ind] == (
                       FieldsValues.not_checked):
                        back_value = self.__back_field[row_ind][col_ind]
                        if back_value == FieldsValues.mine:
                            self.__open_field(row_ind, col_ind)
                            self.not_checked_count = 0
                            return Response(False, ResponseMsgNums.lose)
                        else:
                            self.front_field[row_ind][col_ind] = back_value
                            self.not_checked_count -= 1
            if self.__check_game_positive_end():
                return Response(False, ResponseMsgNums.win)

        elif operation == Action.int_action_all_flag:
            for row_ind in range(self.field_height):
                for col_ind in range(self.field_width):
                    if self.front_field[row_ind][col_ind] == (
                       FieldsValues.not_checked):
                        self.front_field[row_ind][col_ind] = FieldsValues.flag
                        self.flag_count += 1
                        if self.__back_field[row_ind][col_ind] == (
                           FieldsValues.mine):
                            self.__detected_mine_count += 1
            if self.__check_game_positive_end():
                return Response(False, ResponseMsgNums.win)

        elif operation == Action.int_action_flag:
            self.front_field[row_idx][column_idx] = FieldsValues.flag
            self.flag_count += 1
            if self.__back_field[row_idx][column_idx] == FieldsValues.mine:
                self.__detected_mine_count += 1
            if self.__check_game_positive_end():
                return Response(False, ResponseMsgNums.win)

        elif operation == Action.int_action_deflag:
            self.front_field[row_idx][column_idx] = FieldsValues.not_checked
            self.flag_count -= 1
            if self.__back_field[row_idx][column_idx] == FieldsValues.mine:
                self.__detected_mine_count -= 1

        elif operation == Action.int_action_check:
            if self.__back_field[row_idx][column_idx] == FieldsValues.mine:
                self.__open_field(row_idx, column_idx)
                return Response(False, ResponseMsgNums.lose)
            self.front_field[row_idx][column_idx] = self.__back_field[row_idx][
                column_idx]
            if self.__back_field[row_idx][column_idx] == FieldsValues.empty:
                self.__open_neighbors(row_idx, column_idx)
            self.not_checked_count -= 1
            if self.__check_game_positive_end():
                return Response(False, ResponseMsgNums.win)

        else:
            print("Unknown operation on the back-end.")
            raise Exception()

        return Response(True)

    def __check_game_positive_end(self) -> bool:
        return self.mine_count == self.__detected_mine_count and (
            not self.not_checked_count)
    """
    def __open_neighbors(self, row_idx: int, column_idx: int) -> None:
        # Old version
        for shift in NEIGHBORS_SHIFTS:
            row_ind = row_idx + shift[0]
            column_ind = column_idx + shift[1]
            if self.is_cell_in_field(row_ind, column_ind) and (
               self.front_field[row_ind][column_ind] ==
               FieldsValues.not_checked):
                new_value = self.__back_field[row_ind][column_ind]
                self.front_field[row_ind][column_ind] = new_value
                self.not_checked_count -= 1
                if new_value == FieldsValues.empty:
                    # Т.к. вызываемся только от empty, то ничего, кроме цифр или
                    # empty не откроется
                    self.__open_neighbors(row_ind, column_ind)
    """
    def __open_field(self, row_idx: int, column_idx: int) -> None:
        for row in range(self.field_height):
            for col in range(self.field_width):
                if self.front_field[row][col] == FieldsValues.flag:
                    if self.__back_field[row][col] != FieldsValues.mine:
                        self.front_field[row][col] = FieldsValues.wrong_flag
                else:
                    self.front_field[row][col] = self.__back_field[row][col]
        self.front_field[row_idx][column_idx] = FieldsValues.explosion

    def __open_neighbors(self, row_idx: int, column_idx: int) -> None:
        open_queue: List[Tuple[int, int]] = [(row_idx, column_idx)]
        while open_queue:
            row_idx, column_idx = open_queue.pop(0)
            for shift in NEIGHBORS_SHIFTS:
                shifted_row = row_idx + shift[0]
                shifted_column = column_idx + shift[1]
                if self.is_cell_in_field(shifted_row, shifted_column) and (
                        self.front_field[shifted_row][shifted_column] ==
                        FieldsValues.not_checked):
                    new_value = self.__back_field[shifted_row][shifted_column]
                    self.front_field[shifted_row][shifted_column] = new_value
                    self.not_checked_count -= 1
                    if new_value == FieldsValues.empty:
                        open_queue.append((shifted_row, shifted_column))
