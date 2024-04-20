from __future__ import annotations
from .staticdrawable import *


@dataclass()
class StaticTextCreateInfo(StaticDrawableCreateInfo):
    # Text properties
    size: int = 0
    color: tuple[int, int, int] = (0, 0, 0)
    text: str = ''
    background: Optional[tuple[int, int, int]] = None


class StaticText(StaticDrawable):
    # Basic class for text objects
    # Text properties
    size: int = field(init=False, default=0)
    color: tuple[int, int, int] = field(init=False, default=(0, 0, 0))
    text: str = field(init=False, default='')
    background: Optional[tuple[int, int, int]] = field(init=False, default=None)
    # Internal variables
    program_name: str = field(init=False, default='texture_2d')

    def __init__(self, info: Union[type[StaticTextCreateInfo], StaticTextCreateInfo]):
        self.posPx = info.posPx
        self.size = info.size
        self.color = info.color
        self.text = info.text
        self.texture = f"{self.name}.{self.text}"
        self.textures = [self.texture]
        StaticDrawable.__init__(self, info)

        # Rescale to establish initial scale and gain initial model
        self.rescale(self.scale)

    def _initialize_texture(self) -> None:
        self.app.add_render_program(self.program_name)
        self.app.add_text_texture(self.texture, self.size, self.color, self.text, self.background)
