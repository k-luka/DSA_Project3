from .staticbutton import *
from dataclasses import dataclass

@dataclass()
class SpriteCreateInfo(StaticButtonCreateInfo):
    pass

class Sprite(StaticButton):
    def __init__(self, info: Union[type[SpriteCreateInfo], SpriteCreateInfo]):
        StaticButton.__init__(self, info)