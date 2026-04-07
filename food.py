from turtle import Turtle
import random

from game_logic import playable_bounds, snap_to_grid

class Food(Turtle):
    FOOD_TYPES = [
        {"name": "normal", "points": 1, "color": "blue", "weight": 70, "ttl": None, "effect": None},
        {"name": "bonus", "points": 3, "color": "gold", "weight": 15, "ttl": 6, "effect": None},
        {"name": "speed", "points": 1, "color": "red", "weight": 8, "ttl": None, "effect": "speed_up"},
        {"name": "slow", "points": 1, "color": "green", "weight": 7, "ttl": None, "effect": "slow_down"},
    ]

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_len=0.5,stretch_wid=0.5)
        self.speed("fastest")
        self.food_type = self.FOOD_TYPES[0]
        self.spawn_time = None
        self.refresh([])

    def _choose_food_type(self):
        weights = [food["weight"] for food in self.FOOD_TYPES]
        return random.choices(self.FOOD_TYPES, weights=weights, k=1)[0]

    def refresh(self, blocked_positions):
        self.food_type = self._choose_food_type()
        self.color(self.food_type["color"])
        min_x, max_x, min_y, max_y = playable_bounds()
        blocked = {(snap_to_grid(int(x)), snap_to_grid(int(y))) for x, y in blocked_positions}

        for _ in range(250):
            random_x = snap_to_grid(random.randint(int(min_x), int(max_x)))
            random_y = snap_to_grid(random.randint(int(min_y), int(max_y)))
            if (random_x, random_y) in blocked:
                continue
            self.goto(random_x, random_y)
            break
