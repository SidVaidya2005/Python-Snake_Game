import random
from turtle import Turtle

from config import GRID_SIZE, MAX_OBSTACLES, OBSTACLE_SCORE_STEP
from game_logic import playable_bounds, snap_to_grid


class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def clear(self):
        for obstacle in self.obstacles:
            obstacle.hideturtle()
        self.obstacles.clear()

    def _blocked_keys(self, blocked_positions):
        return {(snap_to_grid(int(x)), snap_to_grid(int(y))) for x, y in blocked_positions}

    def _spawn_obstacle(self, blocked):
        min_x, max_x, min_y, max_y = playable_bounds()
        for _ in range(200):
            x = snap_to_grid(random.randint(int(min_x), int(max_x)))
            y = snap_to_grid(random.randint(int(min_y), int(max_y)))
            key = (x, y)
            if key in blocked:
                continue
            obstacle = Turtle(shape="square")
            obstacle.penup()
            obstacle.color("gray")
            obstacle.goto(x, y)
            self.obstacles.append(obstacle)
            blocked.add(key)
            return

    def refresh_for_score(self, score, blocked_positions):
        target_count = min(MAX_OBSTACLES, score // OBSTACLE_SCORE_STEP)
        blocked = self._blocked_keys(blocked_positions)
        while len(self.obstacles) < target_count:
            self._spawn_obstacle(blocked)
