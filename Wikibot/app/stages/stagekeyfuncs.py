from abc import ABC
from ..appinterface import AppInterface
from ..asset.sprite import Sprite, SpriteCreateInfo
import random
import math


class StageKeyFuncs(ABC):
    app: AppInterface
    asset_dictionary: dict
    test_objects: list[Sprite] = list()

    def quit(self, *args):
        self.app.quit()

    def add_node(self, *args):
        title = f"node_{len(self.asset_dictionary.keys())}"
        print(f"Adding node {title}")
        if self.app.get_graph_size() == 0:
            self.app.add_source_node(title)
        elif self.app.get_graph_size() == 1:
            self.app.add_target_node(title)
        else:
            self.app.add_node(title)

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
        if self.app.get_graph_size() < 2:
            self.add_node()
            return
        title = f"node_{len(self.asset_dictionary.keys())}"
        random_node_title = self.app.get_random_node_title()
        print(f"Adding node {title} with inlink from {random_node_title}")
        self.app.add_node_with_link(random_node_title, title)


