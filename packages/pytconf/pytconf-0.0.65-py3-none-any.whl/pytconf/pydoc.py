from typing import Union


def get_first_line(doc: Union[str, None]) -> Union[str, None]:
    """
    Get first line for a pydoc string
    :param doc: the pydoc string
    :return: the first line which is not whitespace
    """
    if doc is None:
        return None
    lines = doc.split("\n")
    for line in lines:
        if line == "" or line.isspace():
            continue
        return line.strip()
    return None
