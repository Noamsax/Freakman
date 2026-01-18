import random


# ==========================================
# חלק 1: המחלקות (לפי הוראות ה-PDF)
# ==========================================

class Coin:
    """
    מחלקה המייצגת מטבע במשחק.
    """

    def __init__(self, center_x, center_y, value=10):
        # שמירת המיקום של המטבע
        self.center_x = center_x
        self.center_y = center_y
        # שמירת הערך של המטבע (ברירת מחדל 10)
        self.value = value


class Wall:
    """
    מחלקה המייצגת קיר במשחק (מכשול).
    """

    def __init__(self, center_x, center_y):
        self.center_x = center_x
        self.center_y = center_y


class Character:
    """
    מחלקה כללית לדמות (גם שחקן וגם אויב יורשים ממנה).
    מכילה תכונות משותפות כמו מיקום ומהירות.
    """

    def __init__(self, center_x, center_y, speed=1.0):
        self.center_x = center_x
        self.center_y = center_y
        self.speed = speed

        # כיוון התנועה הנוכחי (0 אומר שלא זזים)
        self.change_x = 0
        self.change_y = 0


class Player(Character):
    """
    השחקן הראשי (פקמן).
    יורש מ-Character ולכן יש לו מיקום ומהירות.
    """

    def __init__(self, center_x, center_y, speed=1.0):
        # קריאה לבנאי של המחלקה Character כדי לאתחל מיקום
        super().__init__(center_x, center_y, speed)

        # תכונות מיוחדות לפקמן
        self.score = 0  # ניקוד
        self.lives = 3  # חיים

    def move(self):
        """
        פעולה שמזיזה את הפקמן לפי הכיוון והמהירות שלו.
        """
        # חישוב המרחק: כיוון * מהירות
        step_x = self.change_x * self.speed
        step_y = self.change_y * self.speed

        # עדכון המיקום החדש
        self.center_x = self.center_x + step_x
        self.center_y = self.center_y + step_y


class Enemy(Character):
    """
    אויב (רוח רפאים).
    יורש מ-Character.
    """

    def __init__(self, center_x, center_y, speed=1.0):
        super().__init__(center_x, center_y, speed)
        # משתנה שעוזר לרוח להחליט מתי לשנות כיוון שוב
        self.time_to_change_direction = 0

    def pick_new_direction(self):
        """
        בוחר כיוון תנועה חדש באופן אקראי.
        """
        # רשימה של כל הכיוונים האפשריים:
        # (ימינה, שמאלה, למעלה, למטה, או עמידה במקום)
        possible_directions = [
            (1, 0),  # ימינה
            (-1, 0),  # שמאלה
            (0, 1),  # למעלה
            (0, -1),  # למטה
            (0, 0)  # ללא תנועה
        ]

        # בחירת כיוון אחד אקראי מתוך הרשימה
        chosen_direction = random.choice(possible_directions)

        # עדכון כיווני התנועה של הרוח
        self.change_x = chosen_direction[0]
        self.change_y = chosen_direction[1]

        # קביעת זמן אקראי עד לשינוי הכיוון הבא (בין 0.3 ל-1.0 שניות)
        self.time_to_change_direction = random.uniform(0.3, 1.0)

    def update(self, delta_time=1 / 60):
        """
        פעולה שמעדכנת את מצב הרוח (נקראת כל הזמן במשחק רציף).
        """
        # הפחתת הזמן שנשאר עד להחלפת כיוון
        self.time_to_change_direction = self.time_to_change_direction - delta_time

        # אם הזמן נגמר - בוחרים כיוון חדש
        if self.time_to_change_direction <= 0:
            self.pick_new_direction()

        # הזזת הרוח
        self.center_x = self.center_x + (self.change_x * self.speed)
        self.center_y = self.center_y + (self.change_y * self.speed)


# ==========================================
# חלק 2: משחק הקונסול (בדיקה)
# ==========================================

# מפה לדוגמה: # = קיר, . = מטבע, P = פקמן, G = רוח
LEVEL_MAP = [
    "###########",
    "#P....G...#",
    "#.........#",
    "###########",
]


class ConsolePacmanGame:
    """
    מחלקה שמנהלת את המשחק בתוך מסך הטקסט (Console).
    """

    def __init__(self, level_map):
        self.level_map = level_map
        # חישוב גובה ורוחב המפה
        self.height = len(level_map)
        if self.height > 0:
            self.width = len(level_map[0])
        else:
            self.width = 0

        # רשימות שיחזיקו את האובייקטים במשחק
        self.walls = []
        self.coins = []
        self.ghosts = []
        self.player = None

        self.start_x = 0
        self.start_y = 0

        # הפעלת הפונקציה שטוענת את המשחק
        self.setup()

    def setup(self):
        """
        קורא את המפה ויוצר את האובייקטים (קירות, מטבעות, שחקן).
        """
        # איפוס רשימות
        self.walls = []
        self.coins = []
        self.ghosts = []
        self.player = None

        # מעבר על כל שורה במפה
        # אנחנו משתמשים ב-reversed כדי שציר Y יתחיל מלמטה (כמו במערכת צירים)
        for y, row in enumerate(reversed(self.level_map)):
            # מעבר על כל תא בשורה
            for x, cell in enumerate(row):
                if cell == "#":
                    # יצירת קיר
                    new_wall = Wall(x, y)
                    self.walls.append(new_wall)
                elif cell == ".":
                    # יצירת מטבע
                    new_coin = Coin(x, y)
                    self.coins.append(new_coin)
                elif cell == "P":
                    # יצירת שחקן
                    self.player = Player(x, y)
                    self.start_x = x
                    self.start_y = y
                elif cell == "G":
                    # יצירת רוח
                    new_ghost = Enemy(x, y)
                    self.ghosts.append(new_ghost)

        # אם לא נמצא שחקן במפה, ניצור אחד במרכז כברירת מחדל
        if self.player is None:
            center_x = self.width // 2
            center_y = self.height // 2
            self.player = Player(center_x, center_y)
            self.start_x = center_x
            self.start_y = center_y

    def render(self):
        """
        מדפיס את לוח המשחק למסך בצורה פשוטה.
        """
        # שלב 1: יצירת לוח ריק (גריד) מלא ברווחים
        grid = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(" ")
            grid.append(row)

        # שלב 2: הצבת קירות בלוח
        for wall in self.walls:
            x = int(wall.center_x)
            y = int(wall.center_y)
            grid[y][x] = "#"

        # שלב 3: הצבת מטבעות בלוח
        for coin in self.coins:
            x = int(coin.center_x)
            y = int(coin.center_y)
            grid[y][x] = "."

        # שלב 4: הצבת רוחות בלוח
        for ghost in self.ghosts:
            x = int(ghost.center_x)
            y = int(ghost.center_y)
            grid[y][x] = "G"

        # שלב 5: הצבת פקמן (הוא אחרון כדי שיראו אותו מעל הכל)
        x_player = int(self.player.center_x)
        y_player = int(self.player.center_y)
        grid[y_player][x_player] = "P"

        # שלב 6: הדפסת הלוח למסך
        print("\n" + "=" * (self.width + 2))

        # מדפיסים את השורות בסדר הפוך (כדי ששורה 0 תהיה למטה)
        for row in reversed(grid):
            # הופכים את רשימת התווים למחרוזת אחת
            row_string = "".join(row)
            print("|" + row_string + "|")

        print("=" * (self.width + 2))
        print(f"Score: {self.player.score} | Lives: {self.player.lives}")

    def is_wall(self, x, y):
        """בודק האם יש קיר במיקום x, y"""
        for wall in self.walls:
            if int(wall.center_x) == int(x) and int(wall.center_y) == int(y):
                return True
        return False

    def get_coin_at(self, x, y):
        """מחזיר את המטבע במיקום x, y אם יש, אחרת מחזיר None"""
        for coin in self.coins:
            if int(coin.center_x) == int(x) and int(coin.center_y) == int(y):
                return coin
        return None

    def get_ghost_at(self, x, y):
        """מחזיר את הרוח במיקום x, y אם יש, אחרת מחזיר None"""
        for ghost in self.ghosts:
            if int(ghost.center_x) == int(x) and int(ghost.center_y) == int(y):
                return ghost
        return None

    def handle_player_move(self, direction):
        """מזיז את השחקן לפי הקלט מהמשתמש"""
        dx = 0
        dy = 0

        if direction == "w":  # למעלה
            dy = 1
        elif direction == "s":  # למטה
            dy = -1
        elif direction == "a":  # שמאלה
            dx = -1
        elif direction == "d":  # ימינה
            dx = 1
        else:
            return  # מקש לא מוכר - לא עושים כלום

        # חישוב המיקום החדש הפוטנציאלי
        new_x = self.player.center_x + dx
        new_y = self.player.center_y + dy

        # בדיקה אם נתקעים בקיר
        if self.is_wall(new_x, new_y):
            return

            # עדכון המיקום בפועל
        self.player.center_x = new_x
        self.player.center_y = new_y

        # בדיקה אם אוספים מטבע
        coin = self.get_coin_at(new_x, new_y)
        if coin is not None:
            self.player.score = self.player.score + coin.value
            self.coins.remove(coin)

        # בדיקה אם מתנגשים ברוח
        ghost = self.get_ghost_at(new_x, new_y)
        if ghost is not None:
            self.player.lives = self.player.lives - 1
            print("אוי! רוח תפסה אותך.")
            self.reset_player_position()

    def reset_player_position(self):
        """מחזיר את השחקן לנקודת ההתחלה"""
        self.player.center_x = self.start_x
        self.player.center_y = self.start_y

    def move_ghosts(self):
        """מזיז את הרוחות (צעד אחד בכל תור)"""
        for ghost in self.ghosts:
            # סיכוי קטן (30%) שהרוח תשנה כיוון אקראית
            # או אם היא עומדת במקום
            if random.random() < 0.3 or (ghost.change_x == 0 and ghost.change_y == 0):
                ghost.pick_new_direction()

            # חישוב המיקום החדש
            new_x = ghost.center_x + ghost.change_x
            new_y = ghost.center_y + ghost.change_y

            # אם יש קיר - הרוח לא זזה לשם
            if self.is_wall(new_x, new_y):
                continue

            # עדכון מיקום הרוח
            ghost.center_x = new_x
            ghost.center_y = new_y

            # בדיקה אם הרוח נכנסה בשחקן
            if int(ghost.center_x) == int(self.player.center_x) and int(ghost.center_y) == int(self.player.center_y):
                self.player.lives = self.player.lives - 1
                print("אוי! רוח תפסה אותך.")
                self.reset_player_position()

    def is_game_over(self):
        """בדיקה האם המשחק נגמר (ניצחון או הפסד)"""
        if self.player.lives <= 0:
            print("Game Over - נגמרו החיים!")
            return True
        if len(self.coins) == 0:
            print("You Win - כל המטבעות נאספו!")
            return True
        return False

    def run(self):
        """לולאת המשחק הראשית"""
        print("ברוכים הבאים לפקמן!")
        print("מקשים: w=למעלה, s=למטה, a=שמאלה, d=ימינה, q=יציאה")

        while True:
            # 1. ציור הלוח
            self.render()

            # 2. בדיקת סיום
            if self.is_game_over():
                break

            # 3. קבלת קלט מהמשתמש
            command = input("לאן לזוז? ").strip().lower()

            if command == "q":
                print("להתראות!")
                break

            # 4. ביצוע תנועת שחקן
            self.handle_player_move(command)

            # 5. ביצוע תנועת רוחות
            self.move_ghosts()


# הפעלת המשחק רק אם מריצים את הקובץ הזה ישירות
if __name__ == "__main__":
    game = ConsolePacmanGame(LEVEL_MAP)
    game.run()