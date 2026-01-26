import heapq
from constants import TILE_SIZE


class Pathfinder:
    def __init__(self, level_map):
        self.level_map = level_map
        self.rows = len(level_map)
        self.cols = len(level_map[0])

        self.walls = set()
        for r, row in enumerate(level_map):
            for c, char in enumerate(row):
                if char == "#":
                    self.walls.add((c, r))

    def heuristic(self, a, b):
        """
        פונקציית היוריסטיקה (Manhattan Distance).
        מעריכה את המרחק בין שתי נקודות בקוים ישרים (ללא אלכסונים).
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_path(self, start_grid_pos, goal_grid_pos):
        """
        A* Algorithm implementation.
        מקבל נקודת התחלה וסיום (בקואורדינטות של רשת - שורה/עמודה)
        ומחזיר רשימה של צעדים.
        """
        # תור עדיפויות - תמיד שולף את הנתיב עם הציון המשוקלל הנמוך ביותר
        open_set = []
        heapq.heappush(open_set, (0, start_grid_pos))

        came_from = {}

        # g_score: המרחק שעברנו מההתחלה עד לנקודה הנוכחית
        g_score = {start_grid_pos: 0}

        # f_score: המרחק שעברנו + המרחק המשוער לסוף (היוריסטיקה)
        f_score = {start_grid_pos: self.heuristic(start_grid_pos, goal_grid_pos)}

        while open_set:
            # שליפת הצומת עם ה-f_score הנמוך ביותר
            current = heapq.heappop(open_set)[1]

            # אם הגענו ליעד - נשחזר את המסלול ונחזיר אותו
            if current == goal_grid_pos:
                return self.reconstruct_path(came_from, current)

            # בדיקת השכנים (למעלה, למטה, שמאלה, ימינה)
            neighbors = [
                (current[0] + 1, current[1]),  # ימינה
                (current[0] - 1, current[1]),  # שמאלה
                (current[0], current[1] + 1),  # למטה (במערך שורות גדל למטה)
                (current[0], current[1] - 1)  # למעלה
            ]

            for neighbor in neighbors:
                # בדיקה שהשכן בתוך גבולות המפה
                if 0 <= neighbor[0] < self.cols and 0 <= neighbor[1] < self.rows:
                    # בדיקה שהשכן הוא לא קיר
                    if neighbor in self.walls:
                        continue

                    # הציון החדש: המרחק עד כה + 1 (כי כל צעד הוא במרחק 1)
                    tentative_g_score = g_score[current] + 1

                    # אם מצאנו דרך קצרה יותר להגיע לשכן הזה, או שזו פעם ראשונה שמגיעים אליו
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal_grid_pos)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return []  # לא נמצא מסלול

    def reconstruct_path(self, came_from, current):
        """ משחזר את המסלול מהסוף להתחלה """
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.append(current)
        return total_path[::-1]  # הופך את הרשימה (מההתחלה לסוף)

    # --- פונקציות עזר להמרה בין פיקסלים לרשת ---

    def world_to_grid(self, x, y):
        """ המרה מפיקסלים (Arcade) לקואורדינטות רשת (שורה, עמודה) """
        col = int(x // TILE_SIZE)
        # ה-Y של Arcade הפוך מהשורות במערך, לכן החישוב הזה נדרש
        row = int(self.rows - 1 - (y // TILE_SIZE))
        return (col, row)

    def grid_to_world(self, col, row):
        """ המרה מקואורדינטות רשת למרכז המשבצת בפיקסלים """
        x = col * TILE_SIZE + TILE_SIZE / 2
        y = (self.rows - row - 1) * TILE_SIZE + TILE_SIZE / 2
        return (x, y)