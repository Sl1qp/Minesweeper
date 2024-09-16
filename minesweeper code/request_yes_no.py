from dataclasses import dataclass
from consts import Msg


@dataclass
class RequestYesNo:
    yes: int = 1
    no: int = 2

    @staticmethod
    def get_request(message: str, msg: Msg) -> int:
        while True:
            try:
                request = f"{message}\n1) {msg.yes}\n2) {msg.no}\n"
                response = int(input(request).split()[0])
            except:
                print(msg.invalid_input)
                continue
            if RequestYesNo.yes <= response <= RequestYesNo.no:
                return response
            else:
                print(msg.invalid_input)

