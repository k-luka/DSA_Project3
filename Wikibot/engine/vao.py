from .vbo import VBO
from .shader_program import ShaderProgram


class VAO:
    # Vertex array object, stores vertices for triangles to be used in rendering
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = VBO(ctx)
        self.program = ShaderProgram(ctx)
        self.vaos = {}

    def get_vao(self, program, vbo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attributes)])
        return vao

    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()

    def generate_vao(self, name, program_name, vbo_name):
        # Generate VAO if VAO not in vaos
        self.vaos[name] = self.get_vao(program=self.program.programs[program_name],
                                       vbo=self.vbo.vbos[vbo_name])
