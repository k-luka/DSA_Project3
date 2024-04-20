from Wikibot.engine.graphics import Graphics
from .mainloop import MainLoop
from dataclasses import dataclass
import pygame as pg
from .appinterface import AppInterface
import logging

@dataclass()
class AppCreateInfo:
    win_size: int
    fps: int
    working_directory: str
    debug_level: int

class Application(AppInterface):
    graphics: Graphics
    mainloop: MainLoop
    # keys: AppKeys
    # mouse: AppMouse
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

    def quit(self) -> None:
        self.running = False

    def run(self) -> None:
        while self.running:
            self.mainloop.execute()
            self.appClock = pg.time.Clock()
