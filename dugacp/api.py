import dugacp.original_data as original_data
import dugacp.gameclasses as gameclasses

class DugaAPI:
    def __init__(self):
        self.font = original_data.font
        self.paths = original_data.paths
        self.custom_paths = {}
        self.menu_tiles = []
        self.logo_surface_rect_left = None
        self.custom_textures = []
        self.runner = "NOT SET"
        self._texture_types = {}
        self._solid_tiles = {}
        self._visible_tiles = {}
        self._removed_guns = []
        self._new_guns = {}
        self._spawn_ratings = {}
        self._guns_dict = {}
        self._original_spawnrates = original_data.spawn_mapping

    def _ENTITIES_get_guns(self, guns_dictionary: dict):

        value = guns_dictionary
        value.update(self._new_guns)

        for i in self._removed_guns:
            if value.get(i) is not None:
                value.pop(i)

        self._guns_dict = value

        return value

    def _GENERATION_get_spawnratings(self):
        value = self._guns_dict

        spawnrates = {}

        count = 5
        for i in value:
            if i in self._original_spawnrates:
                spawnrates.update({count: self._original_spawnrates[i]})
            else:
                spawnrates.update({count: self._spawn_ratings[i]})
            count += 1

        return spawnrates

    def _menutiles_get_duga_values(self):
        _value = []
        for i in self.menu_tiles:
            _value.append(i.return_duga_value())
        return _value

    def _menutiles_set_logo_surface_rect_left(self, data, ):
        self.logo_surface_rect_left = data

    def add_gun(self, gun_id, gun, spawnrate):
        self._new_guns.update({gun_id: gun})
        self._spawn_ratings.update({gun_id: spawnrate})

    def remove_gun(self, gun_id):
        self._removed_guns.append(gun_id)

    def get_custom_textures(self):
        return self.custom_textures

    def get_runner(self):
        return self.runner

    def register_texture(self, path, type_of_texture, issolid = True, isvisible = True):
        self.custom_textures.append(path)
        self._texture_types.update({25 + len(self.custom_textures): type_of_texture})
        self._solid_tiles.update({25 + len(self.custom_textures): issolid})
        self._visible_tiles.update({25 + len(self.custom_textures): isvisible})


    def register_path(self, key, path):
        self.custom_paths.update({key: path})

    def get_path(self, key):
        return self.custom_paths.get(key)

    def remove_path(self, key):
        try:
            self.custom_paths.pop(key)
        except:
            pass

    def get_menutile_object(self):
        return gameclasses.MenuTile(self.logo_surface_rect_left)

    def set_font(self, font_path: str) -> None:
        self.font = font_path

    def get_font(self) -> str:
        return self.font

    def set_game_path(self, key, data):
        self.paths[key] = data

    def get_game_path(self, key):
        return self.paths.get(key)

    def add_menutile(self, menu_tile):
        self.menu_tiles.append(menu_tile)

    def remove_menutile(self, name):
        for i, j in enumerate(self.menu_tiles):
            if j.name == name:
                self.menu_tiles.pop(i)
                break