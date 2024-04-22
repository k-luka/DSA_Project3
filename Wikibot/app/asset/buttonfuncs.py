import logging
import pygame as pg
from abc import ABC, abstractmethod


# A place to store specific button functions
class ButtonFuncs(ABC):
    stage: ...

    def switch_to_secondary_texture(self, *args):
        # Switch to the second stored texture, usually a highlight texture
        if hasattr(self, 'switch_to_texture'):
            self.switch_to_texture(1)

    def switch_to_default_texture(self, *args):
        # Switch back to the primary texture, usually from highlighted -> un-highlighted texture
        if hasattr(self, 'switch_to_texture'):
            self.switch_to_texture(0)

    def switch_to_tertiary_texture(self, *args):
        # Switch to the second stored texture, usually a highlight texture
        if hasattr(self, 'switch_to_texture'):
            self.switch_to_texture(2)

    def switch_texture(self, *args):
        # Switch back to the primary texture, usually from highlighted -> un-highlighted texture
        if hasattr(self, 'switch_to_texture') and hasattr(self, 'texture_name') and hasattr(self, 'textures'):
            if self.texture_name == self.textures[0]:
                self.switch_to_texture(1)
            elif self.texture_name == self.textures[1]:
                self.switch_to_texture(0)

    def exit(self, *args):
        # Exit the program
        if hasattr(self, 'app'):
            self.app.quit()

    def go(self, *args):
        if hasattr(self, 'switch_to_texture') and hasattr(self, 'app'):
            self.switch_to_texture(1)
            self.app.generate_api()

    def reset(self, *args):
        if hasattr(self, 'switch_to_texture') and hasattr(self, 'app'):
            self.switch_to_texture(1)
            self.app.reset()

    def select_source_text_box(self, *args):
        if hasattr(self, 'app') and hasattr(self, 'switch_to_texture'):
            self.app.select_source_text_box()
            self.switch_to_texture(1)

    def select_target_text_box(self, *args):
        if hasattr(self, 'app') and hasattr(self, 'switch_to_texture'):
            self.app.select_target_text_box()
            self.switch_to_texture(1)

    def deselect_source_text_box(self, *args):
        if hasattr(self, 'app') and hasattr(self, 'switch_to_texture'):
            self.app.deselect_source_text_box()
            self.switch_to_texture(0)

    def deselect_target_text_box(self, *args):
        if hasattr(self, 'app') and hasattr(self, 'switch_to_texture'):
            self.app.deselect_target_text_box()
            self.switch_to_texture(0)

    def select_number_box(self, *args):
        if hasattr(self, 'app') and hasattr(self, 'switch_to_texture'):
            self.app.select_number_box()
            self.switch_to_texture(1)

    def deselect_number_box(self, *args):
        if hasattr(self, 'app') and hasattr(self, 'switch_to_texture'):
            self.app.deselect_number_box()
            self.switch_to_texture(0)

    def switch_search_mode(self, *args):
        self.switch_texture()
        if hasattr(self, 'app'):
            self.app.switch_search_mode()

    def switch_uniqueness_mode(self, *args):
        self.switch_texture()
        if hasattr(self, 'app'):
            self.app.switch_uniqueness_mode()

