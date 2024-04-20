import pygame as pg
from abc import ABC, abstractmethod
from ..appinterface import AppInterface
from Wikibot.graph.node import Node, NodeCreateInfo
import random


class StageKeyFuncs(ABC):
    app: AppInterface
    asset_dictionary: dict
    nodes: list[Node] = list()

    def quit(self, *args):
        self.app.quit()

    def add_node(self):
        create_info = NodeCreateInfo(
            app=self.app,
            title=f"node_{len(self.asset_dictionary.keys())}",
            stage=self,
            pos=(random.randint(0, 900), random.randint(0, 600)),
        )
        self.nodes.append(Node(create_info))

