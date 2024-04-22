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
        assets.append(generate_asset("source_text_box", stage))
        assets.append(generate_asset("source_text_box_background", stage))
        assets.append(generate_asset("target_text_box", stage))
        assets.append(generate_asset("target_text_box_background", stage))
        assets.append(generate_asset("search_breadth_text", stage))
        assets.append(generate_asset("search_breadth_background", stage))
        assets.append(generate_asset("number_box", stage))
        assets.append(generate_asset("number_box_background", stage))
        assets.append(generate_asset("weight_unique_words_text", stage))
        assets.append(generate_asset("weight_unique_words_background", stage))
        assets.append(generate_asset("uniqueness_enabled_text", stage))
        assets.append(generate_asset("uniqueness_enabled_background", stage))
        assets.append(generate_asset("uniqueness_switch", stage))
        assets.append(generate_asset("mode_text", stage))
        assets.append(generate_asset("mode_text_background", stage))
        assets.append(generate_asset("mode_switch", stage))
        assets.append(generate_asset("mode_display_text", stage))
        assets.append(generate_asset("mode_display_background", stage))
        assets.append(generate_asset("go_button", stage))
        assets.append(generate_asset("reset_button", stage))
        assets.append(generate_asset("exit_button", stage))
        assets.append(generate_asset("ui_menu", stage))
        #assets.append(generate_asset("custom_cursor", stage))
    return assets


def generate_asset(asset_name: str, stage: Stage):
    if asset_name == "source_text_box":
        create_info = TextSpriteCreateInfo(
            app=stage.app,
            name=asset_name,
            stage=stage,
            posPx=(35, 35),
            dimensionsPx=(235, 30),
            scale=(1, 1),
            rot=0,
            kdfs={pg.K_BACKSPACE: 'backspace'},
            kufs=None,
            cafs=None,
            cdfs=None,
            size=30,
            text='Enter Source Page',
            color=(200, 200, 200),
            background=(134, 134, 134),
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
    elif asset_name == "source_text_box_background":
        create_info = SpriteCreateInfo(
            app=stage.app,
            name=asset_name,
            stage=stage,
            posPx=(25, 25),
            dimensionsPx=(250, 38),
            scale=(1, 1),
            rot=0,
            kdfs=None,
            kufs=None,
            textures=["text_box_background_selected.png", "text_box_background.png"],
            haf=None,
            hdf=None,
            cafs={1: 'select_source_text_box'},
            cdfs=None,
            cof='deselect_source_text_box'
        )
        object_type = Sprite
        default_viewable = True
        return AssetCreateInfo(
            create_info,
            object_type,
            default_viewable
        )
    elif asset_name == "target_text_box":
        create_info = TextSpriteCreateInfo(
            app=stage.app,
            name=asset_name,
            stage=stage,
            posPx=(35, 79),
            dimensionsPx=(235, 30),
            scale=(1, 1),
            rot=0,
            kdfs={pg.K_BACKSPACE: 'backspace'},
            kufs=None,
            cafs=None,
            cdfs=None,
            size=30,
            text='Enter Target Page',
            color=(200, 200, 200),
            background=(134, 134, 134),
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
    elif asset_name == "target_text_box_background":
        create_info = SpriteCreateInfo(
            app=stage.app,
            name=asset_name,
            stage=stage,
            posPx=(25, 69),
            dimensionsPx=(250, 38),
            scale=(1, 1),
            rot=0,
            kdfs=None,
            kufs=None,
            textures=["text_box_background_selected.png", "text_box_background.png"],
            haf=None,
            hdf=None,
            cafs={1: 'select_target_text_box'},
            cdfs=None,
            cof='deselect_target_text_box'
        )
        object_type = Sprite
        default_viewable = True
        return AssetCreateInfo(
            create_info,
            object_type,
            default_viewable
        )
    elif asset_name == "search_breadth_text":
        create_info = TextSpriteCreateInfo(
            app=stage.app,
            name=asset_name,
            stage=stage,
            posPx=(33, 143),
            dimensionsPx=(30, 30),
            scale=(1, 1),
            rot=0,
            kdfs=None,
            kufs=None,
            cafs=None,
            cdfs=None,
            size=30,
            text='Search Breadth:',
            color=(20, 20, 20),
            background=(134, 134, 134),
            auto_textbox_scaling=True,
            text_func=None,
        )
        object_type = TextSprite
        default_viewable = True
        return AssetCreateInfo(
            create_info,
            object_type,
            default_viewable
        )
    elif asset_name == "search_breadth_background":
        create_info = SpriteCreateInfo(
            app=stage.app,
            name=asset_name,
            stage=stage,
            posPx=(25, 133),
            dimensionsPx=(175, 38),
            scale=(1, 1),
            rot=0,
            kdfs=None,
            kufs=None,
            textures=["search_breadth.png"],
            haf=None,
            hdf=None,
            cafs=None,
            cdfs=None,
            cof=None,
        )
        object_type = Sprite
        default_viewable = True
        return AssetCreateInfo(
            create_info,
            object_type,
            default_viewable
        )
    elif asset_name == "number_box":
        create_info = TextSpriteCreateInfo(
            app=stage.app,
            name=asset_name,
            stage=stage,
            posPx=(250, 143),
            dimensionsPx=(30, 30),
            scale=(1, 1),
            rot=0,
            kdfs={pg.K_BACKSPACE: 'backspace'},
            kufs=None,
            cafs=None,
            cdfs=None,
            size=30,
            text='5',
            color=(200, 200, 200),
            background=(134, 134, 134),
            auto_textbox_scaling=True,
            text_func='type_numeric_one_digit',
        )
        object_type = TextSprite
        default_viewable = True
        return AssetCreateInfo(
            create_info,
            object_type,
            default_viewable
        )
    elif asset_name == "number_box_background":
        create_info = SpriteCreateInfo(
            app=stage.app,
            name=asset_name,
            stage=stage,
            posPx=(237, 133),
            dimensionsPx=(38, 38),
            scale=(1, 1),
            rot=0,
            kdfs=None,
            kufs=None,
            textures=["number_box.png", "number_box_selected.png"],
            haf=None,
            hdf=None,
            cafs={1: 'select_number_box'},
            cdfs=None,
            cof='deselect_number_box'
        )
        object_type = Sprite
        default_viewable = True
        return AssetCreateInfo(
            create_info,
            object_type,
            default_viewable
        )
    elif asset_name == "weight_unique_words_text":
        create_info = TextSpriteCreateInfo(
            app=stage.app,
            name=asset_name,
            stage=stage,
            posPx=(33, 187),
            dimensionsPx=(30, 30),
            scale=(1, 1),
            rot=0,
            kdfs=None,
            kufs=None,
            cafs=None,
            cdfs=None,
            size=30,
            text='Unique Word Weighting',
            color=(20, 20, 20),
            background=(134, 134, 134),
            auto_textbox_scaling=True,
            text_func=None,
        )
        object_type = TextSprite
        default_viewable = True
        return AssetCreateInfo(
            create_info,
            object_type,
            default_viewable
        )
    elif asset_name == "weight_unique_words_background":
        create_info = SpriteCreateInfo(
            app=stage.app,
            name=asset_name,
            stage=stage,
            posPx=(25, 177),
            dimensionsPx=(250, 38),
            scale=(1, 1),
            rot=0,
            kdfs=None,
            kufs=None,
            textures=["text_box_background_selected.png"],
            haf=None,
            hdf=None,
            cafs=None,
            cdfs=None,
            cof=None,
        )
        object_type = Sprite
        default_viewable = True
        return AssetCreateInfo(
            create_info,
            object_type,
            default_viewable
        )
    elif asset_name == "uniqueness_enabled_text":
        create_info = TextSpriteCreateInfo(
            app=stage.app,
            name=asset_name,
            stage=stage,
            posPx=(33, 231),
            dimensionsPx=(155, 30),
            scale=(1, 1),
            rot=0,
            kdfs=None,
            kufs=None,
            cafs=None,
            cdfs=None,
            size=30,
            text='Enabled',
            color=(200, 200, 200),
            background=(134, 134, 134),
            auto_textbox_scaling=True,
            text_func=None,
        )
        object_type = TextSprite
        default_viewable = True
        return AssetCreateInfo(
            create_info,
            object_type,
            default_viewable
        )
    elif asset_name == "uniqueness_enabled_background":
        create_info = SpriteCreateInfo(
            app=stage.app,
            name=asset_name,
            stage=stage,
            posPx=(25, 221),
            dimensionsPx=(106, 38),
            scale=(1, 1),
            rot=0,
            kdfs=None,
            kufs=None,
            textures=["uniqueness_enabled.png"],
            haf=None,
            hdf=None,
            cafs=None,
            cdfs=None,
            cof=None,
        )
        object_type = Sprite
        default_viewable = True
        return AssetCreateInfo(
            create_info,
            object_type,
            default_viewable
        )
    elif asset_name == "uniqueness_switch":
        create_info = SpriteCreateInfo(
            app=stage.app,
            name=asset_name,
            stage=stage,
            posPx=(182, 221),
            dimensionsPx=(76, 38),
            scale=(1, 1),
            rot=0,
            kdfs=None,
            kufs=None,
            textures=["switch_on.png", "switch_off.png"],
            haf=None,
            hdf=None,
            cafs={1: 'switch_uniqueness_mode'},
            cdfs=None,
            cof=None,
        )
        object_type = Sprite
        default_viewable = True
        return AssetCreateInfo(
            create_info,
            object_type,
            default_viewable
        )
    elif asset_name == "mode_text":
        create_info = TextSpriteCreateInfo(
            app=stage.app,
            name=asset_name,
            stage=stage,
            posPx=(35, 275),
            dimensionsPx=(30, 30),
            scale=(1, 1),
            rot=0,
            kdfs=None,
            kufs=None,
            cafs=None,
            cdfs=None,
            size=30,
            text='Search Algorithm',
            color=(20, 20, 20),
            background=(134, 134, 134),
            auto_textbox_scaling=True,
            text_func=None,
        )
        object_type = TextSprite
        default_viewable = True
        return AssetCreateInfo(
            create_info,
            object_type,
            default_viewable
        )
    elif asset_name == "mode_text_background":
        create_info = SpriteCreateInfo(
            app=stage.app,
            name=asset_name,
            stage=stage,
            posPx=(25, 265),
            dimensionsPx=(193, 38),
            scale=(1, 1),
            rot=0,
            kdfs=None,
            kufs=None,
            textures=["algorithm.png"],
            haf=None,
            hdf=None,
            cafs=None,
            cdfs=None,
            cof=None,
        )
        object_type = Sprite
        default_viewable = True
        return AssetCreateInfo(
            create_info,
            object_type,
            default_viewable
        )
    elif asset_name == "mode_switch":
        create_info = SpriteCreateInfo(
            app=stage.app,
            name=asset_name,
            stage=stage,
            posPx=(22, 309),
            dimensionsPx=(76, 38),
            scale=(1, 1),
            rot=0,
            kdfs=None,
            kufs=None,
            textures=["switch_left.png", "switch_right.png"],
            haf=None,
            hdf=None,
            cafs={1: 'switch_search_mode'},
            cdfs=None,
            cof=None,
        )
        object_type = Sprite
        default_viewable = True
        return AssetCreateInfo(
            create_info,
            object_type,
            default_viewable
        )
    elif asset_name == "mode_display_text":
        create_info = TextSpriteCreateInfo(
            app=stage.app,
            name=asset_name,
            stage=stage,
            posPx=(137, 319),
            dimensionsPx=(75, 30),
            scale=(1, 1),
            rot=0,
            kdfs=None,
            kufs=None,
            cafs=None,
            cdfs=None,
            size=30,
            text='BFS',
            color=(200, 200, 200),
            background=(134, 134, 134),
            auto_textbox_scaling=True,
            text_func=None,
        )
        object_type = TextSprite
        default_viewable = True
        return AssetCreateInfo(
            create_info,
            object_type,
            default_viewable
        )
    elif asset_name == "mode_display_background":
        create_info = SpriteCreateInfo(
            app=stage.app,
            name=asset_name,
            stage=stage,
            posPx=(127, 309),
            dimensionsPx=(91, 38),
            scale=(1, 1),
            rot=0,
            kdfs=None,
            kufs=None,
            textures=["mode_text.png"],
            haf=None,
            hdf=None,
            cafs=None,
            cdfs=None,
            cof=None,
        )
        object_type = Sprite
        default_viewable = True
        return AssetCreateInfo(
            create_info,
            object_type,
            default_viewable
        )
    elif asset_name == "go_button":
        create_info = SpriteCreateInfo(
            app=stage.app,
            name=asset_name,
            stage=stage,
            posPx=(24, 430),
            dimensionsPx=(80, 80),
            scale=(1, 1),
            rot=0,
            kdfs=None,
            kufs=None,
            textures=["go.png", "go_border.png", "go_press.png"],
            haf='switch_to_secondary_texture',
            hdf='switch_to_default_texture',
            cafs={1: 'switch_to_tertiary_texture'},
            cdfs={1: 'go'}
        )
        object_type = Sprite
        default_viewable = True
        return AssetCreateInfo(
            create_info,
            object_type,
            default_viewable
        )
    elif asset_name == "reset_button":
        create_info = SpriteCreateInfo(
            app=stage.app,
            name=asset_name,
            stage=stage,
            posPx=(110, 430),
            dimensionsPx=(80, 80),
            scale=(1, 1),
            rot=0,
            kdfs=None,
            kufs=None,
            textures=["reset.png", "reset_border.png", "reset_clicked.png"],
            haf='switch_to_secondary_texture',
            hdf='switch_to_default_texture',
            cafs={1: 'switch_to_tertiary_texture'},
            cdfs={1: 'reset'}
        )
        object_type = Sprite
        default_viewable = True
        return AssetCreateInfo(
            create_info,
            object_type,
            default_viewable
        )
    elif asset_name == "exit_button":
        create_info = SpriteCreateInfo(
            app=stage.app,
            name=asset_name,
            stage=stage,
            posPx=(196, 430),
            dimensionsPx=(80, 80),
            scale=(1, 1),
            rot=0,
            kdfs={pg.K_x: 'key_switch_to_secondary_texture'},
            kufs={pg.K_x: 'key_switch_to_default_texture'},
            textures=["exit.png", "exit_border.png", "exit_clicked.png"],
            haf='switch_to_secondary_texture',
            hdf='switch_to_default_texture',
            cafs={1: 'switch_to_tertiary_texture'},
            cdfs={1: 'exit'}
        )
        object_type = Sprite
        default_viewable = True
        return AssetCreateInfo(
            create_info,
            object_type,
            default_viewable
        )
    elif asset_name == "ui_menu":
        create_info = SpriteCreateInfo(
            app=stage.app,
            name=asset_name,
            stage=stage,
            posPx=(0, 0),
            dimensionsPx=(300, 600),
            scale=(1, 1),
            rot=0,
            kdfs=None,
            kufs=None,
            textures=["ui_background.png"],
            haf=None,
            hdf=None,
            cafs=None,
            cdfs=None,
        )
        object_type = Sprite
        default_viewable = True
        return AssetCreateInfo(
            create_info,
            object_type,
            default_viewable
        )

