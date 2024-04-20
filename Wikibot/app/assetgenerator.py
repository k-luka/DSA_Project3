from .stages import Stage, StageCreateInfo, AssetCreateInfo
from .asset import *
from .appinterface import AppInterface
from typing import Union
import pygame as pg


def generate_stage_info(app: Union[type[AppInterface], AppInterface]) -> list[StageCreateInfo]:
    return [
        StageCreateInfo(
            app=app,
            name="main_menu"
        )
    ]

def generate_asset_info(stage: Stage) -> list[AssetCreateInfo]:
    assets = list()
    if stage.name == "main_menu":
        assets.append(generate_asset("exit_button", stage))
    return assets


def generate_asset(asset_name: str, stage: Stage):
    if asset_name == "exit_button":
        create_info = SpriteCreateInfo(
            app=stage.app,
            name=asset_name,
            stage=stage,
            posPx=(25, 500),
            dimensionsPx=(100, 100),
            scale=(1, 1),
            kdfs={pg.K_x: 'key_switch_to_secondary_texture'},
            kufs={pg.K_x: 'key_switch_to_default_texture'},
            textures=["exit.png", "exit_border.png"],
            haf='switch_to_secondary_texture',
            hdf='switch_to_default_texture',
            cafs=None,
            cdfs={1: 'exit'}
        )
        object_type = Sprite
        default_viewable=True
        return AssetCreateInfo(
            create_info,
            object_type,
            default_viewable
        )
