from .statictextbutton import StaticTextButton, StaticTextButtonCreateInfo
from dataclasses import dataclass
from typing import Union, Callable, Optional, Sequence
import logging
import pygame as pg


@dataclass()
class TextSpriteCreateInfo(StaticTextButtonCreateInfo):
    text_func: Optional[str] = None
    char_size: Optional[tuple[int, int]] = None
    auto_textbox_scaling: bool = False
    pass


class TextSprite(StaticTextButton):
    selected: bool = False
    text_func: Optional[Callable[[int, Sequence[bool]], None]] = None
    char_size: Optional[tuple[int, int]] = None
    auto_textbox_scaling: bool = False
    cof: Callable[[int, tuple[bool, bool, bool] | tuple[bool, bool, bool, bool, bool]], None] = None

    def __init__(self, info: Union[type[TextSpriteCreateInfo], TextSpriteCreateInfo]):
        if info.cafs is None:
            info.cafs = dict()
        info.cafs[1] = 'select'
        if info.char_size is not None:
            text_length = len(info.text)
            info.dimensionsPx = (text_length * info.char_size[0], info.char_size[1])
        self.char_size = info.char_size
        StaticTextButton.__init__(self, info)
        self.cof = self.deselect
        self._initialize_text_func(info.text_func)
        self.auto_textbox_scaling = info.auto_textbox_scaling
        if self.auto_textbox_scaling:
            texture_surface: pg.Surface = self.app.get_texture(self.texture_name)
            texture_dimensions = texture_surface.size
            scale: float = self.dimensionsPx[1] / texture_dimensions[1]
            self.dimensionsPx = (texture_dimensions[0] * scale, self.dimensionsPx[1])
        self.update()

    def _initialize_text_func(self, text_func_string):
        if text_func_string is None:
            self.text_func = None
            return
        func = getattr(self, text_func_string, None)
        if func is None:
            logging.warning(f' {self.__class__.__name__} object \'{self.__repr__}\' '
                            f'attempted to set text function to \'{text_func_string}\', but \'{text_func_string}\' does not exist '
                            f'as any text function or {self.__class__.__name__} class or parent class method. '
                            f'Setting to \'None\' instead')
        self.text_func = func

    def add_to_scene(self, scene_layer: int = None) -> None:
        # Add button to scene, overwrites StaticImage implementation to allow for collision boundary listing
        if not self.isViewable:
            logging.info(f"Adding {self.__class__.__name__} instance \'{self.name}\' to scene")
            self.isViewable = True
            self.list_collision_boundaries()
            self.list_hover_functions()
            self.list_click_functions()
            self.list_click_off_function()
            self.list_text_function()
            if not scene_layer:
                self.app.append_model_to_scene(self.model)
            else:
                self.app.insert_model_into_scene(scene_layer, self.model)
        else:
            logging.warning(
                f' failed to add {self.__class__.__name__} object \'{self.name}\' to scene: already viewable in scene')

    def remove_from_scene(self) -> None:
        # Remove button from scene, overwrites StaticImage implementation to allow for collision boundary de-listing
        if self.isViewable:
            logging.info(f"Removing {self.__class__.__name__} instance \'{self.name}\' from scene")
            self.isViewable = False
            self.delist_collision_boundaries()
            self.delist_hover_functions()
            self.delist_click_functions()
            self.delist_click_off_function()
            self.delist_text_function()
            self.app.remove_model_from_scene(self.model)
        else:
            logging.warning(
                f' failed to remove {self.__class__.__name__} object \'{self.name}\' to scene: object not viewable in scene')

    def update_text(self, new_text, *args):
        self.text = new_text
        self.texture_name = f"{self.name}.{self.text}"
        if self.texture_name not in self.textures:
            self.app.add_text_texture(self.texture_name, self.size, self.color, self.text, self.background)
            self.textures.append(self.texture_name)
        if self.auto_textbox_scaling:
            texture_surface: pg.Surface = self.app.get_texture(self.texture_name)
            texture_dimensions = texture_surface.size
            scale: float = self.dimensionsPx[1] / texture_dimensions[1]
            self.dimensionsPx = (texture_dimensions[0] * scale, self.dimensionsPx[1])
        self.update()

    def list_click_off_function(self):
        if self.cof is not None:
            self.app.add_click_off_binding(self)

    def delist_click_off_function(self):
        if self.cof is not None:
            self.app.remove_click_off_binding(self)

    def list_text_function(self):
        if self.text_func is not None:
            self.app.add_text_binding(self)

    def delist_text_function(self):
        if self.text_func is not None:
            self.app.remove_text_binding(self)

    def select(self, *args):
        self.selected = True
        self.app.add_text_binding(self)

    def deselect(self, *args):
        self.selected = False
        self.app.remove_text_binding(self)

    def click_off(self, trigger, buttons):
        if self.selected:
            self.cof()
