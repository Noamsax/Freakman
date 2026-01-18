# main.py
import arcade
from constants import *
from sprites import Pacman, Ghost, Coin, Wall



class PacmanGame(arcade.View):
    def __init__(self):
        super().__init__()

        self.wall_list = None
        self.coin_list = None
        self.ghost_list = None
        self.player_list = None
        self.player = None
        self.game_over = False
        self.background_color = arcade.color.BLACK
        self.start_x = 0
        self.start_y = 0
        self.score = 0
        self.lives = 3

    def setup(self):
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.ghost_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()

        self.game_over = False
        self.score = 0  # איפוס ניקוד להתחלה

        rows = len(LEVEL_MAP)
        for row_idx, row in enumerate(LEVEL_MAP):
            for col_idx, cell in enumerate(row):
                x = col_idx * TILE_SIZE + TILE_SIZE / 2
                y = (rows - row_idx - 1) * TILE_SIZE + TILE_SIZE / 2

                if cell == "#":
                    wall = Wall()
                    wall.center_x, wall.center_y = x, y
                    self.wall_list.append(wall)
                elif cell == ".":
                    coin = Coin()
                    coin.center_x, coin.center_y = x, y
                    self.coin_list.append(coin)
                elif cell == "G":
                    ghost = Ghost()
                    ghost.center_x, ghost.center_y = x, y
                    self.ghost_list.append(ghost)
                elif cell == "P":
                    self.player = Pacman()
                    self.player.center_x, self.player.center_y = x, y
                    self.player_list.append(self.player)
                    self.start_x = x
                    self.start_y = y

    def on_draw(self):
        self.clear()
        self.wall_list.draw()  # 1. קירות
        self.ghost_list.draw()  # 2. רוחות
        self.coin_list.draw()  # 3. מטבעות
        self.player_list.draw()  # 4. שחקן

        arcade.draw_text(f"Score: {self.score}", 10, WINDOW_HEIGHT - 20, arcade.color.WHITE, 14)
        arcade.draw_text(f"Lives: {self.lives}", 10, WINDOW_HEIGHT - 40, arcade.color.WHITE, 14)

        if self.game_over:
            arcade.draw_text("GAME OVER", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2,
                             arcade.color.RED, 50, anchor_x="center")


def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    game_view = PacmanGame()
    game_view.setup()
    window.show_view(game_view)
    arcade.run()


if __name__ == "__main__":
    main()