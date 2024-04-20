from .graphics import Graphics
from .vbo import GUI_VBO
from .model import GUI

"""The basis for this 2D graphics engine is adapted from
Coder Space's YouTube tutorial, 'Let's code 3D Engine in Python. OpenGL Pygame Tutorial', found at
https://www.youtube.com/watch?v=eJDIsFJN4OQ"""


def create_app(win_size, fps, working_directory, debug):
    app = Graphics(win_size=win_size,
                   FPS=fps, working_directory=working_directory, debug=debug)
    return app