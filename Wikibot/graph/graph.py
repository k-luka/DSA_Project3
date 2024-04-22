from .node import Node, NodeCreateInfo
from ..app.appinterface import AppInterface
from .graphtype import GraphType
from typing import Union
import math
import random


class Graph(GraphType):
    app: Union[type[AppInterface], AppInterface] = None
    stage: ...
    node_indices: dict[tuple[int, int], Node] = dict()
    nodes: dict[str, Node] = dict()
    offset: tuple[float, float] = None
    node_region_radius: float = 15
    grid_transform_scale: tuple[float, float] = (1.5, 0.5 * math.sqrt(3))
    grid_min_x: int = None
    grid_max_x: int = None
    grid_min_y: int = None
    grid_max_y: int = None
    source_node: Node
    target_node: Node

    def __init__(self, app: Union[type[AppInterface], AppInterface], stage_name):
        self.app = app
        self.stage = app.get_stage(stage_name)
        scr_x, scr_y = app.win_size()
        max_dix = scr_x / (self.node_region_radius * self.grid_transform_scale[0])
        self.grid_max_x = round(max_dix)
        self.grid_min_x = 0
        max_diy = scr_y / (self.node_region_radius * self.grid_transform_scale[1])
        self.grid_max_y = round(max_diy)
        self.grid_min_y = 0
        
    def generate_source_node_indices(self):
        return self.round_scr_coords(
            self.app.win_size()[0] * 0.1,
            self.app.win_size()[1] * 0.5
        )

    def generate_target_node_indices(self):
        return self.round_scr_coords(
            self.app.win_size()[0] * 0.9,
            self.app.win_size()[1] * 0.5
        )

    def generate_random_indices(self):
        init_x = None
        init_y = None
        while (init_x is None or init_y is None) or ((init_x, init_y) in self.node_indices.keys()):
            init_x = random.randint(self.grid_min_x, self.grid_max_x)
            init_y = random.randint(self.grid_min_y, self.grid_max_y)
            if (init_x + init_y) % 2:
                direction_shift = random.randint(0, 3)
                if direction_shift == 0:
                    init_x += 1
                elif direction_shift == 1:
                    init_y += 1
                elif direction_shift == 2:
                    init_x -= 1
                else:
                    init_y -= 1
        return init_x, init_y
        
    def round_scr_coords(self, coord_x, coord_y):
        index_x = round(coord_x / (self.node_region_radius * self.grid_transform_scale[0]))
        index_y = round(coord_y / (self.node_region_radius * self.grid_transform_scale[1]))
        if (index_x + index_y) % 2:
            index_x += 1
        return index_x, index_y

    def get_position_from_grid_coordinates(self, coordinates):
        return (coordinates[0] * self.node_region_radius * self.grid_transform_scale[0],
                coordinates[1] * self.node_region_radius * self.grid_transform_scale[1])

    def inform_grid_neighbors(self, from_node, coordinates):
        up_right = (coordinates[0] + 1, coordinates[1] - 1)
        up = (coordinates[0], coordinates[1] - 2)
        up_left = (coordinates[0] - 1, coordinates[1] - 1)
        down_left = (coordinates[0] - 1, coordinates[1] + 1)
        down = (coordinates[0], coordinates[1] + 2)
        down_right = (coordinates[0] + 1, coordinates[1] + 1)
        coords_to_check = [up_right, up, up_left, down_left, down, down_right]
        for coords in coords_to_check:
            if coords in self.node_indices.keys():
                self.node_indices[coords].add_neighbor(coordinates)
                from_node.add_neighbor(coords)

    def add_node(self, node_title):
        new_node_indices = self.generate_random_indices()
        new_node_coords = self.get_position_from_grid_coordinates(new_node_indices)
        create_info = NodeCreateInfo(
            app=self.app,
            title=node_title,
            stage=self.stage,
            center=new_node_coords,
            indices=new_node_indices
        )
        new_node = Node(create_info)
        self.nodes[node_title] = new_node
        self.node_indices[new_node_indices] = new_node
        self.inform_grid_neighbors(self.target_node, new_node_indices)

    def generate_indices_near(self, node_title):
        search_order = 2 * random.randint(0, 1) - 1
        root_node = self.nodes[node_title]
        ring = 1
        x_distance = 1
        y_distance = 1
        while True:
            result = self.explore_ring(ring, x_distance, y_distance,
                                       root_node.indices,
                                       root_node.grid_neighbors)
            if result is not None:
                return result
            ring += 1
            x_distance = ring
            y_distance = (x_distance % 2) * search_order

    @staticmethod
    def explore_ring(ring, x_distance, y_distance, center_indices, neighbors):
        # Search right edge
        for i in range(ring):
            result_index = (center_indices[0] + x_distance, center_indices[1] + y_distance)
            if result_index not in neighbors:
                return result_index
            y_distance *= -1
            result_index = (center_indices[0] + x_distance, center_indices[1] + y_distance)
            if result_index not in neighbors:
                return result_index
            y_distance *= -1
            y_distance += math.copysign(2, y_distance)
        # Search top/bottom right edge
        x_distance -= 1
        y_distance -= math.copysign(1, y_distance)
        for i in range(ring):
            result_index = (center_indices[0] + x_distance, center_indices[1] + y_distance)
            if result_index not in neighbors:
                return result_index
            y_distance *= -1
            result_index = (center_indices[0] + x_distance, center_indices[1] + y_distance)
            if result_index not in neighbors:
                return result_index
            y_distance *= -1
            x_distance -= 1
            y_distance += math.copysign(1, y_distance)
        # Search top/bottom left edge
        y_distance -= math.copysign(2, y_distance)
        for i in range(ring):
            result_index = (center_indices[0] + x_distance, center_indices[1] + y_distance)
            if result_index not in neighbors:
                return result_index
            y_distance *= -1
            result_index = (center_indices[0] + x_distance, center_indices[1] + y_distance)
            if result_index not in neighbors:
                return result_index
            y_distance *= -1
            x_distance -= 1
            y_distance -= math.copysign(1, y_distance)
        # Search left edge
        x_distance += 1
        y_distance -= math.copysign(1, y_distance)
        for i in range(ring - 1):
            result_index = (center_indices[0] + x_distance, center_indices[1] + y_distance)
            if result_index not in neighbors:
                return result_index
            y_distance *= -1
            result_index = (center_indices[0] + x_distance, center_indices[1] + y_distance)
            if result_index not in neighbors:
                return result_index
            y_distance *= -1
            y_distance -= math.copysign(2, y_distance)
        return None

    def add_link(self, source_node, target_node):
        self.nodes[source_node].add_link_out(self.nodes[target_node])

    def add_node_with_in_link(self, source_node, new_node_title):
        new_node_indices = self.generate_indices_near(source_node)
        new_node_coords = self.get_position_from_grid_coordinates(new_node_indices)
        create_info = NodeCreateInfo(
            app=self.app,
            title=new_node_title,
            stage=self.stage,
            center=new_node_coords,
            indices=new_node_indices
        )
        new_node = Node(create_info)
        self.nodes[new_node_title] = new_node
        self.node_indices[new_node_indices] = new_node
        self.nodes[source_node].add_link_out(self.nodes[new_node_title])
        self.inform_grid_neighbors(self.target_node, new_node_indices)
        
    def add_source_node(self, node_title):
        source_node_indices = self.generate_source_node_indices()
        source_node_coords = self.get_position_from_grid_coordinates(source_node_indices)
        create_info = NodeCreateInfo(
            app=self.app,
            title=node_title,
            stage=self.stage,
            center=source_node_coords,
            indices=source_node_indices
        )
        self.source_node = Node(create_info)
        self.nodes[node_title] = self.source_node
        self.node_indices[source_node_indices] = self.source_node
        self.inform_grid_neighbors(self.source_node, source_node_indices)
        
    def add_target_node(self, node_title):
        target_node_indices = self.generate_target_node_indices()
        print(f"Adding target node at {target_node_indices}")
        target_node_coords = self.get_position_from_grid_coordinates(target_node_indices)
        print(f"Target coordinates: {target_node_coords}")
        create_info = NodeCreateInfo(
            app=self.app,
            title=node_title,
            stage=self.stage,
            center=target_node_coords,
            indices=target_node_indices
        )
        self.target_node = Node(create_info)
        self.nodes[node_title] = self.target_node
        self.node_indices[target_node_indices] = self.target_node
        self.inform_grid_neighbors(self.target_node, target_node_indices)

    def construct_from_adjacency_list(self, adjacency_list):
        pass