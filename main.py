import time
from turtle import Screen

from config import (
    DEFAULT_BOUNDARY_MODE,
    DEFAULT_DIFFICULTY,
    DEFAULT_LIVES,
    GRID_SIZE,
    HALF_HEIGHT,
    HALF_WIDTH,
    GameState,
    BoundaryMode,
)
from food import Food
from game_logic import boundary_outcome, combo_multiplier, level_for_score, normalize_combo, tick_delay
from high_score_store import HighScoreStore
from obstacles import ObstacleManager
from scoreboard import Scoreboard
from snake import Snake


class SnakeGame:
    def __init__(self):
        self.screen = Screen()
        self.screen.setup(width=HALF_WIDTH * 2, height=HALF_HEIGHT * 2)
        self.screen.bgcolor("black")
        self.screen.title("Snake Game")
        self.screen.tracer(0)

        self.snake = Snake()
        self.food = Food()
        self.obstacles = ObstacleManager()
        self.scoreboard = Scoreboard(HighScoreStore())

        self.state = GameState.START
        self.difficulty = DEFAULT_DIFFICULTY
        self.boundary_mode = DEFAULT_BOUNDARY_MODE
        self.lives = DEFAULT_LIVES
        self.combo_streak = 1
        self.last_food_time = None
        self.speed_modifier = 0.0

        self._bind_keys()
        self._setup_start_screen()

    def _bind_keys(self):
        self.screen.listen()
        self.screen.onkey(self.snake.up, "Up")
        self.screen.onkey(self.snake.down, "Down")
        self.screen.onkey(self.snake.left, "Left")
        self.screen.onkey(self.snake.right, "Right")
        self.screen.onkey(self.toggle_pause, "p")
        self.screen.onkey(self.restart_game, "r")
        self.screen.onkey(self.quit_game, "q")
        self.screen.onkey(self.start_game, "Return")
        self.screen.onkey(self.set_slow, "1")
        self.screen.onkey(self.set_normal, "2")
        self.screen.onkey(self.set_fast, "3")
        self.screen.onkey(self.toggle_boundary_mode, "m")

    def _blocked_positions(self):
        snake_positions = [segment.position() for segment in self.snake.segments]
        obstacle_positions = [ob.position() for ob in self.obstacles.obstacles]
        return snake_positions + obstacle_positions

    def _setup_start_screen(self):
        self.scoreboard.configure(self.difficulty, self.boundary_mode.value, self.lives)
        self.scoreboard.set_status("start")
        self.scoreboard.show_start_menu(self.difficulty, self.boundary_mode.value)
        self.food.hideturtle()

    def set_slow(self):
        if self.state == GameState.START:
            self.difficulty = "slow"
            self._setup_start_screen()

    def set_normal(self):
        if self.state == GameState.START:
            self.difficulty = "normal"
            self._setup_start_screen()

    def set_fast(self):
        if self.state == GameState.START:
            self.difficulty = "fast"
            self._setup_start_screen()

    def toggle_boundary_mode(self):
        if self.state == GameState.START:
            self.boundary_mode = (
                BoundaryMode.WRAP if self.boundary_mode == BoundaryMode.WALL else BoundaryMode.WALL
            )
            self._setup_start_screen()

    def start_game(self):
        if self.state not in (GameState.START, GameState.GAME_OVER):
            return
        self.state = GameState.RUNNING
        self.scoreboard.clear_message()
        self.scoreboard.set_status("running")
        self.food.showturtle()
        self.food.refresh(self._blocked_positions())
        self.last_food_time = None
        self.combo_streak = 1

    def restart_game(self):
        if self.state not in (GameState.GAME_OVER, GameState.RUNNING, GameState.PAUSED):
            return
        self.scoreboard.persist_high_score()
        self.snake.reset()
        self.obstacles.clear()
        self.lives = DEFAULT_LIVES
        self.speed_modifier = 0.0
        self.combo_streak = 1
        self.last_food_time = None
        self.scoreboard.reset_round()
        self.scoreboard.configure(self.difficulty, self.boundary_mode.value, self.lives)
        self.food.refresh(self._blocked_positions())
        self.food.showturtle()
        self.state = GameState.RUNNING
        self.scoreboard.set_status("running")
        self.scoreboard.clear_message()

    def quit_game(self):
        self.scoreboard.persist_high_score()
        self.state = GameState.EXIT

    def toggle_pause(self):
        if self.state == GameState.RUNNING:
            self.state = GameState.PAUSED
            self.scoreboard.set_status("paused")
            self.scoreboard.show_paused()
        elif self.state == GameState.PAUSED:
            self.state = GameState.RUNNING
            self.scoreboard.set_status("running")
            self.scoreboard.clear_message()

    def _on_food_eaten(self):
        now = time.time()
        elapsed = None if self.last_food_time is None else now - self.last_food_time
        self.last_food_time = now
        if combo_multiplier(elapsed) > 1:
            self.combo_streak += 1
        else:
            self.combo_streak = 1
        combo = normalize_combo(self.combo_streak)

        points = self.food.food_type["points"] * combo
        self.scoreboard.add_points(points)
        self.snake.extend()

        effect = self.food.food_type["effect"]
        if effect == "speed_up":
            self.speed_modifier = max(-0.02, self.speed_modifier - 0.006)
        elif effect == "slow_down":
            self.speed_modifier = min(0.03, self.speed_modifier + 0.006)

        self.obstacles.refresh_for_score(self.scoreboard.score, self._blocked_positions())
        self.food.refresh(self._blocked_positions())

    def _lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            self.state = GameState.GAME_OVER
            self.scoreboard.set_status("game over")
            self.scoreboard.show_game_over()
            self.scoreboard.persist_high_score()
            return

        self.snake.reset()
        self.food.refresh(self._blocked_positions())
        self.scoreboard.set_status("life lost")

    def _check_collisions(self):
        # Food collision
        if self.snake.head.distance(self.food) < 15:
            self._on_food_eaten()

        # Wall/wrap boundary
        x, y = self.snake.head.xcor(), self.snake.head.ycor()
        next_x, next_y, hit_wall = boundary_outcome(x, y, self.boundary_mode)
        if hit_wall:
            self._lose_life()
            return
        if self._did_wrap(x, y, next_x, next_y):
            self.snake.set_head_position(next_x, next_y)

        # Tail collision
        for segment in self.snake.segments[1:]:
            if self.snake.head.distance(segment) < 10:
                self._lose_life()
                return

        # Obstacle collision
        for obstacle in self.obstacles.obstacles:
            if self.snake.head.distance(obstacle) < 14:
                self._lose_life()
                return

    def _update_hud_runtime(self, delay):
        level = level_for_score(self.scoreboard.score)
        speed_display = round(1.0 / delay, 1) if delay > 0 else 0.0
        combo = normalize_combo(self.combo_streak)
        self.scoreboard.set_runtime(level, speed_display, self.lives, combo)

    @staticmethod
    def _did_wrap(previous_x, previous_y, next_x, next_y):
        # Wrapping teleports across the board and therefore exceeds one grid step.
        return abs(next_x - previous_x) > GRID_SIZE or abs(next_y - previous_y) > GRID_SIZE

    def run(self):
        while self.state != GameState.EXIT:
            self.screen.update()
            if self.state == GameState.RUNNING:
                delay = tick_delay(
                    difficulty=self.difficulty,
                    score=self.scoreboard.score,
                    speed_modifier=self.speed_modifier,
                )
                self._update_hud_runtime(delay)
                self.snake.move()
                self._check_collisions()
                time.sleep(delay)
            else:
                time.sleep(0.03)

        self.screen.bye()


if __name__ == "__main__":
    SnakeGame().run()
