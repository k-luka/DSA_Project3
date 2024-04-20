from abc import ABC, abstractmethod


class Keyfuncs(ABC):
    @abstractmethod
    def switch_to_texture(self) -> None: pass

    def key_switch_to_secondary_texture(self, *args):
        # Switch to the second stored texture, usually a highlight texture
        self.switch_to_texture(1)

    def key_switch_to_default_texture(self, *args):
        # Switch back to the primary texture, usually from highlighted -> un-highlighted texture
        self.switch_to_texture(0)
