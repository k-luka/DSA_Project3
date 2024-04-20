from __future__ import annotations
from .staticdrawable import *


@dataclass()
class StaticImageCreateInfo(StaticDrawableCreateInfo):
    textures: Optional[Union[tuple[str], list[str]]] = field(default_factory=list)


class StaticImage(StaticDrawable):
    def __init__(self, info: Union[type[StaticImageCreateInfo], StaticImageCreateInfo]):
        # Handle special textures case
        self.textures = info.textures
        StaticDrawable.__init__(self, info)