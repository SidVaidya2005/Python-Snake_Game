from enum import Enum


class GameState(str, Enum):
    START = "start"
    RUNNING = "running"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    EXIT = "exit"


class BoundaryMode(str, Enum):
    WALL = "wall"
    WRAP = "wrap"


SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
HALF_WIDTH = SCREEN_WIDTH // 2
HALF_HEIGHT = SCREEN_HEIGHT // 2
GRID_SIZE = 20
PLAYABLE_MARGIN = 20

DIFFICULTY_DELAYS = {
    "slow": 0.14,
    "normal": 0.10,
    "fast": 0.075,
}

DEFAULT_DIFFICULTY = "normal"
DEFAULT_BOUNDARY_MODE = BoundaryMode.WALL

MIN_DELAY = 0.045
SPEEDUP_EVERY_POINTS = 5
SPEEDUP_STEP = 0.004

DEFAULT_LIVES = 3
COMBO_WINDOW_SECONDS = 2.0
MAX_COMBO_MULTIPLIER = 3

OBSTACLE_SCORE_STEP = 5
MAX_OBSTACLES = 8
