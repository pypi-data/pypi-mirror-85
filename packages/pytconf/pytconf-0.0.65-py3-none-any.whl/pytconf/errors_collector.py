from typing import List, Tuple, Generator


class ErrorsCollector:
    """
    This collector support two types of error. Regular errors and special errors
    Regular errors are the ones to be printed and carry the error_type = false.
    """
    def __init__(self):
        self._errors: List[Tuple[str, bool]] = []
        self.do_help: bool = False

    def add_error(self, msg: str, error_type: bool = False) -> None:
        self._errors.append((msg, error_type))

    def have_errors(self) -> bool:
        return len(self._errors) > 0

    def set_do_help(self) -> None:
        self.do_help = True

    def get_do_help(self) -> bool:
        return self.do_help

    def yield_errors(self, error_type: bool = False) -> Generator[str, None, None]:
        for error in self._errors:
            if error[1] == error_type:
                yield error[0]
