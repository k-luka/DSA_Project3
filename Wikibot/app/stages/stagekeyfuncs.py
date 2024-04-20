import pygame as pg
from abc import ABC
from ..appinterface import AppInterface
from Wikibot.graph.node import Node, NodeCreateInfo
from ..asset.sprite import Sprite, SpriteCreateInfo
import random
import math


class StageKeyFuncs(ABC):
    app: AppInterface
    asset_dictionary: dict
    nodes: list[Node] = list()
    test_objects: list[Sprite] = list()

    def quit(self, *args):
        self.app.quit()

    def add_node(self, *args):
        position = (random.randint(0, 900), random.randint(0, 600))
        if len(self.nodes) == 0:
            position = (450, 300)
        create_info = NodeCreateInfo(
            app=self.app,
            title=f"node_{len(self.asset_dictionary.keys())}",
            stage=self,
            center=position,
        )
        self.nodes.append(Node(create_info))

    def add_test_image(self, *args):
        create_info = SpriteCreateInfo(
            app=self.app,
            name=f"test_asset_{len(self.asset_dictionary.keys())}",
            stage=self,
            posPx=(random.randint(0, 900), random.randint(0, 600)),
            dimensionsPx=(50, 50),
            scale=(1, 1),
            rot=random.uniform(0, 2 * math.pi),
            kdfs=None,
            kufs=None,
            textures=["test.png"],
            haf=None,
            hdf=None,
            cafs=None,
            cdfs=None
        )
        test_sprite = Sprite(create_info)
        self.test_objects.append(test_sprite)
        self.app.add_sprite_to_stage(test_sprite, self, make_viewable=True)

    def add_node_with_link(self, *args):
        if len(self.nodes) == 0:
            self.add_node()
            return
        create_info = NodeCreateInfo(
            app=self.app,
            title=f"node_{len(self.asset_dictionary.keys())}",
            stage=self,
            center=(random.randint(0, 900), random.randint(0, 600)),
        )
        new_node = Node(create_info)
        if len(self.nodes) > 0:
            random_node_index = random.randint(0, len(self.nodes) - 1)
            self.nodes[random_node_index].add_link_out(new_node)
        self.nodes.append(new_node)


