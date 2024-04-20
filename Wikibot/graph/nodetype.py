from abc import ABC, abstractmethod
from ..app.appinterface import AppInterface
from typing import Union
from ..app.asset import Sprite


class NodeType(ABC):
    app: Union[type[AppInterface], AppInterface]
    title: str
    position: tuple[float, float]
    sprite: ...

    @abstractmethod
    def get_scr_pos(self) -> tuple[float, float]: pass # TODO: implement later

