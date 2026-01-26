import arcade
from constants import *
from sprites import Pacman, Ghost, Coin, Wall
from pathfinding import Pathfinder


class PacmanGame(arcade.View):
    def __init__(self):
        super().__init__()

        self.wall_list = None
        self.coin_list = None
        self.ghost_list = None
        self.player_list = None
        self.player = None
        self.pathfinder = None
        self.game_over = False
        self.score = 0
        self.lives = 3

    def setup(self):
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.ghost_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()

        self.game_over = False
        self.score = 0
        self.lives = 3

        self.pathfinder = Pathfinder(LEVEL_MAP)

        # משתנה שסופר כמה רוחות יצרנו כדי לתת להן ID שונה
        ghost_counter = 0

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
                    # יצירת רוח עם ID ייחודי
                    ghost = Ghost(ghost_counter)
                    ghost.center_x, ghost.center_y = x, y
                    self.ghost_list.append(ghost)
                    ghost_counter += 1  # קידום המספר לרוח הבאה
                elif cell == "P":
                    self.player = Pacman()
                    self.player.center_x, self.player.center_y = x, y
                    self.player_list.append(self.player)
                    self.start_x = x
                    self.start_y = y

    def on_draw(self):
        self.clear()
        self.wall_list.draw()
        self.coin_list.draw()
        self.ghost_list.draw()
        self.player_list.draw()

        arcade.draw_text(f"Score: {self.score}", 10, WINDOW_HEIGHT - 20, arcade.color.WHITE, 14)
        arcade.draw_text(f"Lives: {self.lives}", 10, WINDOW_HEIGHT - 40, arcade.color.WHITE, 14)

        if self.game_over:
            arcade.draw_text("GAME OVER", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2,
                             arcade.color.RED, 50, anchor_x="center")
            arcade.draw_text("Press SPACE to Restart", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50,
                             arcade.color.WHITE, 20, anchor_x="center")

    def on_update(self, delta_time):
        if self.game_over:
            return

        start_x = self.player.center_x
        start_y = self.player.center_y
        self.player.update()

        if arcade.check_for_collision_with_list(self.player, self.wall_list):
            self.player.center_x = start_x
            self.player.center_y = start_y

        for ghost in self.ghost_list:
            ghost_start_x = ghost.center_x
            ghost_start_y = ghost.center_y

            ghost.follow_target(self.pathfinder, self.player)
            ghost.update()

            if arcade.check_for_collision_with_list(ghost, self.wall_list):
                ghost.center_x = ghost_start_x
                ghost.center_y = ghost_start_y

                # אם רוח נתקעת בקיר, היא תמיד משנה כיוון (גם החכמה וגם הטיפשה)
                # כדי שלא יתקעו לנצח
                ghost.change_direction()

        hit_list = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for coin in hit_list:
            self.score += coin.value
            coin.remove_from_sprite_lists()

        if arcade.check_for_collision_with_list(self.player, self.ghost_list):
            self.lives -= 1
            self.player.center_x = self.start_x
            self.player.center_y = self.start_y
            self.player.change_x = 0
            self.player.change_y = 0

            if self.lives <= 0:
                self.game_over = True

    def on_key_press(self, key, modifiers):
        if self.game_over:
            if key == arcade.key.SPACE:
                self.setup()
            return

        CORRECTION = 12
        nearest_x = round((self.player.center_x - TILE_SIZE / 2) / TILE_SIZE) * TILE_SIZE + TILE_SIZE / 2
        nearest_y = round((self.player.center_y - TILE_SIZE / 2) / TILE_SIZE) * TILE_SIZE + TILE_SIZE / 2

        if key == arcade.key.UP:
            if abs(self.player.center_x - nearest_x) <= CORRECTION:
                self.player.center_x = nearest_x
                self.player.change_x = 0
                self.player.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            if abs(self.player.center_x - nearest_x) <= CORRECTION:
                self.player.center_x = nearest_x
                self.player.change_x = 0
                self.player.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            if abs(self.player.center_y - nearest_y) <= CORRECTION:
                self.player.center_y = nearest_y
                self.player.change_y = 0
                self.player.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            if abs(self.player.center_y - nearest_y) <= CORRECTION:
                self.player.center_y = nearest_y
                self.player.change_y = 0
                self.player.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0


def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    game_view = PacmanGame()
    game_view.setup()
    window.show_view(game_view)
    arcade.run()


if __name__ == "__main__":
    main()