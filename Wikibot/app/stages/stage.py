from __future__ import annotations
from typing import Union, Optional, Callable, Sequence, TypeVar
from dataclasses import dataclass, field
from ..appinterface import AppInterface
import logging
from .stagefuncs import StageFuncs
from .stagekeyfuncs import StageKeyFuncs
from ..asset import *
from .stagetype import StageType

@dataclass()
class AssetCreateInfo:
    asset_info: Union[ButtonCreateInfo, SpriteCreateInfo, StaticButtonCreateInfo,
    StaticDrawableCreateInfo, StaticImageCreateInfo, StaticTextCreateInfo]
    asset_type: type[Union[ButtonType, Sprite, StaticButton, StaticDrawable, StaticImage, StaticText]]
    start_visible: Optional[bool] = False


@dataclass()
class StageCreateInfo:
    app: Union[type[AppInterface], AppInterface]
    name: str
    stage_func: Optional[str] = None
    kdfs: Optional[dict[int, str]] = None
    kufs: Optional[dict[int, str]] = None


class Stage(StageType, StageFuncs, StageKeyFuncs):
    app: AppInterface
    name: str
    state: int = -1
    stage_func: Callable[[], None]
    kdfs: Optional[dict[int, Callable[[int, Sequence[bool]], None]]] = field(init=False, default=None)
    kufs: Optional[dict[int, Callable[[int, Sequence[bool]], None]]] = field(init=False, default=None)
    asset_dictionary: dict[str, ...] = dict()

    def __init__(self, info: StageCreateInfo):
        self.app = info.app
        self.name = info.name
        self.asset_dictionary = dict()
        self._initialize_stage_func(info.stage_func)
        self._initialize_kdfs(info.kdfs)
        self._initialize_kufs(info.kufs)

    def _initialize_stage_func(self, stage_func):
        if stage_func is None:
            self.stage_func = getattr(self, f'{self.name}', None)
            if self.stage_func is None:
                logging.critical(f' Failed to load stage function \'{self.name}\' for stage \'{self.name}\': StageFunc does not exist')
        else:
            self.stage_func = getattr(self, stage_func, None)
            if self.stage_func is None:
                logging.critical(f' Failed to load stage function \'{stage_func}\' for stage \'{self.name}\': StageFunc does not exist')

    def _initialize_kdfs(self, string_kdfs) -> None:
        # Exit if string_kdfs does not exist key
        if string_kdfs is None:
            self.kdfs = None
            return
        # Turn key function strings into callable funcs
        self.kdfs = dict()
        for key in string_kdfs:
            func = getattr(self, string_kdfs[key], None)
            if func is None:
                logging.warning(f' {self.__class__.__name__} object \'{self.__repr__}\' '
                                f'attempted to set key down function to \'{string_kdfs[key]}\', but \'{string_kdfs[key]}\' does not exist '
                                f'as any key funcs or {self.__class__.__name__} class or parent class method. '
                                f'Setting to \'None\' instead')
            self.kdfs[key] = func

    def _initialize_kufs(self, string_kufs) -> None:
        # Exit if string_kdfs does not exist key
        if string_kufs is None:
            self.kufs = None
            return
        # Turn key function strings into callable funcs
        self.kufs = dict()
        for key in string_kufs:
            func = getattr(self, string_kufs[key], None)
            if func is None:
                logging.warning(f' {self.__class__.__name__} object \'{self.__repr__}\' '
                                f'attempted to set key up function to \'{string_kufs[key]}\', but \'{string_kufs[key]}\' does not exist '
                                f'as any key funcs or {self.__class__.__name__} class or parent class method. '
                                f'Setting to \'None\' instead')
            self.kufs[key] = func

    def create_asset(self, info: AssetCreateInfo) -> None:
        if info.asset_info.name in self.asset_dictionary:
            logging.warning(f"Attempting to create an asset with duplicate name {info.asset_info.name}. Overwriting old object")
            # del self.asset_dictionary[info.asset_info.name]
        self.asset_dictionary[info.asset_info.name] = info.asset_type(info.asset_info)
        asset = self.asset_dictionary[info.asset_info.name]
        if self.state > -1:
            asset.load()
        if info.start_visible and self.state > -1:
            asset.add_to_scene()
        logging.info(f"Successfully loaded asset \'{asset.name}\'")

    def remove_game_object(self, asset) -> None:
        if not asset.name in self.asset_dictionary:
            logging.warning(f"Failed to remove asset \'{asset.name}\': Asset is not in asset dictionary")
            return
        if self.state > -1:
            asset.unload()
        if asset.isViewable:
            self.asset_dictionary[asset.name].remove_from_scene()
        del self.asset_dictionary[asset.name]

    def load(self) -> None:
        logging.info(f"Loading stage \'{self.name}\'")
        self.state = 0
        # Append app objects to mainloop app object list
        for asset in self.asset_dictionary.values():
            logging.info(f"Loading stage asset \'{asset.name}\'")
            asset.load()
        # Load key funcs
        if self.kdfs is not None:
            for key in self.kdfs.keys():
                self.app.add_key_down_binding(key, self)
        if self.kufs is not None:
            for key in self.kufs.keys():
                self.app.add_key_up_binding(key, self)
        self.update(0)

    def unload(self) -> None:
        logging.info(f"Unloading stage \'{self.name}\'")
        self.state = -1
        for asset in self.asset_dictionary.values():
            if asset.isViewable:
                asset.remove_from_scene()
            logging.info(f"Unloading stage asset \'{asset.name}\'")
            asset.unload()
        # Unload key funcs
        if self.kdfs is not None:
            for key in self.kdfs.keys():
                self.app.remove_key_down_binding(key, self)
        if self.kufs is not None:
            for key in self.kufs.keys():
                self.app.remove_key_up_binding(key, self)

    def update(self, new_state: int) -> None:
        self.state = new_state
        if self.stage_func is not None:
            self.stage_func()

    def key_down(self, key, keys) -> None:
        self.kdfs[key](key, keys)

    def key_up(self, key, keys) -> None:
        self.kufs[key](key, keys)
