import logging
from abc import ABC, abstractmethod
from Wikibot.engine.graphics import Graphics
from typing import Optional
import pygame as pg

class AppInterface(ABC):
    graphics: Graphics

    @abstractmethod
    def add_key_down_binding(self, trigger, drawable) -> None: pass

    @abstractmethod
    def add_key_up_binding(self, trigger, drawable) -> None: pass

    @abstractmethod
    def add_mouse_down_binding(self, trigger, clickable) -> None: pass

    @abstractmethod
    def add_mouse_up_binding(self, trigger, clickable) -> None: pass

    @abstractmethod
    def add_hover_activate_binding(self, hoverable) -> None: pass

    @abstractmethod
    def add_hover_deactivate_binding(self, hoverable) -> None: pass

    @abstractmethod
    def remove_key_down_binding(self, trigger, drawable) -> None: pass

    @abstractmethod
    def remove_key_up_binding(self, trigger, drawable) -> None: pass

    @abstractmethod
    def remove_mouse_down_binding(self, trigger, clickable) -> None: pass

    @abstractmethod
    def remove_mouse_up_binding(self, trigger, clickable) -> None: pass

    @abstractmethod
    def remove_hover_activate_binding(self, hoverable) -> None: pass

    @abstractmethod
    def remove_hover_deactivate_binding(self, hoverable) -> None: pass

    @abstractmethod
    def list_bounded_object(self, bounded_object) -> None: pass

    @abstractmethod
    def delist_bounded_object(self, bounded_object) -> None: pass

    @abstractmethod
    def add_static_drawable(self, drawable) -> None: pass

    @abstractmethod
    def remove_static_drawable(self, drawable) -> None: pass

    @abstractmethod
    def append_model_to_scene(self, model) -> None: pass

    @abstractmethod
    def insert_model_into_scene(self, layer, model) -> None: pass

    @abstractmethod
    def get_model_layer(self, model) -> int: pass

    @abstractmethod
    def set_model_in(self, layer: int, model) -> None: pass

    @abstractmethod
    def scene_object_count(self) -> int: pass

    @abstractmethod
    def remove_model_from_scene(self, model) -> None: pass

    @abstractmethod
    def win_size(self) -> tuple[int, int]: pass

    @abstractmethod
    def add_render_program(self, program) -> None: pass

    @abstractmethod
    def add_texture(self, texture) -> None: pass

    @abstractmethod
    def regenerate_vbo(self, vbo_name, vbo_type, scaled_width, scaled_height) -> None: pass

    @abstractmethod
    def regenerate_vao(self, vao_name, vbo_name, program_name) -> None: pass

    @abstractmethod
    def add_text_texture(self, texture, size, color, text, background) -> None: pass

    @abstractmethod
    def quit(self) -> None: pass

    @abstractmethod
    def run(self) -> None: pass

    @abstractmethod
    def add_sprite_to_stage(self, sprite, stage, make_viewable: bool = False) -> None: pass

    @abstractmethod
    def add_node(self, node) -> None: pass

    @abstractmethod
    def add_link(self, source_node_title, target_node_title) -> None: pass

    @abstractmethod
    def add_node_with_link(self, source_node_title, target_node) -> None: pass

    @abstractmethod
    def add_source_node(self, source_node_title) -> None: pass

    @abstractmethod
    def add_target_node(self, target_node) -> None: pass

    @abstractmethod
    def get_stage(self, stage_name): pass

    @abstractmethod
    def get_graph_size(self) -> int: pass

    @abstractmethod
    def get_random_node_title(self) -> str: pass

    @abstractmethod
    def switch_cursor_to_custom(self) -> None: pass

    @abstractmethod
    def switch_cursor_to_normal(self) -> None: pass

    @abstractmethod
    def add_text_binding(self, textbox) -> None: pass

    @abstractmethod
    def remove_text_binding(self, textbox) -> None: pass

    @abstractmethod
    def add_click_off_binding(self, clickable) -> None: pass

    @abstractmethod
    def remove_click_off_binding(self, clickable) -> None: pass

    @abstractmethod
    def get_texture(self, texture_name) -> pg.Surface: pass

    @abstractmethod
    def select_source_text_box(self) -> None: pass

    @abstractmethod
    def select_target_text_box(self) -> None: pass

    @abstractmethod
    def deselect_source_text_box(self) -> None: pass

    @abstractmethod
    def deselect_target_text_box(self) -> None: pass

    @abstractmethod
    def select_number_box(self) -> None: pass

    @abstractmethod
    def deselect_number_box(self) -> None: pass

    @abstractmethod
    def switch_search_mode(self) -> None: pass

    @abstractmethod
    def switch_uniqueness_mode(self) -> None: pass

    @abstractmethod
    def generate_api(self) -> None: pass

    @abstractmethod
    def get_source(self) -> Optional[str]: pass

    @abstractmethod
    def get_target(self) -> Optional[str]: pass

    @abstractmethod
    def get_search_breadth(self) -> Optional[int]: pass

    @abstractmethod
    def get_word_weighting_mode(self) -> bool: pass

    @abstractmethod
    def get_search_algorithm(self) -> bool: pass

    @abstractmethod
    def construct_graph_from_adjacency_list(self, source_article, target_article, adjacency_list) -> None: pass

    @abstractmethod
    def reset(self) -> None: pass

    @abstractmethod
    def remove_sprite_from_stage(self, sprite, stage) -> None: pass

