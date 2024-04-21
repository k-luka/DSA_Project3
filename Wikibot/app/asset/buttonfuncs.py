import logging
import pygame as pg
from abc import ABC, abstractmethod


# A place to store specific button functions
class ButtonFuncs(ABC):
    stage: ...

    @abstractmethod
    def switch_to_texture(self, value: int) -> None: pass

    def switch_to_secondary_texture(self, *args):
        # Switch to the second stored texture, usually a highlight texture
        self.switch_to_texture(1)

    def switch_to_default_texture(self, *args):
        # Switch back to the primary texture, usually from highlighted -> un-highlighted texture
        self.switch_to_texture(0)

    def exit(self, *args):
        # Exit the program
        if hasattr(self, 'app'):
            self.app.quit()

