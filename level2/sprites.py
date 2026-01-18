# sprites.py
import arcade
from constants import TILE_SIZE

class Pacman(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.make_circle_texture(TILE_SIZE, arcade.color.YELLOW)
        self.width = self.texture.width
        self.height = self.texture.height

class Ghost(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.make_circle_texture(TILE_SIZE, arcade.color.RED)
        self.width = self.texture.width
        self.height = self.texture.height

class Coin(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.make_circle_texture(int(TILE_SIZE / 4), arcade.color.YELLOW)
        self.width = self.texture.width
        self.height = self.texture.height

class Wall(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.make_soft_square_texture(TILE_SIZE, arcade.color.BLUE, outer_alpha=255)
        self.width = self.texture.width
        self.height = self.texture.height