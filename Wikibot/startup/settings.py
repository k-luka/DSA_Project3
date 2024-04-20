import os
import logging


class Settings:
    # Allow for settings to be imported from external file
    def __init__(self, filename):
        # Create a list of line strings from settings file
        with open(filename) as self.file:
            self.file = self.file.readlines()

        # Remove white spaces and new lines
        for i in range(len(self.file)):
            self.file[i] = self.file[i].strip('\n')
            self.file[i] = self.file[i].replace('\t', '')
            self.file[i] = self.file[i].replace(' ', '')

        # Extract data from lines
        settings_data = {'screenwidth': 600, 'screenheight': 400, 'fps': 60, 'debug': 0}
        for line in self.file:
            if line != '':
                data = line.split('=')
                if data[0] not in settings_data.keys():
                    logging.warning(f"Setting {data[0]} is not a valid setting. Skipping.")
                elif len(data) == 0:
                    logging.warning(f"Setting {data[0]} does not have a value. Skipping.")
                else:
                    try:
                        value = int(data[1])
                        settings_data[data[0]] = value
                    except ValueError:
                        logging.warning(f"Setting {data[0]} does not have an integer value. Skipping.")

        # Process data from lines
        self.widthSetting = settings_data['screenwidth']
        self.heightSetting = settings_data['screenheight']
        self.fpsSetting = settings_data['fps']
        self.debugSetting = settings_data['debug']

