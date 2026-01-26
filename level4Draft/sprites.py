import arcade
import random
import time
from constants import TILE_SIZE, MOVEMENT_SPEED

# מהירות הרוחות - נשאיר אותן איטיות כדי שיהיה הוגן
GHOST_SPEED = 2


class Pacman(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.make_circle_texture(int(TILE_SIZE * 0.8), arcade.color.YELLOW)
        self.width = self.texture.width
        self.height = self.texture.height


class Ghost(arcade.Sprite):
    def __init__(self, ghost_id):
        super().__init__()
        self.ghost_id = ghost_id  # שומרים את המספר המזהה של הרוח

        # צבעים שונים כדי שנוכל להבדיל ביניהן
        if ghost_id == 0:
            color = arcade.color.RED  # הצייד החכם
        elif ghost_id == 1:
            color = arcade.color.PINK
        elif ghost_id == 2:
            color = arcade.color.CYAN
        else:
            color = arcade.color.ORANGE

        self.texture = arcade.make_circle_texture(TILE_SIZE, color)
        self.width = self.texture.width
        self.height = self.texture.height

        self.mode = "scatter"
        self.last_calc_time = 0
        self.change_direction()

    def change_direction(self):
        """ בחירת כיוון רנדומלי """
        directions = [
            (GHOST_SPEED, 0),
            (-GHOST_SPEED, 0),
            (0, GHOST_SPEED),
            (0, -GHOST_SPEED)
        ]
        self.change_x, self.change_y = random.choice(directions)

    def follow_target(self, pathfinder, target_sprite):
        """ ההתנהגות משתנה לפי ה-ID של הרוח """

        # --- רוחות "טיפשות" (סתם מטיילות) ---
        # אם ה-ID הוא לא 0, הרוח הזו לא משתמשת ב-A* בכלל!
        # היא פשוט מסתובבת רנדומלית ומפריעה במקרה.
        if self.ghost_id != 0:
            if self.change_x == 0 and self.change_y == 0:
                self.change_direction()

            # מדי פעם משנות כיוון סתם כדי להיות בלתי צפויות
            if random.random() < 0.02:
                self.change_direction()
            return

        # --- רוח מספר 0: הציידת (היחידה שמשתמשת במוח) ---

        # חישוב מרחק
        distance = ((self.center_x - target_sprite.center_x) ** 2 +
                    (self.center_y - target_sprite.center_y) ** 2) ** 0.5

        # טווח ראייה לציידת
        if distance > 350:
            if self.change_x == 0 and self.change_y == 0:
                self.change_direction()
            return

        # המרה לקואורדינטות רשת
        start_pos = pathfinder.world_to_grid(self.center_x, self.center_y)
        current_grid_center = pathfinder.grid_to_world(start_pos[0], start_pos[1])

        dist_x = abs(self.center_x - current_grid_center[0])
        dist_y = abs(self.center_y - current_grid_center[1])
        TOLERANCE = GHOST_SPEED

        # בדיקה אם הגענו למרכז משבצת
        if dist_x <= TOLERANCE and dist_y <= TOLERANCE:

            # חישוב מסלול A*
            end_pos = pathfinder.world_to_grid(target_sprite.center_x, target_sprite.center_y)
            path = pathfinder.get_path(start_pos, end_pos)

            if path and len(path) > 1:
                next_step = path[1]

                new_change_x = 0
                new_change_y = 0

                if next_step[0] > start_pos[0]:
                    new_change_x = GHOST_SPEED
                elif next_step[0] < start_pos[0]:
                    new_change_x = -GHOST_SPEED
                elif next_step[1] > start_pos[1]:
                    new_change_y = -GHOST_SPEED
                elif next_step[1] < start_pos[1]:
                    new_change_y = GHOST_SPEED

                if new_change_x != self.change_x or new_change_y != self.change_y:
                    self.center_x = current_grid_center[0]
                    self.center_y = current_grid_center[1]
                    self.change_x = new_change_x
                    self.change_y = new_change_y


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