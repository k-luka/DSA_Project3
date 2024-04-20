from typing import Union
import pygame as pg
import moderngl as mgl


class Texture:
    # Uses pygame module to convert either text or a texture image file into a Surface to be turned into pixel data for rendering
    def __init__(self, ctx):
        self.ctx = ctx
        self.textures = {}

    def generate_texture(self, name: str, directory: str) -> None:
        self.textures[name] = self.get_image_texture(path=f'{directory}/textures/{name}')

    def generate_texture_txt(self, name:str, size: int, color: tuple[int, int, int], text: str, background: Union[tuple[int, int, int], None]) -> None:
        if background is None:
            background = (255, 255, 255)
        self.textures[name] = self.get_text_texture(size=size, color=color, text=text, background=background)

    def get_image_texture(self, path: str) -> pg.Surface:
        texture = pg.image.load(path).convert_alpha()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(), components=4,
                                   data=pg.image.tostring(texture, 'RGBA'))
        # Mipmaps
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()

        # Anisotropic Filtering
        texture.anisotropy = 32.0

        return texture

    def get_text_texture(self, size: int, color: tuple[int, int, int], text: str, background: tuple[int, int, int]) -> pg.Surface:
        texture = pg.font.Font(None, size).render(text, True, color, background)
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(), components=4,
                                   data=pg.image.tostring(texture, 'RGBA'))
        # Mipmaps
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()

        # Anisotropic Filtering
        texture.anisotropy = 32.0

        return texture

    def destroy(self) -> None:
        [texture.release() for texture in self.textures.values()]
