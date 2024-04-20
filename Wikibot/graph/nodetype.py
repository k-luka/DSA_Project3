from abc import ABC, abstractmethod
from ..app.appinterface import AppInterface
from typing import Union
# from ..app.asset import Sprite


class NodeType(ABC):
    app: Union[type[AppInterface], AppInterface]
    stage: ...
    title: str
    position: tuple[float, float]
    size: Union[int, float]
    sprite: ...

    @abstractmethod
    def get_scr_pos(self) -> tuple[float, float]: pass

    @abstractmethod
    def get_center(self) -> tuple[float, float]: pass

