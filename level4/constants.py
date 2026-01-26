WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Pacman Nitzanim"
TILE_SIZE = 32
MOVEMENT_SPEED = 4
LEVEL_MAP = []


try:
    with open("config.txt", "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line:
                key, value = line.strip().split("=", 1)

                if key == "WINDOW_WIDTH":
                    WINDOW_WIDTH = int(value)
                elif key == "WINDOW_HEIGHT":
                    WINDOW_HEIGHT = int(value)
                elif key == "WINDOW_TITLE":
                    WINDOW_TITLE = value
                elif key == "TILE_SIZE":
                    TILE_SIZE = int(value)
                elif key == "MOVEMENT_SPEED":
                    MOVEMENT_SPEED = int(value)
    print("Configuration loaded successfully.")
except FileNotFoundError:
    print("Error: config.txt not found. Using default values.")

try:
    with open("level_map.txt", "r", encoding="utf-8") as f:
        LEVEL_MAP = [line.rstrip('\n') for line in f]
    print("Level map loaded successfully.")
except FileNotFoundError:
    print("Error: level_map.txt not found.")