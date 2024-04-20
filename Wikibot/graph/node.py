from __future__ import annotations
from ..app.asset import Sprite, SpriteCreateInfo
from ..app.appinterface import AppInterface
from typing import Union
from .LinkDrawings import LinkDrawings
from .nodetype import NodeType


class NodeCreateInfo:
    app: Union[type[AppInterface], AppInterface]
    title: str
    stage: ...
    position: tuple[float, float]


class Node(NodeType):
    title: str
    out_links: set[Node] = set()
    out_link_drawings: set[LinkDrawings]
    in_links: set[Node] = set()
    sprite: Sprite

    def __init__(self, info: NodeCreateInfo):
        self.title = info.title
        self.app = info.app
        sprite_create_info = SpriteCreateInfo(
            app=info.app,
            name=f"{info.title}_wiki_page",
            stage=info.stage,
            posPx=(info.position[0], info.position[1]),
            dimensionsPx=(15, 15),
            scale=(1, 1),
            kdfs=None,
            kufs=None,
            textures=["node.png, node_highlight.png"],
            haf='switch_to_secondary_texture',
            hdf='switch_to_default_texture',
            cafs=None,
            cdfs=None,
        )
        self.sprite = Sprite(sprite_create_info)
        self.app.add_sprite_to_stage(self.sprite, info.stage)

    def add_link_out(self, link: Node):
        self.out_links.add(link)
        self.out_link_drawings.add(LinkDrawings(self, link))

    def add_link_in(self, link: Node):
        self.in_links.add(link)

    def get_scr_pos(self) -> tuple[float, float]:
        return self.sprite.posPx
