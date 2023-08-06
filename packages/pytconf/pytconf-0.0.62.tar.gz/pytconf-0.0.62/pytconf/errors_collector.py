from typing import List


class ErrorsCollector:
    def __init__(self):
        self.errors: List[str] = []
        self.flag_errors = False

    def add_error(self, msg: str) -> None:
        self.errors.append(msg)

    def raise_error(self):
        self.flag_errors = True

    def have_errors(self) -> bool:
        return len(self.errors) > 0 or self.flag_errors
