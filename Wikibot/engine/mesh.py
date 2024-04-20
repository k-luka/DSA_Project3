from .vao import VAO
from .texture import Texture


class Mesh:
    # Creates mesh object which stores rendering data
    def __init__(self, app):
        self.app = app
        self.vao = VAO(app.ctx)
        self.vbo = self.vao.vbo
        self.program = self.vao.program
        self.texture = Texture(app.ctx)

    def destroy(self):
        self.vao.destroy()
        self.texture.destroy()