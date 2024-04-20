import logging
from abc import ABC, abstractmethod
from ..appinterface import AppInterface


class StageFuncs(ABC):
    state: int
    asset_dictionary: dict
    @abstractmethod
    def unload(self) -> None: pass

    def main_menu(self):
        if self.state == -1:
            self.unload()
        elif self.state == 0:
            for asset in self.asset_dictionary.values():
                asset.add_to_scene()
        else:
            logging.critical(f'Failed to run StageFunc \'main_menu\': '
                             f'At least one required attribute from class {self.__class__.__name__} is missing')