import logging
import pygame as pg
from dataclasses import field
from typing import Union
from .appinterface import AppInterface
from .asset.sprite import Sprite
from .asset.staticdrawable import StaticDrawable
from .asset.buttontype import ButtonType
from .asset.staticbutton import StaticButton
from .asset.textsprite import TextSprite
from .assetgenerator import generate_stage_info, generate_asset_info
from .stages.stage import Stage


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
    click_off_bindings: set[Union[type[TextSprite], TextSprite]] = set()
    clicked_off: set[Union[type[TextSprite], TextSprite]] = set()
    hover_activate_bindings: set[Union[type[StaticButton], StaticButton]] = set()
    hover_deactivate_bindings: set[Union[type[StaticButton], StaticButton]] = set()
    text_bindings: set[TextSprite] = set()
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
        self.clicked_off.clear()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.app.quit()

            elif event.type == pg.KEYDOWN:
                self.handle_key_down(event.key)
                self.handle_text_event(event.unicode)

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
        for clickable in self.click_off_bindings.difference(self.clicked_off).difference(self.hover_activated_objects):
            clickable.click_off(trigger, buttons)
            self.clicked_off.add(clickable)

    def handle_mouse_up(self, trigger: int) -> None:
        if trigger not in self.mouse_up_bindings.keys():
            return
        buttons = pg.mouse.get_pressed()
        for clickable in self.mouse_up_bindings[trigger].intersection(self.hover_activated_objects):
            clickable.mouse_up(trigger, buttons)

    def handle_text_event(self, unicode: int) -> None:
        keys = pg.key.get_pressed()
        for textbox in self.text_bindings:
            textbox.text_func(unicode, keys)

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

    def get_stage(self, stage_name):
        return self.stages[stage_name]

    def activate_custom_cursor(self):
        for stage in self.stages.values():
            if "custom_cursor" in stage.asset_dictionary.keys() and stage.state > -1:
                stage.set_viewable("custom_cursor")
                return

    def deactivate_custom_cursor(self):
        for stage in self.stages.values():
            if "custom_cursor" in stage.asset_dictionary.keys() and stage.state > -1:
                stage.unset_viewable("custom_cursor")
                return

    def add_text_binding(self, textbox):
        self.text_bindings.add(textbox)

    def remove_text_binding(self, textbox):
        if textbox in self.text_bindings:
            self.text_bindings.remove(textbox)

    def add_co_binding(self, clickable):
        self.click_off_bindings.add(clickable)

    def remove_co_binding(self, clickable):
        self.click_off_bindings.remove(clickable)

    def select_source_text_box(self) -> None:
        for stage in self.stages.values():
            if "source_text_box" in stage.asset_dictionary.keys() and stage.state > -1:
                stage.select_text_box("source_text_box")
                return

    def select_target_text_box(self) -> None:
        for stage in self.stages.values():
            if "target_text_box" in stage.asset_dictionary.keys() and stage.state > -1:
                stage.select_text_box("target_text_box")
                return

    def deselect_source_text_box(self) -> None:
        for stage in self.stages.values():
            if "source_text_box" in stage.asset_dictionary.keys() and stage.state > -1:
                stage.deselect_text_box("source_text_box")
                return

    def deselect_target_text_box(self) -> None:
        for stage in self.stages.values():
            if "target_text_box" in stage.asset_dictionary.keys() and stage.state > -1:
                stage.deselect_text_box("target_text_box")
                return

    def select_number_box(self) -> None:
        for stage in self.stages.values():
            if "number_box" in stage.asset_dictionary.keys() and stage.state > -1:
                stage.select_text_box("number_box")
                return

    def deselect_number_box(self) -> None:
        for stage in self.stages.values():
            if "number_box" in stage.asset_dictionary.keys() and stage.state > -1:
                stage.deselect_text_box("number_box")
                return

    def switch_search_mode(self) -> None:
        for stage in self.stages.values():
            if "mode_display_text" in stage.asset_dictionary.keys() and stage.state > -1:
                stage.swap_text("mode_display_text", 'BFS', 'Greedy')
                return

    def switch_uniqueness_mode(self) -> None:
        for stage in self.stages.values():
            if "uniqueness_enabled_text" in stage.asset_dictionary.keys() and stage.state > -1:
                stage.swap_text("uniqueness_enabled_text", 'Enabled', 'Disabled')
                return

    def get_source(self) -> Optional[str]:
        for stage in self.stages.values():
            if "source_text_box" in stage.asset_dictionary.keys() and stage.state > -1:
                source = stage.get_title_text("source_text_box")
                if source is None:
                    logging.warning("Failed to get source article title")
                else:
                    logging.info(f"Found source article title: \"{source}\"")
                return source
        logging.warning("Failed to find source_text_box text sprite in any stage")
        return None

    def get_target(self) -> Optional[str]:
        for stage in self.stages.values():
            if "target_text_box" in stage.asset_dictionary.keys() and stage.state > -1:
                target = stage.get_title_text("target_text_box")
                if target is None:
                    logging.warning("Failed to get target article title")
                else:
                    logging.info(f"Found target article title: \"{target}\"")
                return target
        logging.warning("Failed to find target_text_box text sprite in any stage")
        return None

    def get_search_breadth(self) -> Optional[int]:
        for stage in self.stages.values():
            if "number_box" in stage.asset_dictionary.keys() and stage.state > -1:
                number = stage.get_digit_text("number_box")
                if number is None:
                    logging.warning("Failed to get search depth")
                else:
                    logging.info(f"Found search depth: {number}")
                    number = int(number)
                return number
        logging.warning("Failed to find number_box text sprite in any stage")
        return None

    def get_word_weighting_mode(self) -> bool:
        for stage in self.stages.values():
            if "uniqueness_switch" in stage.asset_dictionary.keys() and stage.state > -1:
                weight_unique = stage.sprite_using_texture_name("uniqueness_switch", "switch_on.png")
                logging.info(f"Found word uniqueness weighting mode: {weight_unique}")
                return weight_unique
        logging.warning("Failed to find uniqueness_switch sprite in any stage")
        return None

    def get_search_algorithm(self) -> bool:
        for stage in self.stages.values():
            if "mode_display_text" in stage.asset_dictionary.keys() and stage.state > -1:
                mode = stage.get_text("mode_display_text")
                logging.info(f"Found word uniqueness weighting mode: {mode}")
                if mode == "BFS":
                    return True
                elif mode == "Greedy":
                    return False
                else:
                    return None
        logging.warning("Failed to find mode_display_text sprite in any stage")
        return None