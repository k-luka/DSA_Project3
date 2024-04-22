import logging
import pygame as pg
from dataclasses import dataclass
from .appinterface import AppInterface
from .mainloop import MainLoop
from Wikibot.engine.graphics import Graphics
from Wikibot.graph.graph import Graph
import random
from typing import Optional
from Wikibot.wikiapi.wikiAPI_functions import WikiApi


@dataclass()
class AppCreateInfo:
    win_size: int
    fps: int
    working_directory: str
    debug_level: int


class Application(AppInterface):
    graphics: Graphics
    mainloop: MainLoop
    graph: Graph
    wikiapi: Optional[WikiApi]
    running: bool
    appClock: pg.time.Clock

    def __init__(self, info: AppCreateInfo):
        pg.init()
        self.graphics = Graphics(info.win_size, info.fps, info.working_directory, info.debug_level)
        self.mainloop = MainLoop(self, info.fps, info.debug_level)
        self.mainloop.initialize_stages()
        # self.keys = AppKeys()
        # self.mouse = AppMouse()
        self.running = True
        self.appClock = pg.time.Clock()
        self.graph = Graph(self, "main_menu")
        self.wikiapi = None

    def add_key_down_binding(self, trigger, drawable) -> None:
        self.mainloop.add_kd_binding(trigger, drawable)

    def add_key_up_binding(self, trigger, drawable) -> None:
        self.mainloop.add_ku_binding(trigger, drawable)

    def add_mouse_down_binding(self, trigger, drawable) -> None:
        self.mainloop.add_md_binding(trigger, drawable)

    def add_mouse_up_binding(self, trigger, drawable) -> None:
        self.mainloop.add_mu_binding(trigger, drawable)

    def add_hover_activate_binding(self, hoverable) -> None:
        self.mainloop.add_ha_binding(hoverable)

    def add_hover_deactivate_binding(self, hoverable) -> None:
        self.mainloop.add_hd_binding(hoverable)

    def add_text_binding(self, textbox) -> None:
        self.mainloop.add_text_binding(textbox)

    def remove_key_down_binding(self, trigger, drawable) -> None:
        self.mainloop.remove_kd_binding(trigger, drawable)

    def remove_key_up_binding(self, trigger, drawable) -> None:
        self.mainloop.remove_ku_binding(trigger, drawable)

    def remove_mouse_down_binding(self, trigger, drawable) -> None:
        self.mainloop.remove_md_binding(trigger, drawable)

    def remove_mouse_up_binding(self, trigger, drawable) -> None:
        self.mainloop.remove_mu_binding(trigger, drawable)

    def remove_hover_activate_binding(self, hoverable) -> None:
        self.mainloop.remove_ha_binding(hoverable)

    def remove_hover_deactivate_binding(self, hoverable) -> None:
        self.mainloop.add_hd_binding(hoverable)

    def remove_text_binding(self, textbox) -> None:
        self.mainloop.remove_text_binding(textbox)

    def list_bounded_object(self, bounded_object) -> None:
        self.mainloop.add_bounded_object(bounded_object)

    def delist_bounded_object(self, bounded_object) -> None:
        self.mainloop.remove_bounded_object(bounded_object)

    def add_static_drawable(self, drawable) -> None:
        self.mainloop.add_static_drawable(drawable)

    def remove_static_drawable(self, drawable) -> None:
        self.mainloop.remove_static_drawable(drawable)

    def append_model_to_scene(self, model) -> None:
        self.graphics.scene.add_object(model)

    def insert_model_into_scene(self, layer, model) -> None:
        self.graphics.scene.insert(layer, model)

    def get_model_layer(self, model) -> int:
        return self.graphics.scene.objects.index(model)

    def set_model_in(self, layer: int, model):
        self.graphics.scene.objects[layer] = model

    def scene_object_count(self) -> int:
        return len(self.graphics.scene.objects)

    def remove_model_from_scene(self, model) -> None:
        self.graphics.scene.remove_object(model)

    def add_render_program(self, program) -> None:
        if program not in self.graphics.mesh.program.programs:
            self.graphics.mesh.program.generate_program(program, self.graphics.directory)

    def add_texture(self, texture) -> None:
        if texture not in self.graphics.mesh.texture.textures:
            self.graphics.mesh.texture.generate_texture(texture, self.graphics.directory)

    def regenerate_vbo(self, vbo_name, vbo_type, scaled_width, scaled_height) -> None:
        # Create new VBO fork, delete old one if necessary
        if vbo_name in self.graphics.mesh.vbo.vbos:
            del self.graphics.mesh.vbo.vbos[vbo_name]
            logging.info(f' Replacing VBO \'{vbo_name}\'')
        self.graphics.mesh.vbo.generate_vbo(vbo_name, vbo_type, scaled_width, scaled_height)

    def regenerate_vao(self, vao_name, vbo_name, program_name) -> None:
        # Create new VAO fork, delete old one if necessary
        if vao_name in self.graphics.mesh.vao.vaos:
            del self.graphics.mesh.vao.vaos[vao_name]
            logging.info(f' Replacing VAO \'{vao_name}\'')
        self.graphics.mesh.vao.generate_vao(name=vao_name, vbo_name=vbo_name, program_name=program_name)

    def add_text_texture(self, texture, size, color, text, background) -> None:
        if texture not in self.graphics.mesh.texture.textures:
            self.graphics.mesh.texture.generate_texture_txt(texture, size, color, text, background)

    def win_size(self) -> tuple[int, int]:
        return self.graphics.WIN_SIZE

    def add_sprite_to_stage(self, sprite, stage, make_viewable: bool = False) -> None:
        self.mainloop.add_sprite_to_stage(sprite, stage, make_viewable)

    def add_node(self, node_title) -> None:
        self.graph.add_node(node_title)

    def add_link(self, source_node_title, target_node_title) -> None:
        self.graph.add_link(source_node_title, target_node_title)

    def add_node_with_link(self, source_node_title, target_node_title) -> None:
        self.graph.add_node_with_in_link(source_node_title, target_node_title)

    def get_stage(self, stage_name):
        return self.mainloop.get_stage(stage_name)

    def add_source_node(self, source_node_title) -> None:
        self.graph.add_source_node(source_node_title)

    def add_target_node(self, target_node) -> None:
        self.graph.add_target_node(target_node)

    def get_graph_size(self) -> int:
        return len(self.graph.nodes)

    def get_random_node_title(self) -> str:
        random_title_index = random.randint(0, self.get_graph_size() - 2)
        random_title = [title for title in self.graph.nodes if title != "node_1"][random_title_index]
        return random_title

    def switch_cursor_to_custom(self):
        pg.mouse.set_visible(False)
        self.mainloop.activate_custom_cursor()

    def switch_cursor_to_normal(self):
        pg.mouse.set_visible(True)
        self.mainloop.deactivate_custom_cursor()

    def add_click_off_binding(self, clickable) -> None:
        self.mainloop.add_co_binding(clickable)

    def remove_click_off_binding(self, clickable) -> None:
        self.mainloop.remove_co_binding(clickable)

    def get_texture(self, texture_name) -> pg.Surface:
        return self.graphics.mesh.texture.textures[texture_name]

    def select_source_text_box(self) -> None:
        self.mainloop.select_source_text_box()

    def select_target_text_box(self) -> None:
        self.mainloop.select_target_text_box()

    def deselect_source_text_box(self) -> None:
        self.mainloop.deselect_source_text_box()

    def deselect_target_text_box(self) -> None:
        self.mainloop.deselect_target_text_box()

    def select_number_box(self) -> None:
        self.mainloop.select_number_box()

    def deselect_number_box(self) -> None:
        self.mainloop.deselect_number_box()

    def switch_search_mode(self) -> None:
        self.mainloop.switch_search_mode()

    def switch_uniqueness_mode(self) -> None:
        self.mainloop.switch_uniqueness_mode()

    def generate_api(self) -> None:
        self.reset()
        source_article = self.get_source()
        target_article = self.get_target()
        search_breadth = self.get_search_breadth()
        unique_word_weighting = self.get_word_weighting_mode()
        algorithm_is_bfs = self.get_search_algorithm()
        if source_article is None or target_article is None or search_breadth is None: return
        self.wikiapi = WikiApi(source_article, target_article, unique_word_weighting, search_breadth, algorithm_is_bfs)
        self.wikiapi.search()
        adjacency_list: dict[str, list[str]] = self.wikiapi.get_adjacency_list()
        proper_source_title = self.wikiapi.get_source_page_title()
        proper_target_title = self.wikiapi.get_target_page_title()
        self.construct_graph_from_adjacency_list(proper_source_title, proper_target_title, adjacency_list)
        path_length: Optional[int] = self.wikiapi.get_length_of_path()
        if path_length is not None:
            self.mainloop.set_path_length_display_text(path_length)
        pages_visited: int = self.wikiapi.get_number_of_visited_sites()
        self.mainloop.set_visited_pages_display_text(pages_visited)
        path: Optional[list[str]] = self.wikiapi.trace_path_backwards()
        if path is not None:
            print(f"\nSuccessfully found a path from the Wikipedia article \"{proper_source_title}\" to the article \"{proper_target_title}\":")
            [print('\"' + title + '\"' + ' to ', '') for title in path[:-1]]
            print(f"\"{path[len(path) - 1]}\"")
            self.graph.highlight_path(path)
        else:
            print(f"\nFailed to find a path from the Wikipedia article \"{proper_source_title}\" to the article \"{proper_target_title}\"")

    def get_source(self) -> Optional[str]:
        return self.mainloop.get_source()

    def get_target(self) -> Optional[str]:
        return self.mainloop.get_target()

    def get_search_breadth(self) -> Optional[int]:
        return self.mainloop.get_search_breadth()

    def get_word_weighting_mode(self) -> bool:
        return self.mainloop.get_word_weighting_mode()

    def get_search_algorithm(self) -> bool:
        return self.mainloop.get_search_algorithm()

    def construct_graph_from_adjacency_list(self, source_article: str,
                                            target_article: str,
                                            adjacency_list: dict[str, list[str]]) -> None:
        self.graph.construct_from_adjacency_list(source_article, target_article, adjacency_list)

    def remove_sprite_from_stage(self, sprite, stage) -> None:
        self.mainloop.remove_sprite_from_stage(sprite, stage)

    def reset(self) -> None:
        self.wikiapi = None
        self.graph.clear()
        self.mainloop.reset()

    def quit(self) -> None:
        self.running = False

    def run(self) -> None:
        while self.running:
            self.mainloop.execute()
            self.appClock = pg.time.Clock()
