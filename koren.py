import arcade

# --- קבועים (Constants) ---
# [cite: 83-86] הגדרת רוחב ואורך החלון, כותרת, גודל אריח ומפת השלב
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Pacman Nitzanim"
TILE_SIZE = 32

# מפת שלב לדוגמה (נבנתה כדי להתאים לגודל החלון ולקוד)
# P = שחקן, G = רוח, . = מטבע, # = קיר
LEVEL_MAP = [
    "#########################",
    "#P............#.........#",
    "#.###.#######.#.#######.#",
    "#.#...#.......G.......#.#",
    "#.#.###.#####.#.#####.#.#",
    "#.............#.........#",
    "#.###.#######.#######.###",
    "#...#.................#.#",
    "###.###.#.#####.#.###.###",
    "#.......#...G...#.......#",
    "#########################"
]


# --- מחלקות האובייקטים (Sprites) ---

class Pacman(arcade.Sprite):
    def __init__(self):
        super().__init__()
        # [cite: 19] עיגול צהוב
        self.texture = arcade.make_circle_texture(TILE_SIZE, arcade.color.YELLOW)
        # [cite: 34-36] עדכון רוחב וגובה לפי הטקסטורה
        self.width = self.texture.width
        self.height = self.texture.height


class Ghost(arcade.Sprite):
    def __init__(self):
        super().__init__()
        # [cite: 20] עיגול אדום
        self.texture = arcade.make_circle_texture(TILE_SIZE, arcade.color.RED)
        self.width = self.texture.width
        self.height = self.texture.height


class Coin(arcade.Sprite):
    def __init__(self):
        super().__init__()
        # [cite: 21] עיגול צהוב קטן (חצי גודל)
        self.texture = arcade.make_circle_texture(int(TILE_SIZE / 4), arcade.color.YELLOW)
        self.width = self.texture.width
        self.height = self.texture.height


class Wall(arcade.Sprite):
    def __init__(self):
        super().__init__()
        # [cite: 22] ריבוע כחול
        self.texture = arcade.make_soft_square_texture(TILE_SIZE, arcade.color.BLUE, outer_alpha=255)
        self.width = self.texture.width
        self.height = self.texture.height


# --- מחלקת ניהול המשחק ---

class PacmanGame(arcade.View):  # [cite: 41] יורשת מ-arcade.View
    def __init__(self):
        # [cite: 47] מתודת הבנאי
        super().__init__()

        # [cite: 49-52] אתחול הרשימות
        self.wall_list = None
        self.coin_list = None
        self.ghost_list = None
        self.player_list = None

        # [cite: 53-56] אתחול משתנים נוספים
        self.player = None
        self.game_over = False
        self.background_color = arcade.color.BLACK
        self.start_x = 0
        self.start_y = 0

        # משתנים לניקוד וחיים (נדרשים עבור on_draw)
        self.score = 0
        self.lives = 3

    def setup(self):
        # [cite: 60-65] אתחול המשחק מחדש ובניית המפה

        # 1. יצירת ה-SpriteLists מחדש
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.ghost_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()

        # 2. איפוס דגל המשחק
        self.game_over = False
        self.score = 0  # איפוס ניקוד

        # 3. בניית העולם לפי המפה [cite: 68-71]
        rows = len(LEVEL_MAP)
        for row_idx, row in enumerate(LEVEL_MAP):
            for col_idx, cell in enumerate(row):
                # חישוב המיקום לפי הנוסחה שניתנה במדריך
                x = col_idx * TILE_SIZE + TILE_SIZE / 2
                y = (rows - row_idx - 1) * TILE_SIZE + TILE_SIZE / 2

                if cell == "#":
                    wall = Wall()
                    wall.center_x = x
                    wall.center_y = y
                    self.wall_list.append(wall)
                elif cell == ".":
                    coin = Coin()
                    coin.center_x = x
                    coin.center_y = y
                    self.coin_list.append(coin)
                elif cell == "G":
                    ghost = Ghost()
                    ghost.center_x = x
                    ghost.center_y = y
                    self.ghost_list.append(ghost)
                elif cell == "P":
                    # יצירת השחקן ושמירת נקודת ההתחלה
                    self.player = Pacman()
                    self.player.center_x = x
                    self.player.center_y = y
                    self.start_x = x
                    self.start_y = y
                    self.player_list.append(self.player)

    def on_draw(self):
        # [cite: 72-73] ציור המשחק למסך
        self.clear()  # ניקוי המסך לפני ציור מחדש

        # 1-4. ציור האובייקטים [cite: 74-77]
        self.wall_list.draw()
        self.coin_list.draw()
        self.ghost_list.draw()
        self.player_list.draw()

        # 5-6. טקסט ניקוד וחיים בצד שמאל למעלה [cite: 78-79]
        arcade.draw_text(f"Score: {self.score}", 10, WINDOW_HEIGHT - 20, arcade.color.WHITE, 14)
        arcade.draw_text(f"Lives: {self.lives}", 10, WINDOW_HEIGHT - 40, arcade.color.WHITE, 14)

        # 7. טקסט "הפסדנו" אם המשחק נגמר [cite: 80]
        if self.game_over:
            arcade.draw_text("GAME OVER", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2,
                             arcade.color.RED, 50, anchor_x="center")


# --- הרצת המשחק (Main) ---
# [cite: 96-104] סדר הפעולות הנדרש להרצה
def main():
    # 1. יצירת חלון
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    # 2. יצירת אובייקט המשחק
    game_view = PacmanGame()

    # 3. אתחול עולם המשחק
    game_view.setup()

    # 4. הצגת ה-View
    window.show_view(game_view)

    # 5. הפעלת לולאת המשחק
    arcade.run()


if __name__ == "__main__":
    main()