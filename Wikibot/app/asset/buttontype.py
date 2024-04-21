from dataclasses import dataclass, field
from typing import Optional, Callable, Union
from .buttonfuncs import ButtonFuncs
import logging


@dataclass()
class ButtonCreateInfo:
    # click activate function lists
    cafs: Optional[dict[int, str]] = None
    cdfs: Optional[dict[int, str]] = None

    # hover activate function, hover deactivate function, hover-hold function
    haf: Optional[str] = None
    hdf: Optional[str] = None


class ButtonType(ButtonFuncs):
    # click activate function lists
    cafs: Optional[dict[int, Callable[[int, tuple[bool, bool, bool] | tuple[bool, bool, bool, bool, bool]], None]]] = field(init=False, default=None)
    cdfs: Optional[dict[int, Callable[[int, tuple[bool, bool, bool] | tuple[bool, bool, bool, bool, bool]], None]]] = field(init=False, default=None)
    # hover activate function, hover deactivate function, hover-hold function
    haf: Optional[Callable[[], None]] = field(init=False, default=None)
    hdf: Optional[Callable[[], None]] = field(init=False, default=None)
    # Other state tacking vars
    click_times: dict = field(init=False, default=dict)

    def __init__(self, info: Union[type[ButtonCreateInfo], ButtonCreateInfo]):
        logging.info(f' Generating ButtonBase data for {self.__class__.__name__} object')
        self._initialize_cafs(info.cafs)
        self._initialize_cdfs(info.cdfs)
        self._initialize_haf(info.haf)
        self._initialize_hdf(info.hdf)
        self.isClicked = [False, False, False, False, False]

    def _initialize_cafs(self, string_cafs: dict[int, str]) -> None:
        if string_cafs is None:
            self.cafs = None
            return

        self.cafs = {}
        for button in string_cafs:
            func = getattr(self, string_cafs[button], None)
            if func is None:
                logging.warning(f' {self.__class__.__name__} object \'{self.__repr__}\' '
                                f'attempted to set click activate function to \'{string_cafs[button]}\', but \'{string_cafs[button]}\' does not exist '
                                f'as any button funcs, button base, or {self.__class__.__name__} class or parent class method. '
                                f'Setting to \'None\' instead')
            self.cafs[button] = func

    def _initialize_cdfs(self, string_cdfs: dict[int, str]) -> None:
        if string_cdfs is None:
            self.cdfs = None
            return

        self.cdfs = {}
        for button in string_cdfs:
            func = getattr(self, string_cdfs[button], None)
            if func is None:
                logging.warning(f' {self.__class__.__name__} object \'{self.__repr__}\' '
                                f'attempted to set click deactivate function to \'{string_cdfs[button]}\', but \'{string_cdfs[button]}\' does not exist '
                                f'as any button funcs, button base, or {self.__class__.__name__} class or parent class method. '
                                f'Setting to \'None\' instead')
            self.cdfs[button] = func

    def _initialize_haf(self, string_haf: str) -> None:
        if string_haf is None:
            self.haf = None
            return

        func = getattr(self, string_haf, None)
        if func is None:
            logging.warning(f' {self.__class__.__name__} object \'{self.__repr__}\' '
                            f'attempted to set hover activate function to \'{string_haf}\', but \'{string_haf}\' does not exist '
                            f'as any button funcs, button base, or {self.__class__.__name__} class or parent class method. '
                            f'Setting to \'None\' instead')
        self.haf = func

    def _initialize_hdf(self, string_hdf: str) -> None:
        if string_hdf is None:
            self.hdf = None
            return

        func = getattr(self, string_hdf, None)
        if func is None:
            logging.warning(f' {self.__class__.__name__} object \'{self.__repr__}\' '
                            f'attempted to set hover activate function to \'{string_hdf}\', but \'{string_hdf}\' does not exist '
                            f'as any button funcs, button base, or {self.__class__.__name__} class or parent class method. '
                            f'Setting to \'None\' instead')
        self.hdf = func

    def hover_activate(self) -> None:
        # Turns hover on and runs hover-activate-function
        self.haf()

    def hover_deactivate(self) -> None:
        # Turns hover off and runs hover-deactivate-function
        self.hdf()

    def mouse_down(self, button: int, buttons: tuple[bool, bool, bool] | tuple[bool, bool, bool, bool, bool]) -> None:
        # If a mouse button goes down, runs click-activate-functions corresponding to the mouse button that clicked it
        if self.cafs is not None and button in self.cafs and self.cafs[button] is not None:
            self.cafs[button](button, buttons)

    def mouse_up(self, button: int, buttons: tuple[bool, bool, bool] | tuple[bool, bool, bool, bool, bool]) -> None:
        # If a mouse button comes up, runs click-activate-functions corresponding to the mouse button that clicked it
        if self.cdfs is not None and button in self.cdfs and self.cdfs[button] is not None:
            self.cdfs[button](button, buttons)

    def switch_to_texture(self, value: int) -> None: pass
