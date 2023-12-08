from ..db import read_db


class PiballGame:
    def __init__(self):
        self.__elements = read_db()
