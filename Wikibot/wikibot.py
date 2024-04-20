import logging
import time
import os
from startup import Settings
from app.application import Application, AppCreateInfo


def main(win_size, fps, debug_level):
    # Get working directory
    working_directory = os.getcwd()
    if '\\Wikibot' not in working_directory:
        working_directory += '\\Wikibot'
    # Create application window
    app_create_info = AppCreateInfo(
        win_size=win_size,
        fps=fps,
        working_directory=working_directory,
        debug_level=debug_level)
    application = Application(app_create_info)
    application.run()


if __name__ == "__main__":
    # Start loading timer
    startTime = time.perf_counter()

    # Logging setup1
    logging.basicConfig(level=logging.WARN)
    logging.info(f" Running \'main.py\' as \'main\'")

    # Import file settings and initialize pygame
    settings_data = Settings('startup/settings.txt')
    screensize = settings_data.widthSetting, settings_data.heightSetting
    FPS = settings_data.fpsSetting
    debug = settings_data.debugSetting

    # Logging setup2
    logging_level = logging.INFO if debug == 0 else logging.WARN
    logging.basicConfig(level=logging_level)

    # Run app
    logging.info(f" Finished initialization in: {time.perf_counter() - startTime} seconds")

    main(screensize, FPS, debug)

    logging.info(f" Program finished in: {time.perf_counter() - startTime} seconds")