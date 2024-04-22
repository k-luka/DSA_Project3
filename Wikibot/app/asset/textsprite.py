from .statictextbutton import StaticTextButton, StaticTextButtonCreateInfo
from dataclasses import dataclass
from typing import Union, Callable, Optional, Sequence
import logging
import pygame as pg


@dataclass()
class TextSpriteCreateInfo(StaticTextButtonCreateInfo):
    text_func: Optional[str] = None
    auto_textbox_scaling: bool = False
    pass

class TextSprite(StaticTextButton):
    selected: bool = False
    text_func: Optional[Callable[[int, Sequence[bool]], None]] = None
    auto_textbox_scaling: bool = False
    default_scale: Optional[Union[tuple[int, int], tuple[float, float]]]
    ever_clicked: bool = False

    def __init__(self, info: Union[type[TextSpriteCreateInfo], TextSpriteCreateInfo]):
        StaticTextButton.__init__(self, info)
        self._initialize_text_func(info.text_func)
        # Doing it auto rescaling after StaticTextButton initialization to avoid work
        self.auto_textbox_scaling = info.auto_textbox_scaling
        if self.auto_textbox_scaling:
            self.default_scale = self.scale
            texture_surface: pg.Surface = self.app.get_texture(self.texture_name)
            texture_dimensions = texture_surface.size
            scale: tuple[float, float] = (texture_dimensions[0] * self.default_scale[0] / self.dimensionsPx[0],
                                          texture_dimensions[1] * self.default_scale[1] / self.dimensionsPx[1])
            self.rescale(scale)
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
            scale: tuple[float, float] = (texture_dimensions[0] * self.default_scale[0] / self.dimensionsPx[0],
                                          texture_dimensions[1] * self.default_scale[1] / self.dimensionsPx[1])
            if scale[0] <= 1:
                self.rescale(scale)
        self.update()

    def list_text_function(self):
        if self.text_func is not None:
            self.app.add_text_binding(self)

    def delist_text_function(self):
        if self.text_func is not None:
            self.app.remove_text_binding(self)

    def select(self, *args):
        if self.selected:
            return
        self.selected = True
        self.app.add_text_binding(self)
        if not self.ever_clicked or self.text_func == self.type_numeric_one_digit:
            self.ever_clicked = True
            self.update_text('')
        self.moveByPx((1, 1))


    def deselect(self, *args):
        if not self.selected:
            return
        self.selected = False
        self.app.remove_text_binding(self)
        self.moveByPx((-1, -1))
