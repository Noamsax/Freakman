import arcade
import random
from constants import TILE_SIZE, MOVEMENT_SPEED

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
        self.change_direction()

    def change_direction(self):
        directions = [
            (MOVEMENT_SPEED, 0),
            (-MOVEMENT_SPEED, 0),
            (0, MOVEMENT_SPEED),
            (0, -MOVEMENT_SPEED)
        ]
        self.change_x, self.change_y = random.choice(directions)

class Coin(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.make_circle_texture(int(TILE_SIZE / 4), arcade.color.YELLOW)
        self.width = self.texture.width
        self.height = self.texture.height
        self.value = 10

class Wall(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.make_soft_square_texture(TILE_SIZE, arcade.color.BLUE, outer_alpha=255)
        self.width = self.texture.width
        self.height = self.texture.height