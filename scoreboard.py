from turtle import Turtle

HUD_FONT = ("Courier", 15, "normal")
MESSAGE_FONT = ("Courier", 16, "normal")
TITLE_FONT = ("Courier", 20, "bold")


class Scoreboard:
    def __init__(self, high_score_store):
        self.store = high_score_store
        self.score = 0
        self.high_score = self.store.load()
        self.level = 1
        self.speed_display = 0.0
        self.lives = 0
        self.difficulty = "normal"
        self.boundary_mode = "wall"
        self.combo = 1
        self.status = ""

        self.hud_turtle = Turtle()
        self.hud_turtle.hideturtle()
        self.hud_turtle.penup()
        self.hud_turtle.color("white")
        self.hud_turtle.goto(0, 270)

        self.message_turtle = Turtle()
        self.message_turtle.hideturtle()
        self.message_turtle.penup()
        self.message_turtle.color("white")

        self.update_hud()

    def configure(self, difficulty, boundary_mode, lives):
        self.difficulty = difficulty
        self.boundary_mode = boundary_mode
        self.lives = lives
        self.update_hud()

    def set_status(self, status_text):
        self.status = status_text
        self.update_hud()

    def set_runtime(self, level, speed_display, lives, combo):
        self.level = level
        self.speed_display = speed_display
        self.lives = lives
        self.combo = combo
        self.update_hud()

    def add_points(self, points):
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score
        self.update_hud()

    def reset_round(self):
        self.score = 0
        self.level = 1
        self.combo = 1
        self.status = ""
        self.update_hud()

    def persist_high_score(self):
        self.store.save(self.high_score)

    def update_hud(self):
        self.hud_turtle.clear()
        self.hud_turtle.write(
            f"Score: {self.score}  High: {self.high_score}  Level: {self.level}  "
            f"Speed: {self.speed_display:.1f}  Lives: {self.lives}  "
            f"Diff: {self.difficulty}  Mode: {self.boundary_mode}  Combo: x{self.combo}"
            + (f"  [{self.status}]" if self.status else ""),
            align="center",
            font=HUD_FONT,
        )

    def clear_message(self):
        self.message_turtle.clear()

    def show_message(self, message, y=0, font=MESSAGE_FONT):
        self.message_turtle.clear()
        self.message_turtle.goto(0, y)
        self.message_turtle.write(message, align="center", font=font)

    def show_start_menu(self, difficulty, boundary_mode):
        self.show_message(
            "SNAKE GAME\n\n"
            "Press 1 = Slow, 2 = Normal, 3 = Fast\n"
            f"Current Difficulty: {difficulty}\n"
            f"Boundary Mode: {boundary_mode} (press M to toggle)\n\n"
            "Press ENTER to Start\n"
            "Press Q to Quit",
            y=-80,
            font=MESSAGE_FONT,
        )
        self.message_turtle.goto(0, 170)
        self.message_turtle.write("Snake Game", align="center", font=TITLE_FONT)

    def show_paused(self):
        self.show_message("PAUSED\nPress P to Resume", y=0, font=TITLE_FONT)

    def show_game_over(self):
        self.show_message("GAME OVER\nPress R to Restart or Q to Quit", y=0, font=TITLE_FONT)
