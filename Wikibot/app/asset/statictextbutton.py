from .statictext import StaticText, StaticTextCreateInfo
from .buttontype import ButtonType, ButtonCreateInfo
from dataclasses import dataclass
from typing import Union
import numpy as np
import logging


@dataclass()
class StaticTextButtonCreateInfo(ButtonCreateInfo, StaticTextCreateInfo):
    pass


class StaticTextButton(ButtonType, StaticText):
    def __init__(self, info: Union[type[StaticTextButtonCreateInfo], StaticTextButtonCreateInfo]):
        StaticText.__init__(self, info)
        ButtonType.__init__(self, info)
        self.bb_corners = self.get_corners()
        self.rectangular_bounds = self.get_bounds()

    def get_corners(self) -> list[np.ndarray]:
        # Determine where the corners of the button are
        bottom_left = [-0.5 * self.dimensionsPx[0], -0.5 * self.dimensionsPx[1]]
        top_right = [0.5 * self.dimensionsPx[0], 0.5 * self.dimensionsPx[1]]
        top_left = [bottom_left[0], top_right[1]]
        bottom_right = [top_right[0], bottom_left[1]]
        # Create list of corners, convert them to numpy vectors
        corners = [top_left, top_right, bottom_left, bottom_right]
        corners = [np.array([[corner[0]], [corner[1]]], dtype=float) for corner in corners]

        scaling_matrix = np.array([[self.scale[0], 0],
                                   [0, self.scale[1]]], dtype=float)

        # create translation vector
        translation_vector = np.array([[self.posPx[0] + 0.5 * self.scale[0] * self.dimensionsPx[0]],
                                       [self.posPx[1] + 0.5 * self.scale[1] * self.dimensionsPx[1]]], dtype=float)

        # Compute corners from matrix mult
        for corner in corners:
            np.matmul(scaling_matrix, corner, out=corner)
            np.add(translation_vector, corner, out=corner)

        # Output corners as 1d arrays, flip top and bottom coords
        corners = [corners[2], corners[3], corners[0], corners[1]]
        return [corner.flatten() for corner in corners]

    def get_bounds(self) -> list[
        list[Union[tuple, int], Union[tuple, int]], list[Union[tuple, int], Union[tuple, int]]]:
        # Determine the min and max x's and y's of the button, allowing for easy collision checks
        x_bounds = [min(corner[0] for corner in self.bb_corners), max(corner[0] for corner in self.bb_corners)]
        y_bounds = [min(corner[1] for corner in self.bb_corners), max(corner[1] for corner in self.bb_corners)]
        return [x_bounds, y_bounds]

    def list_collision_boundaries(self) -> None:
        # Append collision boundaries to mainloop boundary array
        self.app.list_bounded_object(self)

    def delist_collision_boundaries(self) -> None:
        # Remove collision boundaries from mainloop boundary array
        self.app.delist_bounded_object(self)

    def add_to_scene(self, scene_layer: int = None) -> None:
        # Add button to scene, overwrites StaticText implementation to allow for collision boundary listing
        if not self.isViewable:
            logging.info(f"Adding {self.__class__.__name__} instance \'{self.name}\' to scene")
            self.isViewable = True
            self.list_collision_boundaries()
            self.list_hover_functions()
            self.list_click_functions()
            if not scene_layer:
                self.app.append_model_to_scene(self.model)
            else:
                self.app.insert_model_into_scene(scene_layer, self.model)
        else:
            logging.warning(
                f' failed to add {self.__class__.__name__} object \'{self.name}\' to scene: already viewable in scene')

    def remove_from_scene(self) -> None:
        # Remove button from scene, overwrites StaticText implementation to allow for collision boundary de-listing
        if self.isViewable:
            logging.info(f"Removing {self.__class__.__name__} instance \'{self.name}\' from scene")
            self.isViewable = False
            self.delist_collision_boundaries()
            self.delist_hover_functions()
            self.delist_click_functions()
            self.app.remove_model_from_scene(self.model)
        else:
            logging.warning(
                f' failed to remove {self.__class__.__name__} object \'{self.name}\' to scene: object not viewable in scene')

    def update(self) -> None:
        # Update the button if it moves or changes
        StaticText.update(self)
        self.bb_corners = self.get_corners()
        self.rectangular_bounds = self.get_bounds()

    def updateTo(self, model) -> None:
        # Change the model to an already-extant model and update the button
        StaticText.updateTo(self, model)
        self.bb_corners = self.get_corners()
        self.rectangular_bounds = self.get_bounds()

    def list_hover_functions(self):
        if self.haf is not None:
            self.app.add_hover_activate_binding(self)
        if self.hdf is not None:
            self.app.add_hover_deactivate_binding(self)

    def delist_hover_functions(self):
        if self.haf is not None:
            self.app.remove_hover_activate_binding(self)
        if self.hdf is not None:
            self.app.add_hover_deactivate_binding(self)

    def list_click_functions(self):
        if self.cafs is not None:
            for trigger in self.cafs.keys():
                self.app.add_mouse_down_binding(trigger, self)
        if self.cdfs is not None:
            for trigger in self.cdfs.keys():
                self.app.add_mouse_up_binding(trigger, self)

    def delist_click_functions(self):
        if self.cafs is not None:
            for trigger in self.cafs.keys():
                self.app.remove_mouse_down_binding(trigger, self)
        if self.cdfs is not None:
            for trigger in self.cdfs.keys():
                self.app.remove_mouse_up_binding(trigger, self)