import pygame as pg
from .assetgenerator import generate_stage_info, generate_asset_info
from .appinterface import AppInterface
from dataclasses import field
from typing import Union
from .asset import Sprite, StaticDrawable, StaticButton
import logging
from .stages import Stage


class MainLoop:
    app: AppInterface
    FPS: int
    debug: int
    sprites: set[Sprite] = field(init=False, default_factory=set)
    drawings: set[Union[type[StaticDrawable], StaticDrawable]] = set()
    key_down_bindings: dict[int, set[Union[type[StaticDrawable], StaticDrawable]]] = dict()
    key_up_bindings: dict[int, set[Union[type[StaticDrawable], StaticDrawable]]] = dict()
    mouse_down_bindings: dict[int, set[Union[type[StaticButton], StaticButton]]] = dict()
    mouse_up_bindings: dict[int, set[Union[type[StaticButton], StaticButton]]] =dict()
    hover_activate_bindings: set[Union[type[StaticButton], StaticButton]] = set()
    hover_deactivate_bindings: set[Union[type[StaticButton], StaticButton]] = set()
    stages: dict[str, Stage] = dict()
    bounded_objects: set[Union[type[StaticButton], StaticButton]] = set()
    hover_activated_objects: set[Union[type[StaticButton], StaticButton]] = set()

    # Class that handles app execution every frame
    def __init__(self, app, compute_fps, debug):
        self.app = app
        self.FPS = compute_fps
        self.debug = debug
        self.stages = dict()

    def initialize_stages(self) -> None:
        # Generate stages and load main menu
        stage_info = generate_stage_info(self.app)
        for info in stage_info:
            self.stages[info.name] = Stage(info)
        for stage in self.stages.values():
            initial_assets_info = generate_asset_info(stage)
            for asset_info in initial_assets_info:
                stage.create_asset(asset_info)
        if "main_menu" not in self.stages.keys():
            logging.warning("Failed to load \'main menu\' stage: program may not display as intended")
            return
        self.stages["main_menu"].load()

    def check_app_updates(self) -> None:
        # Check for important update from pygame
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.app.quit()

            elif event.type == pg.KEYDOWN:
                self.handle_key_down(event.key)

            elif event.type == pg.KEYUP:
                self.handle_key_up(event.key)

            elif event.type == pg.MOUSEBUTTONDOWN:
                self.handle_mouse_down(event.button)

            elif event.type == pg.MOUSEBUTTONUP:
                self.handle_mouse_up(event.button)

    def do_collisions(self) -> None:
        # Check for collisions between the mouse and a button
        mouse_pos = pg.mouse.get_pos()

        for interactive_object in self.bounded_objects:
            x_bounds, y_bounds = interactive_object.rectangular_bounds
            if (x_bounds[0] <= mouse_pos[0] <= x_bounds[1] and
                    y_bounds[0] <= mouse_pos[1] <= y_bounds[1]):
                if interactive_object not in self.hover_activated_objects:
                    self.handle_hover_activate_event(interactive_object)
            elif interactive_object in self.hover_activated_objects:
                # Run hover deactivate function if leaving hover
                self.handle_hover_deactivate_event(interactive_object)


    def handle_hover_activate_event(self, interactive_object: Union[type[StaticButton], StaticButton]):
        self.hover_activated_objects.add(interactive_object)
        if interactive_object in self.hover_activate_bindings:
            interactive_object.hover_activate()

    def handle_hover_deactivate_event(self, interactive_object: Union[type[StaticButton], StaticButton]):
        self.hover_activated_objects.remove(interactive_object)
        if interactive_object in self.hover_deactivate_bindings:
            interactive_object.hover_deactivate()

    def handle_key_up(self, trigger: int) -> None:
        if trigger not in self.key_up_bindings.keys():
            return
        keys = pg.key.get_pressed()
        for drawable in self.key_up_bindings[trigger]:
            drawable.key_up(trigger, keys)

    def handle_key_down(self, trigger: int) -> None:
        if trigger not in self.key_down_bindings.keys():
            return
        keys = pg.key.get_pressed()
        for drawable in self.key_down_bindings[trigger]:
            drawable.key_down(trigger, keys)

    def handle_mouse_down(self, trigger: int) -> None:
        if trigger not in self.mouse_down_bindings.keys():
            return
        buttons = pg.mouse.get_pressed()
        for clickable in self.mouse_down_bindings[trigger].intersection(self.hover_activated_objects):
            clickable.mouse_down(trigger, buttons)

    def handle_mouse_up(self, trigger: int) -> None:
        if trigger not in self.mouse_up_bindings.keys():
            return
        buttons = pg.mouse.get_pressed()
        for clickable in self.mouse_up_bindings[trigger].intersection(self.hover_activated_objects):
            clickable.mouse_up(trigger, buttons)

    def execute(self) -> None:
        # Main overarching code for app loop
        self.do_collisions()
        self.check_app_updates()
        self.app.graphics.render_frame()

    def add_kd_binding(self, trigger, drawable) -> None:
        if trigger not in self.key_down_bindings.keys():
            self.key_down_bindings[trigger] = set()
        self.key_down_bindings[trigger].add(drawable)

    def add_ku_binding(self, trigger, drawable) -> None:
        if trigger not in self.key_up_bindings.keys():
            self.key_up_bindings[trigger] = set()
        self.key_up_bindings[trigger].add(drawable)

    def add_md_binding(self, trigger, clickable) -> None:
        if trigger not in self.mouse_down_bindings.keys():
            self.mouse_down_bindings[trigger] = set()
        self.mouse_down_bindings[trigger].add(clickable)

    def add_mu_binding(self, trigger, clickable) -> None:
        if trigger not in self.mouse_up_bindings.keys():
            self.mouse_up_bindings[trigger] = set()
        self.mouse_up_bindings[trigger].add(clickable)

    def add_ha_binding(self, hoverable) -> None:
        self.hover_activate_bindings.add(hoverable)

    def add_hd_binding(self, hoverable):
        self.hover_deactivate_bindings.add(hoverable)

    def remove_kd_binding(self, trigger, drawable) -> None:
        if trigger not in self.key_down_bindings.keys():
            logging.warning(f"Failed to remove key down binding for key '{trigger}' and drawable object '{drawable.name}': Trigger has never been bound to an object")
            return
        if drawable not in self.key_down_bindings[trigger]:
            logging.warning(
                f"Failed to remove key down binding for key '{trigger}' and drawable object '{drawable.name}': Object is not bound to that trigger")
            return
        self.key_down_bindings[trigger].remove(drawable)

    def remove_ku_binding(self, trigger, drawable) -> None:
        if trigger not in self.key_up_bindings.keys():
            logging.warning(f"Failed to remove key ip binding for key '{trigger}' and drawable object '{drawable.name}': Trigger has never been bound to an object")
            return
        if drawable not in self.key_up_bindings[trigger]:
            logging.warning(
                f"Failed to remove key up binding for key '{trigger}' and drawable object '{drawable.name}': Object is not bound to that trigger")
            return
        self.key_up_bindings[trigger].remove(drawable)

    def remove_md_binding(self, trigger, clickable) -> None:
        if trigger not in self.mouse_down_bindings.keys():
            logging.warning(f"Failed to remove mouse down binding for key '{trigger}' and drawable object '{clickable.name}': Trigger has never been bound to an object")
            return
        if clickable not in self.mouse_down_bindings[trigger]:
            logging.warning(
                f"Failed to remove mouse down binding for button '{trigger}' and drawable object '{clickable.name}': Object is not bound to that trigger")
            return
        self.mouse_down_bindings[trigger].remove(clickable)

    def remove_mu_binding(self, trigger, clickable) -> None:
        if trigger not in self.mouse_up_bindings.keys():
            logging.warning(f"Failed to remove mouse up binding for button '{trigger}' and drawable object '{clickable.name}': Trigger has never been bound to an object")
            return
        if clickable not in self.mouse_up_bindings[trigger]:
            logging.warning(
                f"Failed to remove mouse up binding for key '{trigger}' and drawable object '{clickable.name}': Object is not bound to that trigger")
            return
        self.mouse_up_bindings[trigger].remove(clickable)

    def remove_ha_binding(self, hoverable) -> None:
        if hoverable not in self.hover_activate_bindings:
            logging.warning(f"Failed to remove hover activate binding for drawable object '{hoverable.name}': Object is not bound to a hover activation")
            return
        self.hover_activate_bindings.remove(hoverable)

    def remove_hd_binding(self, hoverable) -> None:
        if hoverable not in self.hover_deactivate_bindings:
            logging.warning(f"Failed to remove hover activate binding for drawable object '{hoverable.name}': Object is not bound to a hover deactivation")
            return
        self.hover_deactivate_bindings.remove(hoverable)

    def add_bounded_object(self, bounded_object):
        self.bounded_objects.add(bounded_object)

    def remove_bounded_object(self, bounded_object):
        if bounded_object not in self.bounded_objects:
            logging.warning(f"Failed to remove bounded object '{bounded_object.name}' from bounded object list: Object is not in bounded object list")
        self.bounded_objects.remove(bounded_object)

    def add_static_drawable(self, drawable):
        self.drawings.add(drawable)

    def remove_static_drawable(self, drawable):
        if drawable not in self.drawings:
            logging.warning(
                f"Failed to remove {drawable.__class__.__name__} object '{drawable.name}' from static drawable object list: Object is not in static drawable object list")
        self.drawings.remove(drawable)

    def add_sprite_to_stage(self, sprite: Sprite, stage: Stage, make_viewable: bool = False):
        self.stages[stage.name].add_sprite(sprite, make_viewable)

    def remove_sprite_from_stage(self, sprite: Sprite, stage: Stage):
        self.stages[stage.name].destroy_sprite(sprite)