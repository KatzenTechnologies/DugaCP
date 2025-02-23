import pygame

# Классы для удобства кодинга апи dugacp
class MenuTile:
    def __init__(self, logo_surface_rect_left):
        self.logo_surface_rect_left = logo_surface_rect_left
        self.count_tiles = 0
        self.name = None
        self.duga_value = []

    def set_name(self, name):
        self.name = name

    def add_texture(self, texture_path):
        self.duga_value.append([pygame.image.load(texture_path).convert(), self.logo_surface_rect_left + (160*self.count_tiles)])
        self.count_tiles += 1

    def return_duga_value(self):
        return self.duga_value
