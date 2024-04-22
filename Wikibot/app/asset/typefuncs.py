from abc import ABC, abstractmethod
import pygame as pg
from typing import Optional, Union


class TypeFuncs(ABC):
    text: str
    selected: bool
    dimensionsPx: Optional[Union[tuple[float, float], tuple[int, int]]]

    @abstractmethod
    def update_text(self, new_text: str, *args) -> None: pass

    def backspace(self, *args):
        if self.selected and len(self.text) > 0:
            self.update_text(self.text[:-1])

    def type_alphanum(self, unicode: str, *args):
        if len(unicode) != 1:
            return
        if self.selected and 32 <= ord(unicode) <= 126:
            self.update_text(self.text + unicode)

    def type_numeric(self, unicode: str, *args):
        if len(unicode) != 1:
            return
        if self.selected and 48 <= ord(unicode) <= 57:
            self.update_text(self.text + unicode)

    def type_numeric_one_digit(self, unicode: str, *args):
        if len(unicode) != 1:
            return
        if self.selected and 49 <= ord(unicode) <= 57 and len(self.text) == 0:
            self.update_text(self.text + unicode)



