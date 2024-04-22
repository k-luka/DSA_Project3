from ..app.asset.sprite import Sprite, SpriteCreateInfo
from .nodetype import NodeType
from typing import Union
import math
import math
from ..app.appinterface import AppInterface
from typing import Union
from dataclasses import dataclass


@dataclass()
class LinkCreateInfo:
    source: Union[type[NodeType], NodeType]
    target: Union[type[NodeType], NodeType]


class Link:
    app: Union[type[AppInterface], AppInterface]
    stage: ...
    source: Union[type[NodeType], NodeType]
    target: Union[type[NodeType], NodeType]
    body: Sprite
    head: Sprite

    def __init__(self, info: LinkCreateInfo):
        # Get info from create info
        self.app = info.source.app
        self.stage = info.source.stage
        self.source = info.source
        self.target = info.target
        # Get source center coordinates and difference vector
        source_x, source_y = self.source.get_center()
        target_x, target_y = self.target.get_center()
        difference_x = (target_x - source_x)
        difference_y = (target_y - source_y)
        # Set unit size, head ratio, and target separation distance
        unit_size = 2
        head_ratio = 3
        target_sep_dist = 6
        # Compute arrow width/height based on unit_size and difference vector
        distance = math.hypot(difference_x, difference_y)
        length = distance - target_sep_dist * unit_size
        scale_x = length / unit_size

        half_width = 0.5 * length
        half_height = 0.5 * unit_size
        # Important geometric values for position correction calculation
        arrow_angle = math.atan2(-difference_y, difference_x)
        arrow_f_cos = 1 - math.cos(arrow_angle)
        arrow_sin = math.sin(arrow_angle)
        # Position correction calculation (moves top-left corner to source node's center)
        dx = (half_height * arrow_sin) - (half_width * arrow_f_cos)
        dy = (half_width * arrow_sin) + (half_height * arrow_f_cos)
        # Little (l) position correction calculation (aligns the middle of the arrow's left edge to the source node's center
        arrow_perp = arrow_angle + (math.pi * 0.5)
        ldx = half_height * math.cos(arrow_perp)
        ldy = half_height * math.sin(arrow_perp)
        # Arrow position computation
        body_position = (source_x + dx + ldx, source_y - dy - ldy)
        # Arrow body information
        body_create_info = SpriteCreateInfo(
            app=self.app,
            name=f"{self.source.title}_to_{self.target.title}_link_out_body",
            stage=self.source.stage,
            posPx=body_position,
            dimensionsPx=(unit_size, unit_size),
            scale=(scale_x, 1),
            rot = arrow_angle,
            kdfs=None,
            kufs=None,
            textures=["link_arrow_base.png", "link_arrow_base_highlight.png"],
            haf=None,
            hdf=None,
            cafs=None,
            cdfs=None,
        )
        # Correction factors for arrow head
        head_inital_x = source_x + (length * difference_x / distance)
        head_inital_y = source_y + (length * difference_y / distance)
        # Settings width/height vars (arrow png is a square of 2 * unit_size by 2 * unit_size)
        half_width = 0.5 * head_ratio * unit_size
        half_height = 0.5 * head_ratio * unit_size
        # Major correct factor
        dx = (half_height * arrow_sin) - (half_width * arrow_f_cos)
        dy = (half_width * arrow_sin) + (half_height * arrow_f_cos)
        # Minor correction factor
        ldx = half_height * math.cos(arrow_perp)
        ldy = half_height * math.sin(arrow_perp)
        # Get arrow head position
        head_position = (head_inital_x + dx + ldx, head_inital_y - dy - ldy)
        head_create_info = SpriteCreateInfo(
            app=self.app,
            name=f"{self.source.title}_to_{self.target.title}_link_out_head",
            stage=self.source.stage,
            posPx=head_position,
            dimensionsPx=(head_ratio * unit_size, head_ratio * unit_size),
            scale=(1, 1),
            rot = arrow_angle,
            kdfs=None,
            kufs=None,
            textures=["link_arrow_head.png", "link_arrow_head_highlight.png"],
            haf=None,
            hdf=None,
            cafs=None,
            cdfs=None,
        )
        self.body = Sprite(body_create_info)
        self.head = Sprite(head_create_info)
        self.app.add_sprite_to_stage(self.body, self.stage, make_viewable=True)
        self.app.add_sprite_to_stage(self.head, self.stage, make_viewable=True)

    def destroy(self):
        # print(f"Destroying link between {self.source.title} and {self.target.title}")
        self.app.remove_sprite_from_stage(self.body, self.stage)
        self.app.remove_sprite_from_stage(self.head, self.stage)

    def highlight(self):
        self.head.switch_to_texture(1)
        self.body.switch_to_texture(1)
