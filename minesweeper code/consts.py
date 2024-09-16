from dataclasses import dataclass
from typing import Tuple, Dict, List
from file_worker import files, LanguageJson

NEIGHBORS_SHIFTS: List[Tuple[int, int]] = [
    (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0)
]

NUMBERS: Dict[int, int] = {1: 1, 2: 2, 3: 3,  4: 4, 5: 5, 6: 6, 7: 7, 8: 8}


@dataclass
class Action:
    action_open: str = "open"
    action_flag: str = "flag"
    action_deflag: str = "deflag"
    action_all_open: str = "all_open"
    action_all_flag: str = "all_flag"

    int_action_check: int = 1
    int_action_flag: int = 2
    int_action_deflag: int = 3
    int_action_all_open: int = 4
    int_action_all_flag: int = 5


@dataclass
class Msg:
    def __init__(self):
        self.languages: Dict[int, str] = {1: "English", 2: "Russian"}

    actual_language: str

    new_game: str
    settings: str
    exit: str
    language: str
    style: str
    edit_language: str
    edit_style: str
    back_to_menu: str

    new_game: str

    request_language: str
    request_style: str
    set_number: str
    not_checked_name: str
    empty_name: str
    flag_name: str
    wrong_flag_name: str
    mine_name: str
    explosion_name: str
    request_field_size: str
    request_mine_count: str
    request_position: str
    request_restart_game: str

    invalid_input: str
    invalid_input_from_file: str
    invalid_input_field_size: str
    invalid_input_mine_count: str
    invalid_position: str
    invalid_operation: str
    repeat: str

    title_not_checked_cells: str
    title_mines: str
    title_flags: str

    yes: str
    no: str

    positive_end: str
    negative_end: str

    def set_language(self) -> None:
        from response import Response
        print(f"{self.request_language}\n" + "\n".join(
            f"{idx}) {name}"for idx, name in self.languages.items()))
        resp = Response.get_user_input(
            self.languages.keys(),
            "Invalid format of input data."
        )
        self.translate_lang(self.languages[resp])

    def translate_lang(self, lang_name: str):
        lang = files.get_language(lang_name)
        self.actual_language = lang[LanguageJson.actual_language]

        self.new_game = lang[LanguageJson.new_game]
        self.settings = lang[LanguageJson.settings]
        self.exit = lang[LanguageJson.exit]
        self.language = lang[LanguageJson.language]
        self.style = lang[LanguageJson.style]
        self.edit_language = lang[LanguageJson.edit_language]
        self.edit_style = lang[LanguageJson.edit_style]
        self.back_to_menu = lang[LanguageJson.back_to_menu]

        self.request_language = lang[LanguageJson.request_language]
        self.request_style = lang[LanguageJson.request_style]
        self.set_number = lang[LanguageJson.set_number]
        self.not_checked_name = lang[LanguageJson.not_checked_name]
        self.empty_name = lang[LanguageJson.empty_name]
        self.flag_name = lang[LanguageJson.flag_name]
        self.wrong_flag_name = lang[LanguageJson.wrong_flag_name]
        self.mine_name = lang[LanguageJson.mine_name]
        self.explosion_name = lang[LanguageJson.explosion_name]
        self.request_field_size = lang[LanguageJson.request_field_size]
        self.request_mine_count = lang[LanguageJson.request_mine_count]
        self.request_position = lang[LanguageJson.request_position]
        self.request_restart_game = lang[LanguageJson.request_restart_game]

        self.invalid_input = lang[LanguageJson.invalid_input]
        self.invalid_input_from_file = lang[LanguageJson.invalid_input_from_file]
        self.invalid_input_field_size = lang[LanguageJson.invalid_input_field_size]
        self.invalid_input_mine_count = lang[LanguageJson.invalid_input_mine_count]
        self.invalid_position = lang[LanguageJson.invalid_position]
        self.invalid_operation = lang[LanguageJson.invalid_operation]
        self.repeat = lang[LanguageJson.repeat]

        self.title_not_checked_cells = lang[LanguageJson.title_not_checked_cells]
        self.title_mines = lang[LanguageJson.title_mines]
        self.title_flags = lang[LanguageJson.title_flags]

        self.yes = lang[LanguageJson.yes]
        self.no = lang[LanguageJson.no]

        self.positive_end = lang[LanguageJson.positive_end]
        self.negative_end = lang[LanguageJson.negative_end]


@dataclass
class FieldsValues:
    not_checked: int = -1
    empty: int = 0
    flag: int = -2
    wrong_flag: int = -3
    mine: int = -4
    explosion: int = -5

    symbols = {}

    @staticmethod
    def set_symbols():
        from file_worker import files, StyleJson
        inp_symbols = files.get_symbols()
        for key, item in inp_symbols.items():
            tmp_dict = {FieldsValues.not_checked: item[StyleJson.not_checked],
                        FieldsValues.empty: item[StyleJson.empty],
                        FieldsValues.flag: item[StyleJson.flag],
                        FieldsValues.wrong_flag: item[StyleJson.wrong_flag],
                        FieldsValues.mine: item[StyleJson.mine],
                        FieldsValues.explosion: item[StyleJson.explosion]
                        }
            FieldsValues.symbols[int(key)] = tmp_dict

    @staticmethod
    def get_idx_for_config(inp_symbols: Dict[int, str]) -> int:
        for idx, item in FieldsValues.symbols.items():
            if inp_symbols == item:
                return idx


@dataclass
class ResponseMsgNums:
    lose: int = 0
    win: int = 1
    repeat: int = 2
