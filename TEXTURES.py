#Textures for tiles: Walls and sprites.
import os

all_textures = []

def init_dugacp_api(game_api):
    global all_textures
    all_textures = [
        game_api.paths["null"], #Air #0

        #-- Wood theme --
        # Walls
        game_api.paths["wood_wall"],  #1
        game_api.paths["wood_painting"],  #2
        game_api.paths["wood_fireplace"],  #3
        game_api.paths["wood_books"],  #4
        game_api.paths["wood_end"],  #5

        # Doors 6&7 Originally Double-Defined
        game_api.paths["wood_door"],  #6
        game_api.paths["wood_door"],  #7
        # Sprites
        game_api.paths["pillar"],  #8
        game_api.paths["table"],  #9
        game_api.paths["lysekrone"],  #10

        #-- Stone theme --
        # Walls
        game_api.paths["stone_wall"],  # 11
        game_api.paths["stone_vent"],  #12
        game_api.paths["stone_wall_crack"],  #13
        game_api.paths["stone_vase"],  #14
        game_api.paths["stone_end"],  #15

        # Sprites
        game_api.paths["lysestage"], #16
        game_api.paths["barrel"], #17
        game_api.paths["stone_pillar"], #18

        #-- Baroque theme --
        # Walls
        game_api.paths["baroque"], #19
        game_api.paths["baroque_lamps"], #20
        game_api.paths["baroque_worn"], #21
        game_api.paths["baroque_end"], # 22

        # Doors
        game_api.paths["baroque_door"], #23
        game_api.paths["baroque_door"], #24
        # Sprites
        game_api.paths["fern"] #25
        ]
    all_textures += game_api.get_custom_textures()

