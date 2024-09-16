from dataclasses import dataclass
from json import dump
import os


@dataclass
class Backup:
    __config = {"language": "English", "style": 3}
    __eng_lang = {
        "actual_language": "English",
        "new_game": "New game",
        "settings": "Settings",
        "exit": "Exit",
        "language": "Language",
        "style": "Style",
        "edit_language": "Edit language",
        "edit_style": "Edit style",
        "back_to_menu": "Back to menu",

        "request_language": "Select language:",
        "request_style": "Select style:",
        "set_number": "Kit number",
        "not_checked_name": "Not checked",
        "empty_name": "Empty",
        "flag_name": "Flag",
        "wrong_flag_name": "Wrong flag",
        "mine_name": "Mine",
        "explosion_name": "Explosive",
        "request_field_size": "Enter field size (height width): ",
        "request_mine_count": "Enter count of mines: ",
        "request_position": "Make your move in the format: \n\t* Row Column Action(open, flag, deflag) \n\t* Global action: all_open, all_flag\n",
        "request_restart_game": "Play again?",

        "invalid_input": "Invalid format of input data.",
        "invalid_input_from_file": "Invalid format of file input data.",
        "invalid_input_field_size": "Invalid input field size format.",
        "invalid_input_mine_count": "Invalid format of input mine count.",
        "invalid_position": "Selected cell is not on the field.",
        "invalid_operation": "Wrong action.",
        "repeat": "Repeat the turn.",

        "title_not_checked_cells": "Not checked cells without mines",
        "title_mines": "Mines",
        "title_flags": "Flags",

        "yes": "Yes",
        "no": "No",

        "positive_end": "Victory!",
        "negative_end": "You died."
    }
    __rus_lang = {
        "actual_language": "Russian",
        "new_game": "Новая игра",
        "settings": "Настройки",
        "exit": "Выход",
        "language": "Язык",
        "style": "Стиль",
        "edit_language": "Изменить язык",
        "edit_style": "Изменить стиль",
        "back_to_menu": "Вернуться в меню",

        "request_language": "Выберите язык:",
        "request_style": "Выберите оформление:",
        "set_number": "Номер набора",
        "not_checked_name": "Не открыта",
        "empty_name": "Пустая",
        "flag_name": "Флаг",
        "wrong_flag_name": "Ошибочный флаг",
        "mine_name": "Мина",
        "explosion_name": "Взорвавшаяся мина",
        "request_field_size": "Введите размер игрового поля (высота ширина): ",
        "request_mine_count": "Введите количество мин: ",
        "request_position": "Делайте свой ход в формате:\n\t* Строка Столбец Действие(open, flag, deflag)\n\t* Глобальное действие: all_open, all_flag\n",
        "request_restart_game": "Сыграем снова?",

        "invalid_input": "Неверный ввод данных.",
        "invalid_input_from_file": "Неверный ввод данных из файла.",
        "invalid_input_field_size": "Недопустимый размер поля.",
        "invalid_input_mine_count": "Недопустимое количество мин.",
        "invalid_position": "Введённая позиция находится вне игрового поля.",
        "invalid_operation": "Неизвестное действие.",
        "repeat": "Повторите ход.",

        "title_not_checked_cells": "Неоткрытых клеток без мин",
        "title_mines": "Мин",
        "title_flags": "Флагов",

        "yes": "Да",
        "no": "Нет",

        "positive_end": "Поздравляю! Вы победили.",
        "negative_end": "К сожалению, Вы проиграли."
    }

    __symbol = {
        "1": {
            "not_checked": " ",
            "empty": "0",
            "flag": "►",
            "wrong_flag": "✗",
            "mine": "*",
            "explosion": "♰"
        },
        "2": {
            "not_checked": " ",
            "empty": "0",
            "flag": "✓",
            "wrong_flag": "✗",
            "mine": "*",
            "explosion": "⊛"
        },
        "3": {
            "not_checked": " ",
            "empty": "0",
            "flag": "P",
            "wrong_flag": "X",
            "mine": "*",
            "explosion": "#"
        }
    }
    __folder_path: str = rf"{os.getenv('APPDATA')}\Minesweeper"

    @staticmethod
    def upload_config(file_name: str):
        if file_name == "config.json":
            with open(rf"{Backup.__folder_path}\config.json", "w", encoding="utf-8") as file:
                dump(Backup.__config, file)
        if file_name == "English.json":
            with open(rf"{Backup.__folder_path}\English.json", "w", encoding="utf-8") as file:
                dump(Backup.__eng_lang, file)
        if file_name == "Russian.json":
            with open(rf"{Backup.__folder_path}\Russian.json", "w", encoding="utf-8") as file:
                dump(Backup.__rus_lang, file)
        if file_name == "symbols.json":
            with open(rf"{Backup.__folder_path}\symbols.json", "w", encoding="utf-8") as file:
                dump(Backup.__symbol, file)
