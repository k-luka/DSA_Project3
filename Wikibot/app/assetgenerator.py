from .asset.sprite import Sprite, SpriteCreateInfo
from .asset.textsprite import TextSprite, TextSpriteCreateInfo
from .appinterface import AppInterface
from .stages.stage import Stage, StageCreateInfo, AssetCreateInfo
from typing import Union
import pygame as pg


def generate_stage_info(app: Union[type[AppInterface], AppInterface]) -> list[StageCreateInfo]:
    return [
        StageCreateInfo(
            app=app,
            name="main_menu",
            stage_func=None,
            kdfs=None,
            kufs={pg.K_ESCAPE: "quit", pg.K_n: "add_node", pg.K_l: "add_node_with_link"}
        )
    ]


def generate_asset_info(stage: Stage) -> list[AssetCreateInfo]:
    assets = list()
    if stage.name == "main_menu":
        assets.append(generate_asset("exit_button", stage))
        assets.append(generate_asset("source_text_box", stage)) # TODO: Design source text box
        #assets.append(generate_asset("target_text_box", stage)) # TODO: Design target text box
        #assets.append(generate_asset("search_depth_box", stage)) # TODO: Design search depth box
        #assets.append(generate_asset("toggle_1", stage)) # TODO: Designate toggle parameter
        #assets.append(generate_asset("toggle_2", stage)) # TODO: Designate toggle parameter
        #assets.append(generate_asset("go_button", stage)) # TODO: Design go button
        #assets.append(generate_asset("reset_button", stage)) # TODO: Design reset button
        #assets.append(generate_asset("custom_cursor", stage))
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
            rot=0,
            kdfs={pg.K_x: 'key_switch_to_secondary_texture'},
            kufs={pg.K_x: 'key_switch_to_default_texture'},
            textures=["exit.png", "exit_border.png"],
            haf='switch_to_secondary_texture',
            hdf='switch_to_default_texture',
            cafs=None,
            cdfs={1: 'exit'}
        )
        object_type = Sprite
        default_viewable = True
        return AssetCreateInfo(
            create_info,
            object_type,
            default_viewable
        )
    elif asset_name == "source_text_box":
        create_info = TextSpriteCreateInfo(
            app=stage.app,
            name=asset_name,
            stage=stage,
            posPx=(25, 25),
            dimensionsPx=(150, 25),
            scale=(1, 1),
            rot=0,
            kdfs={pg.K_BACKSPACE: 'backspace'},
            kufs=None,
            cafs=None,
            cdfs=None,
            size=30,
            text='Enter Title Here',
            color=(200, 200, 200),
            background=(10, 10, 10),
            # char_size=(30, 20),
            auto_textbox_scaling=True,
            text_func='type_alphanum',
        )
        object_type = TextSprite
        default_viewable = True
        return AssetCreateInfo(
            create_info,
            object_type,
            default_viewable
        )

