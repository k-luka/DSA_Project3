from ..app.asset import Sprite, SpriteCreateInfo
from .nodetype import NodeType
from typing import Union
import math


class LinkDrawings:
    source: Union[type[NodeType], NodeType]
    target: Union[type[NodeType], NodeType]
    body: Sprite
    head: Sprite

    def __init__(self, source: Union[type[NodeType], NodeType], target: Union[type[NodeType], NodeType]):
        self.source = source
        self.target = target
        source_x, source_y = source.get_scr_pos()
        target_x, target_y = target.get_scr_pos()
        avg_x = 0.5 * (source_x + target_x)
        avg_y = 0.5 * (source_y + target_y)
        difference_x = (target_x - source_x)
        difference_y = (target_y - source_y)
        unit_size = 5
        distance = math.hypot(difference_x, difference_y)
        length = distance - unit_size
        scale_x = length / unit_size

        body_create_info = SpriteCreateInfo(
            app=source.app,
            name=f"{source.title}_to_{target.title}_link_out_body",
            stage=source.sprite.stage,
            posPx=(round(avg_x), round(avg_y)),
            dimensionsPx=(unit_size, unit_size),
            scale=(scale_x, 1),
            kdfs=None,
            kufs=None,
            textures=["link_arrow_base.png"],
            haf=None,
            hdf=None,
            cafs=None,
            cdfs=None,
        )
        head_create_info = SpriteCreateInfo(
            app=source.app,
            name=f"{source.title}_to_{target.title}_link_out_head",
            stage=source.sprite.stage,
            posPx=(source_x + (length * difference_x / distance),
                   (source_y + (length * difference_y / distance))),
            dimensionsPx=(10, 10),
            scale=(1, 1),
            kdfs=None,
            kufs=None,
            textures=["link_arrow_head.png"],
            haf=None,
            hdf=None,
            cafs=None,
            cdfs=None,
        )
        self.body = Sprite(body_create_info)
        self.head = Sprite(head_create_info)
