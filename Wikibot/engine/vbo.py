import numpy as np
from typing import Union


class VBO:
    # Vertex buffer object, determines how corner indices are to be treated and passed to the GPU
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbos = {}

    def destroy(self):
        [vbo.destroy() for vbo in self.vbos.values()]

    def generate_vbo(self, name, VBO_class, *args):
        self.vbos[name] = VBO_class(self.ctx, *args)


class BaseVBO:
    def __init__(self, ctx, *vbo_args):
        self.ctx = ctx
        self.vbo = self.get_vbo(vbo_args)
        self.format: str = None
        self.attrib: list = None

    def get_vertex_data(self): ...

    def get_vbo(self, vbo_args) -> None:
        vertex_data = self.get_vertex_data(*vbo_args)
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def destroy(self):
        self.vbo.release()


class GUI_VBO(BaseVBO):
    def __init__(self, ctx, px_width: Union[float, int], px_height: Union[float, int]):
        super().__init__(ctx, px_width, px_height)
        self.format = '2f 3f'
        self.attributes = ['in_texture_coord_0', 'in_position']

    @staticmethod
    def get_data(vertices: Union[list[tuple[float, ...], ...], list[tuple[int, ...], ...]],
                 indices: list[tuple[int, ...], ...]) -> np.array:

        data = [vertices[index] for triangle in indices for index in triangle]
        return np.array(data, dtype='f4')

    def get_vertex_data(self, px_width: Union[float, int], px_height: Union[float, int]):
        vertices = [(-1.0 * px_width, -1.0 * px_height, 0.0),
                    (1.0 * px_width, -1.0 * px_height, 0.0),
                    (1.0 * px_width, 1.0 * px_height, 0.0),
                    (-1.0 * px_width, 1.0 * px_height, 0.0)]
        indices = [(0, 2, 3), (0, 1, 2)]

        vertex_data = self.get_data(vertices, indices)

        texture_vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]
        texture_indices = [(0, 2, 3), (0, 1, 2)]

        texture_data = self.get_data(texture_vertices, texture_indices)

        vertex_data = np.hstack([texture_data, vertex_data])
        return vertex_data
