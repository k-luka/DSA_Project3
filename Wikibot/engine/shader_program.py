import moderngl as mgl

class ShaderProgram:
    # Creates an object instance of the program for the GPU to run when rendering
    def __init__(self, ctx):
        self.ctx = ctx
        self.programs = {}

    def get_program(self, shader_program_name: str, directory:str) -> mgl.Program:
        with open(f'{directory}/shaders/{shader_program_name}.vert') as file:
            vertex_shader = file.read()

        with open(f'{directory}/shaders/{shader_program_name}.frag') as file:
            fragment_shader = file.read()

        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program

    def generate_program(self, name: str, directory: str) -> None:
        self.programs[name] = self.get_program(name, directory)

    def destroy(self):
        [program.release() for program in self.programs.values()]
