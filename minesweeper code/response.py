from consts import Msg, ResponseMsgNums
from typing import Optional, List


class Response:
    def __init__(self, is_continues: bool, message_mun: Optional[int] = None):
        self.is_continues = is_continues
        self.message_num = message_mun

    def get_message(self, language: Msg) -> str:
        if self.message_num == ResponseMsgNums.lose:
            return language.negative_end
        elif self.message_num == ResponseMsgNums.win:
            return language.positive_end
        elif self.message_num == ResponseMsgNums.repeat:
            return language.repeat
        else:
            raise Exception("Unknown message number.")

    @staticmethod
    def get_user_input(variants: List[int], incorrect_input_msg: str) -> int:
        while True:
            try:
                response = int(input().split()[0])
            except:
                print(incorrect_input_msg)
                continue
            if response in variants:
                return response
            print(incorrect_input_msg)
