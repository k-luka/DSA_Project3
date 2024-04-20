import sys
import pygame as pg
from .mesh import Mesh
from .scene import Scene
import moderngl as mgl


class Graphics:
    def __init__(self, win_size=(1600, 900), FPS=60, working_directory="", debug=0):
        # Initialize pygame modules
        pg.init()

        # Store window size
        self.WIN_SIZE = win_size

        # Set framerate
        self.FPS = FPS

        # Set working directory
        self.directory = working_directory

        # Set debug
        self.debug = debug

        # Set opengl attributes
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        # Create opengl context
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)

        # Set existing opengl context
        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)

        # Mouse settings
        self.scrolling = 0

        # Set clock object for time tracking
        self.clock = pg.time.Clock()

        # Create and store mesh object
        self.mesh = Mesh(self)

        # Store objects in scene variable
        self.scene = Scene(self)

        # Create mainloop var for later
        self.mainloop = None

    def close(self):
        self.mesh.destroy()
        pg.quit()
        sys.exit()

    def render(self):
        # Clear framebuffer
        self.ctx.clear(color=(0.12, 0.12, 0.16))
        # Render scene
        self.scene.render()
        # Swap Buffers
        pg.display.flip()

    def render_frame(self):
        self.render()
        self.clock.tick(self.FPS)
