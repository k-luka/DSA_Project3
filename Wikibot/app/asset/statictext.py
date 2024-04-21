from __future__ import annotations
from dataclasses import dataclass, field
from typing import Union, Optional, Callable, Sequence
from .staticdrawable import StaticDrawable, StaticDrawableCreateInfo
from .typefuncs import TypeFuncs
import logging


@dataclass()
class StaticTextCreateInfo(StaticDrawableCreateInfo):
    # Text properties
    size: int = 0
    color: tuple[int, int, int] = (0, 0, 0)
    text: str = ''
    background: Optional[tuple[int, int, int]] = None


class StaticText(StaticDrawable, TypeFuncs):
    # Basic class for text objects
    # Text properties
    size: int = 0
    color: tuple[int, int, int] = (0, 0, 0)
    text: str = ''
    background: Optional[tuple[int, int, int]] = None
    # Internal variables
    program_name: str = 'texture_2d'

    def __init__(self, info: Union[type[StaticTextCreateInfo], StaticTextCreateInfo]):
        self.posPx = info.posPx
        self.size = info.size
        self.color = info.color
        self.text = info.text
        self.background = info.background
        self.name = info.name
        self.texture_name = f"{self.name}.{self.text}"
        self.textures = [self.texture_name]
        StaticDrawable.__init__(self, info)

        # Rescale to establish initial scale and gain initial model
        self.rescale(self.scale)

    def _initialize_texture(self) -> None:
        self.app.add_render_program(self.program_name)
        self.app.add_text_texture(self.texture_name, self.size, self.color, self.text, self.background)

    def update_text(self, new_text: str, *args) -> None:
        pass