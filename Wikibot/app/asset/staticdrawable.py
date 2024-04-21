from __future__ import annotations
from dataclasses import dataclass, field
from typing import Union, Optional, Callable, Sequence
from Wikibot.engine import GUI_VBO, GUI
from ..stages.stagetype import StageType
import logging
from ..appinterface import AppInterface
from .assetkeyfuncs import Keyfuncs


@dataclass()
class StaticDrawableCreateInfo:
    # Identifying properties
    app: AppInterface
    name: str
    stage: Union[type[StageType], StageType]
    # Physical properties
    posPx: Optional[Union[tuple[float, float], tuple[int, int], None]] = None
    dimensionsPx: Optional[Union[tuple[float, float], tuple[int, int]]] = None
    scale: Optional[Union[tuple[float, float], tuple[int, int], None]] = field(default=(1, 1))
    rot: Optional[Union[float, int]] = field(default=0)
    # Dynamic function bindings
    kdfs: Optional[dict[int, str]] = None
    kufs: Optional[dict[int, str]] = None


class StaticDrawable(Keyfuncs):
    # Identifying properties
    app: AppInterface = False
    name: str = False
    stage: Union[type[StageType]] = False
    # Physical properties
    textures: Union[tuple[str, ...], list[str, ...]] = list()
    posPx: Optional[Union[tuple[float, float], tuple[int, int], None]] = None
    dimensionsPx: Optional[Union[tuple[float, float], tuple[int, int]]] = None
    scale: Optional[Union[tuple[float, float], tuple[int, int], None]] = (1, 1)
    rot: Optional[Union[float, int]] = 0
    kdfs: Optional[dict[int, Callable[[int, Sequence[bool]], None]]] = None
    kufs: Optional[dict[int, Callable[[int, Sequence[bool]], None]]] = None
    # Post-initialization parameters
    vbo_name: Optional[str] = None
    vao_name: Optional[str] = None
    texture_name: Optional[str] = None
    model: Optional[GUI] = None
    # Internal variables
    program_name: str = 'texture_2d'
    current_texture: int = 0
    isViewable: bool = False

    def __init__(self, info: Union[type[StaticDrawableCreateInfo], StaticDrawableCreateInfo]):
        # Establish initial vars
        self.app = info.app
        self.name = info.name
        self.stage = info.stage
        self.posPx = info.posPx
        self.dimensionsPx = info.dimensionsPx
        self.scale = info.scale
        self.rot = info.rot
        self._initialize_kdfs(info.kdfs)
        self._initialize_kufs(info.kufs)
        logging.info(f' Generating StaticDrawable data for {self.__class__.__name__} object \'{self.name}\'')

        self._initialize_position()
        self._initialize_texture()
        self.rescale(self.scale)

    def _initialize_kdfs(self, string_kdfs) -> None:
        # Exit if string_kdfs does not exist key
        if string_kdfs is None:
            self.kdfs = None
            return
        # Turn key function strings into callable funcs
        self.kdfs = {}
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
        self.kufs = {}
        for key in string_kufs:
            func = getattr(self, string_kufs[key], None)
            if func is None:
                logging.warning(f' {self.__class__.__name__} object \'{self.__repr__}\' '
                                f'attempted to set key up function to \'{string_kufs[key]}\', but \'{string_kufs[key]}\' does not exist '
                                f'as any key funcs or {self.__class__.__name__} class or parent class method. '
                                f'Setting to \'None\' instead')
            self.kufs[key] = func

    def _initialize_position(self) -> None:
        # Compute position conversion based on 2D graphing mode
        if self.posPx is not None:
            self.pos = self.px_to_scr(self.posPx)

        # Establish default pos and dim values if none are given
        if self.posPx is None:
            self.pos = (-1, 1)
            self.posPx = (0, 0)
        if self.dimensionsPx is None:
            self.dimensionsPx = (0, 0)
            # Set aspect ratio to 0 for later, will make it impossible for image to render
            self.aspect_ratio = 0
            logging.warning(
                f' Creating {self.__class__.__name__} object \'{self.name}\' without specified initial dimensions; image will not render upon rescaling')

        # Create vars for initial width and height
        self.width, self.height = self.dimensionsPx

    def _initialize_texture(self) -> None:
        # Ensure that program name and texture files exist
        self.app.add_render_program(self.program_name)
        for texture_name in self.textures:
            self.app.add_texture(texture_name)
        # Ensure that texture name is set
        self.texture_name = self.textures[0]

    def rescale(self, scale: Union[tuple[float, float], tuple[int, int]]) -> None:
        # Establish temp scales
        self.scale = scale
        x_scale, y_scale = scale
        scaled_width = self.dimensionsPx[0] * x_scale
        scaled_height = self.dimensionsPx[1] * y_scale

        # Regenerate VBO
        self.vbo_name = f'gui_vbo_{self.textures[self.current_texture]}_{self.name}'
        self.app.regenerate_vbo(self.vbo_name, GUI_VBO, scaled_width, scaled_height)

        # Regenerate VAO
        self.vao_name = f'gui_vao_{self.textures[self.current_texture]}_{self.name}'
        self.app.regenerate_vao(self.vao_name, self.vbo_name, self.program_name)

        # Update model in scene if object is viewable
        self.update()

    def switch_to_texture(self, texture_index: int) -> None:
        # Switch from a texture to another texture
        num_textures = len(self.textures)
        if (-num_textures) <= texture_index < num_textures:
            self.current_texture = texture_index
            self.texture_name = self.textures[texture_index]
            self.update()
        else:
            logging.warning(
                f' failed to switch {self.__class__.__name__} object \'{self.name}\'s texture to texture [{texture_index}]: '
                f'texture index is not in range of textures array')

    def switch_to_texture_name(self, texture_name: str) -> None:
        if texture_name in self.textures:
            self.texture_name = texture_name
            self.update()
        else:
            logging.warning(
                f' failed to switch {self.__class__.__name__} object \'{self.name}\'s texture \'{texture_name}\': '
                f'\'{texture_name}\' is not a registered texture')

    def generate_model(self) -> GUI:
        # Generate a model for rendering
        model = GUI(app=self.app,
                    vao_name=self.vao_name,
                    texture_name=self.texture_name,
                    pos=self.pos,
                    dimensions=self.dimensionsPx,
                    scale=self.scale,
                    rot=self.rot
                    )
        return model

    def update(self) -> None:
        # Update the current model
        new_model = self.generate_model()
        if self.isViewable:
            scene_layer = self.app.get_model_layer(self.model)
            self.app.set_model_in(scene_layer, new_model)
        self.model = new_model

    def updateTo(self, model: GUI) -> None:
        # Update the model to an already-extant model
        if self.isViewable:
            scene_layer = self.app.get_model_layer(self.model)
            self.app.set_model_in(scene_layer, model)
        self.model = model

    def load(self) -> None:
        # Add self to mainloop active objects list, add key maps to key mapping dictionary
        logging.info(f"Loading {__class__.__name__} instance \'{self.name}\' into mainloop game object list")
        self.app.add_static_drawable(self)
        if self.kdfs is not None:
            for key in self.kdfs.keys():
                self.app.add_key_down_binding(key, self)
        if self.kufs is not None:
            for key in self.kufs:
                self.app.add_key_up_binding(key, self)

    def unload(self) -> None:
        # Remove self from active objects list and from any key maps in the key mapping dictionary
        logging.info(f"Unloading {__class__.__name__} instance \'{self.name}\' from mainloop game object list")
        self.app.remove_static_drawable(self)
        if self.kdfs is not None:
            for key in self.kdfs.keys():
                self.app.remove_key_down_binding(key, self)
        if self.kufs is not None:
            for key in self.kufs.keys():
                self.app.remove_key_up_binding(key, self)

    def add_to_scene(self, scene_layer: int = None) -> None:
        # Add model to scene list of models for rendering
        if not self.isViewable:
            logging.info(f"Adding {self.__class__.__name__} instance \'{self.name}\' to scene")
            self.isViewable = True
            if not scene_layer:
                self.app.append_model_to_scene(self.model)
            else:
                self.app.insert_model_into_scene(scene_layer, self.model)
        else:
            logging.warning(
                f' failed to add {self.__class__.__name__} object \'{self.name}\' to scene: already viewable in scene')

    def move_to_scene_layer(self, scene_layer: int) -> None:
        # Move model to another index in the scene model array, putting it above/below other 2D models
        if not self.isViewable:
            logging.warning(
                f' failed to move {self.__class__.__name__} object \'{self.name}\' to scene layer [{scene_layer}]: object is not viewable in scene')
            return

        scene_objects = self.app.scene_object_count()
        if scene_layer < (-scene_objects) or scene_layer >= scene_objects:
            logging.warning(
                f' failed to move {self.__class__.__name__} object \'{self.name}\' to scene layer [{scene_layer}]: scene layer index not in range of scene object array')
            return

        logging.info(f"Moving {self.__class__.__name__} instance \'{self.name}\' to scene layer {scene_layer}")
        self.remove_from_scene()
        self.add_to_scene(scene_layer)

    def remove_from_scene(self) -> None:
        # Remove model from list of models for rendering
        if not self.isViewable:
            logging.warning(
                f' failed to remove {self.__class__.__name__} object \'{self.name}\' to scene: object not viewable in scene')
            return

        logging.info(f"Removing {self.__class__.__name__} instance \'{self.name}\' from scene")
        self.isViewable = False
        self.app.remove_model_from_scene(self.model)

    def px_to_scr(self, posPx: Union[tuple[float, float], tuple[int, int]]) -> Union[
        tuple[float, float], tuple[int, int]]:
        # Convert from pixel location to screen proportion
        scr_width, scr_height = self.app.win_size()
        pos = (((posPx[0] * 2) / scr_width) - 1,
               ((posPx[1] * -2) / scr_height) + 1)
        return pos

    def key_down(self, key: int, keys: Sequence[bool]):
        # Activate key-down functions, passing list of downed keys in
        self.kdfs[key](key, keys)

    def key_up(self, key: int, keys: Sequence[bool]):
        # Activate key-up functions, passing list of lifted keys in
        self.kufs[key](key, keys)