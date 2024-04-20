import logging


# A place to store specific button functions
class ButtonFuncs:
    def switch_to_secondary_texture(self, *args):
        # Switch to the second stored texture, usually a highlight texture
        if hasattr(self, 'switch_to_texture'):
            self.switch_to_texture(1)
        else:
            logging.warning(f' Failed to execute button function \'switch_to_secondary_texture\':'
                            f' {self.__class__.__name__} does not have required attributes')

    def switch_to_default_texture(self, *args):
        # Switch back to the primary texture, usually from highlighted -> un-highlighted texture
        if hasattr(self, 'switch_to_texture') and hasattr(self, 'rescale'):
            self.switch_to_texture(0)
        else:
            logging.warning(f' Failed to execute button function \'switch_to_default_texture\':'
                            f' {self.__class__.__name__} does not have required attributes')

    def exit(self, *args):
        # Exit the program
        if hasattr(self, 'app'):
            self.app.quit()

