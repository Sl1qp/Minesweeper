import os
from typing import Tuple
from json import load, dump
from dataclasses import dataclass


@dataclass
class ConfigJson:
    language: str = "language"
    style: str = "style"

    default_language: str = "English"
    default_style: Tuple[bool, int] = 1


@dataclass
class LanguageJson:
    actual_language: str = "actual_language"

    new_game: str = "new_game"
    settings: str = "settings"
    exit: str = "exit"
    language: str = "language"
    style: str = "style"
    edit_language: str = "edit_language"
    edit_style: str = "edit_style"
    back_to_menu: str = "back_to_menu"

    request_language: str = "request_language"
    request_style: str = "request_style"
    set_number: str = "set_number"
    not_checked_name: str = "not_checked_name"
    empty_name: str = "empty_name"
    flag_name: str = "flag_name"
    wrong_flag_name: str = "wrong_flag_name"
    mine_name: str = "mine_name"
    explosion_name: str = "explosion_name"
    request_field_size: str = "request_field_size"
    request_mine_count: str = "request_mine_count"
    request_position: str = "request_position"
    request_restart_game: str = "request_restart_game"

    invalid_input: str = "invalid_input"
    invalid_input_from_file: str = "invalid_input_from_file"
    invalid_input_field_size: str = "invalid_input_field_size"
    invalid_input_mine_count: str = "invalid_input_mine_count"
    invalid_position: str = "invalid_position"
    invalid_operation: str = "invalid_operation"
    repeat: str = "repeat"

    title_not_checked_cells: str = "title_not_checked_cells"
    title_mines: str = "title_mines"
    title_flags: str = "title_flags"

    yes: str = "yes"
    no: str = "no"

    positive_end: str = "positive_end"
    negative_end: str = "negative_end"


@dataclass
class StyleJson:
    not_checked: str = "not_checked"
    empty: str = "empty"
    flag: str = "flag"
    wrong_flag: str = "wrong_flag"
    mine: str = "mine"
    explosion: str = "explosion"


class files:
    folder_path: str = rf"{os.getenv('APPDATA')}\Minesweeper"

    config_file_name: str = "config.json"
    symbols_file_name: str = "symbols.json"

    config_file_path: str = rf"{folder_path}\{config_file_name}"
    symbols_file_path: str = rf"{folder_path}\{symbols_file_name}"

    @staticmethod
    def path_validation(file_name) -> None:
        if not os.path.exists(files.folder_path):
            os.mkdir(files.folder_path)
        file_path = rf"{files.folder_path}\{file_name}"
        if not os.path.exists(file_path):
            from backup_json_files import Backup
            Backup.upload_config(file_name)

    @staticmethod
    def get_config():
        files.path_validation(files.config_file_name)
        with open(files.config_file_path, "r", encoding="utf-8") as file:
            inp = load(file)

            if ConfigJson.language in inp and type(inp[ConfigJson.language]
                                                   ) == str:
                language = inp[ConfigJson.language]
            else:
                language = ConfigJson.default_language

            if ConfigJson.style in inp and type(inp[ConfigJson.style]) == int:
                style = inp[ConfigJson.style]
            else:
                style = ConfigJson.default_style

        return {ConfigJson.language: language, ConfigJson.style: style}

    @staticmethod
    def save_config(language: str, style: int) -> None:
        files.path_validation(files.config_file_name)
        with open(files.config_file_path, "w") as f:
            dump({ConfigJson.language: language, ConfigJson.style: style}, f)

    @staticmethod
    def get_symbols():
        files.path_validation(files.symbols_file_name)
        with open(files.symbols_file_path, "r", encoding="utf-8") as file:
            inp = load(file)
            for idx, symbols_dict in inp.items():
                if StyleJson.not_checked not in symbols_dict or type(symbols_dict[StyleJson.not_checked]) != str:
                    raise Exception(f"Error when unpacking '{idx} -> not_checked' in symbols.json")
                if StyleJson.empty not in symbols_dict or type(symbols_dict[StyleJson.empty]) != str:
                    raise Exception(f"Error when unpacking '{idx} -> empty' in symbols.json")
                if StyleJson.flag not in symbols_dict or type(symbols_dict[StyleJson.flag]) != str:
                    raise Exception(f"Error when unpacking '{idx} -> flag' in symbols.json")
                if StyleJson.wrong_flag not in symbols_dict or type(symbols_dict[StyleJson.wrong_flag]) != str:
                    raise Exception(f"Error when unpacking '{idx} -> wrong_flag' in symbols.json")
                if StyleJson.mine not in symbols_dict or type(symbols_dict[StyleJson.mine]) != str:
                    raise Exception(f"Error when unpacking '{idx} -> mine' in symbols.json")
                if StyleJson.explosion not in symbols_dict or type(symbols_dict[StyleJson.explosion]) != str:
                    raise Exception(f"Error when unpacking '{idx} -> explosion' in symbols.json")
        return inp

    @staticmethod
    def get_language(lang_name: str):
        file_name = f"{lang_name}.json"
        files.path_validation(file_name)
        with open(rf"{files.folder_path}\{file_name}", "r", encoding="utf-8") as file:
            inp = load(file)
            if LanguageJson.actual_language not in inp or type(inp[LanguageJson.actual_language]) != str:
                raise Exception(f"Error when unpacking 'actual_language' in {file_name}")
            if LanguageJson.new_game not in inp or type(inp[LanguageJson.new_game]) != str:
                raise Exception(f"Error when unpacking 'new_game' in {file_name}")
            if LanguageJson.settings not in inp or type(inp[LanguageJson.settings]) != str:
                raise Exception(f"Error when unpacking 'settings' in {file_name}")
            if LanguageJson.exit not in inp or type(inp[LanguageJson.exit]) != str:
                raise Exception(f"Error when unpacking 'exit' in {file_name}")
            if LanguageJson.language not in inp or type(inp[LanguageJson.language]) != str:
                raise Exception(f"Error when unpacking 'language' in {file_name}")
            if LanguageJson.style not in inp or type(inp[LanguageJson.style]) != str:
                raise Exception(f"Error when unpacking 'style' in {file_name}")
            if LanguageJson.edit_language not in inp or type(inp[LanguageJson.edit_language]) != str:
                raise Exception(f"Error when unpacking 'edit_language' in {file_name}")
            if LanguageJson.edit_style not in inp or type(inp[LanguageJson.edit_style]) != str:
                raise Exception(f"Error when unpacking 'edit_style' in {file_name}")
            if LanguageJson.back_to_menu not in inp or type(inp[LanguageJson.back_to_menu]) != str:
                raise Exception(f"Error when unpacking 'back_to_menu' in {file_name}")
            if LanguageJson.request_language not in inp or type(inp[LanguageJson.request_language]) != str:
                raise Exception(f"Error when unpacking 'request_language' in {file_name}")
            if LanguageJson.request_style not in inp or type(inp[LanguageJson.request_style]) != str:
                raise Exception(f"Error when unpacking 'request_style' in {file_name}")
            if LanguageJson.set_number not in inp or type(inp[LanguageJson.set_number]) != str:
                raise Exception(f"Error when unpacking 'set_number' in {file_name}")
            if LanguageJson.not_checked_name not in inp or type(inp[LanguageJson.not_checked_name]) != str:
                raise Exception(f"Error when unpacking 'not_checked_name' in {file_name}")
            if LanguageJson.empty_name not in inp or type(inp[LanguageJson.empty_name]) != str:
                raise Exception(f"Error when unpacking 'empty_name' in {file_name}")
            if LanguageJson.flag_name not in inp or type(inp[LanguageJson.flag_name]) != str:
                raise Exception(f"Error when unpacking 'flag_name' in {file_name}")
            if LanguageJson.wrong_flag_name not in inp or type(inp[LanguageJson.wrong_flag_name]) != str:
                raise Exception(f"Error when unpacking 'wrong_flag_name' in {file_name}")
            if LanguageJson.mine_name not in inp or type(inp[LanguageJson.mine_name]) != str:
                raise Exception(f"Error when unpacking 'mine_name' in {file_name}")
            if LanguageJson.explosion_name not in inp or type(inp[LanguageJson.explosion_name]) != str:
                raise Exception(f"Error when unpacking 'explosion_name' in {file_name}")
            if LanguageJson.request_field_size not in inp or type(inp[LanguageJson.request_field_size]) != str:
                raise Exception(f"Error when unpacking 'request_field_size' in {file_name}")
            if LanguageJson.request_mine_count not in inp or type(inp[LanguageJson.request_mine_count]) != str:
                raise Exception(f"Error when unpacking 'request_mine_count' in {file_name}")
            if LanguageJson.request_position not in inp or type(inp[LanguageJson.request_position]) != str:
                raise Exception(f"Error when unpacking 'request_position' in {file_name}")
            if LanguageJson.request_restart_game not in inp or type(inp[LanguageJson.request_restart_game]) != str:
                raise Exception(f"Error when unpacking 'request_restart_game' in {file_name}")
            if LanguageJson.invalid_input not in inp or type(inp[LanguageJson.invalid_input]) != str:
                raise Exception(f"Error when unpacking 'invalid_input' in {file_name}")
            if LanguageJson.invalid_input_from_file not in inp or type(
                    inp[LanguageJson.invalid_input_from_file]) != str:
                raise Exception(f"Error when unpacking 'invalid_input_from_file' in {file_name}")
            if LanguageJson.invalid_input_field_size not in inp or type(
                    inp[LanguageJson.invalid_input_field_size]) != str:
                raise Exception(f"Error when unpacking 'invalid_input_field_size' in {file_name}")
            if LanguageJson.invalid_input_mine_count not in inp or type(
                    inp[LanguageJson.invalid_input_mine_count]) != str:
                raise Exception(f"Error when unpacking 'invalid_input_mine_count' in {file_name}")
            if LanguageJson.invalid_position not in inp or type(inp[LanguageJson.invalid_position]) != str:
                raise Exception(f"Error when unpacking 'invalid_position' in {file_name}")
            if LanguageJson.invalid_operation not in inp or type(inp[LanguageJson.invalid_operation]) != str:
                raise Exception(f"Error when unpacking 'invalid_operation' in {file_name}")
            if LanguageJson.repeat not in inp or type(inp[LanguageJson.repeat]) != str:
                raise Exception(f"Error when unpacking 'repeat' in {file_name}")
            if LanguageJson.title_not_checked_cells not in inp or type(
                    inp[LanguageJson.title_not_checked_cells]) != str:
                raise Exception(f"Error when unpacking 'title_not_checked_cells' in {file_name}")
            if LanguageJson.title_mines not in inp or type(inp[LanguageJson.title_mines]) != str:
                raise Exception(f"Error when unpacking 'title_mines' in {file_name}")
            if LanguageJson.title_flags not in inp or type(inp[LanguageJson.title_flags]) != str:
                raise Exception(f"Error when unpacking 'title_flags' in {file_name}")
            if LanguageJson.yes not in inp or type(inp[LanguageJson.yes]) != str:
                raise Exception(f"Error when unpacking 'yes' in {file_name}")
            if LanguageJson.no not in inp or type(inp[LanguageJson.no]) != str:
                raise Exception(f"Error when unpacking 'no' in {file_name}")
            if LanguageJson.positive_end not in inp or type(inp[LanguageJson.positive_end]) != str:
                raise Exception(f"Error when unpacking 'positive_end' in {file_name}")
            if LanguageJson.negative_end not in inp or type(inp[LanguageJson.negative_end]) != str:
                raise Exception(f"Error when unpacking 'negative_end' in {file_name}")

            return inp


a = ['actual_language', 'new_game', 'settings', 'exit', 'language', 'style', 'edit_language', 'edit_style',
     'back_to_menu', 'request_language', 'request_style', 'set_number', 'not_checked_name', 'empty_name', 'flag_name',
     'wrong_flag_name', 'mine_name', 'explosion_name', 'request_field_size', 'request_mine_count', 'request_position',
     'request_restart_game', 'invalid_input', 'invalid_input_from_file', 'invalid_input_field_size',
     'invalid_input_mine_count', 'invalid_position', 'invalid_operation', 'repeat', 'title_not_checked_cells',
     'title_mines', 'title_flags', 'yes', 'no', 'positive_end', 'negative_end']
