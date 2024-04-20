import pygame as pg
from abc import ABC, abstractmethod
from ..appinterface import AppInterface

class StageKeyFuncs(ABC):
    app: AppInterface
    def quit(self, key, keys):
        if key == pg.K_ESCAPE:
            self.app.quit()

