import glm


class BaseModel2D:
    def __init__(self, app, vao_name, texture_name,
                 pos=(0, 0), dimensions=(0, 0), scale=(1, 1), rot=0):
        # Initialize given variables
        self.app = app
        self.pos = pos
        self.scale = scale
        self.rot = rot

        self.width, self.height = dimensions

        self.texture_name = texture_name
        # Get vao, program vars
        self.vao = app.graphics.mesh.vao.vaos[vao_name]
        self.program = self.vao.program

        # generate initial model matrix
        self.model_matrix = self.get_model_matrix()

    def get_model_matrix(self):
        model_matrix = glm.mat4()
        screen_width, screen_height = self.app.win_size()

        # Apply 2d translation to make object coordinates correspond with the top left of the screen
        offset_x = self.width * self.scale[0] / screen_width
        offset_y = self.height * self.scale[1] / screen_height

        pos = (self.pos[0] + offset_x, self.pos[1] - offset_y, 0)
        model_matrix = glm.translate(model_matrix, pos)

        # scale down vertex coords (written in pixels) to be relative to screen
        relative_width = 1 / screen_width
        relative_height = 1 / screen_height
        pixel_rescale = (relative_width, relative_height, 1.0)
        model_matrix = glm.scale(model_matrix, pixel_rescale)

        # Apply rotation
        model_matrix = glm.rotate(model_matrix, self.rot, glm.vec3(0, 0, 1))

        return model_matrix

    def update(self): ...

    def render(self):
        self.update()
        self.vao.render()


class GUI(BaseModel2D):
    # Creates a functional instance of BaseModel2D class
    # Seperate from BaseModel2D class to allow for other derivative children, but there is only 1 needed here
    def __init__(self, app, vao_name='image_vao', texture_name='',
                 pos=(0, 0), dimensions=(0, 0), scale=(1, 1), rot=0):
        super().__init__(app, vao_name, texture_name, pos, dimensions, scale, rot)
        self.on_init()

    def update(self):
        self.texture.use()
        self.model_matrix = self.get_model_matrix()
        self.program['model_matrix'].write(self.model_matrix)

    def on_init(self):
        # Send texture data to shader
        self.texture = self.app.graphics.mesh.texture.textures[self.texture_name]
        self.program['u_texture_0'] = 0
        self.texture.use()

        # Send matrix data to shader
        self.program['model_matrix'].write(self.model_matrix)
