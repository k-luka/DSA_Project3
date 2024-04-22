from __future__ import annotations
from dataclasses import dataclass
from ..app.appinterface import AppInterface
from ..app.asset.sprite import Sprite, SpriteCreateInfo
from typing import Union
from .link import Link, LinkCreateInfo
from .nodetype import NodeType
import logging


@dataclass()
class NodeCreateInfo:
    app: Union[type[AppInterface], AppInterface]
    title: str
    stage: ...
    center: tuple[float, float]
    indices: tuple[int, int]


class Node(NodeType):
    app: Union[type[AppInterface], AppInterface]
    stage: ...
    title: str
    position: tuple[float, float]
    position_center: tuple[float, float]
    size: Union[int, float] = 10
    out_links: set[Node] = set()
    out_link_drawings: set[Link] = set()
    in_links: set[Node] = set()
    sprite: Sprite
    indices: tuple[int, int]
    grid_neighbors: list[Node] = list()

    def __init__(self, info: NodeCreateInfo):
        self.title = info.title
        self.app = info.app
        self.stage = info.stage
        self.position_center = info.center
        self.position = (self.position_center[0] - self.size * 0.5, self.position_center[1] - self.size * 0.5)
        self.indices = info.indices
        self.color = "gray"
        sprite_create_info = SpriteCreateInfo(
            app=info.app,
            name=f"{info.title}_wiki_page",
            stage=info.stage,
            posPx=(self.position[0], self.position[1]),
            dimensionsPx=(self.size, self.size),
            scale=(1, 1),
            kdfs=None,
            kufs=None,
            textures=["node_gray.png", "node_red.png", "node_green.png", "node_blue.png"],
            haf=None,
            hdf=None,
            cafs=None,
            cdfs=None,
        )
        self.sprite = Sprite(sprite_create_info)
        self.app.add_sprite_to_stage(self.sprite, info.stage, make_viewable=True)

    def add_link_out(self, linked_node: Node):
        self.out_links.add(linked_node)
        link_info = LinkCreateInfo(self, linked_node)
        self.out_link_drawings.add(Link(link_info))

    def add_neighbor(self, coordinates):
        self.grid_neighbors.append(coordinates)

    def add_link_in(self, link: Node):
        self.in_links.add(link)

    def get_scr_pos(self) -> tuple[float, float]:
        return self.sprite.posPx

    def get_center(self) -> tuple[float, float]:
        return self.position_center

    def destroy(self):
        # print(f"Destroying node {self.title}")
        self.app.remove_sprite_from_stage(self.sprite, self.stage)
        for link in self.out_link_drawings:
            link.destroy()
        self.out_link_drawings = set()

    def set_color(self, color: str):
        if color == "gray":
            self.sprite.switch_to_texture(0)
        elif color == "red":
            self.sprite.switch_to_texture(1)
        elif color == "green":
            self.sprite.switch_to_texture(2)
        elif color == "blue":
            self.sprite.switch_to_texture(3)
        else:
            logging.warning(f"Failed to switch node \'{self.title}\' to color \'{color}\': Color is not valid")

    def highlight_link_to(self, node: Node):
        for link in self.out_link_drawings:
            if link.target == node:
                link.highlight()
                return
        logging.warning(f"Failed to highlight link between node \'{self.title}\' and node \'{node.title}\'")
