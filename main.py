from scoreboard import Scoreboard
from turtle import Screen
from snake import Snake
from food import Food
import time
# -------------------- FUNCTIONS -------------------- #
def want_continue():
    want_to_continue = screen.textinput(title="Continue?",prompt="'yes' or 'no': ").lower()
    if want_to_continue[0] == 'n':
        global game_is_on
        game_is_on = False
        scoreboard.game_over()

# ------------------ INITIALIZATION --------------------- #
snake = Snake()
food = Food()
scoreboard = Scoreboard()
screen = Screen()

# ------------------- SCREEN ------------------------- #
screen.setup(width=600,height=600)
screen.bgcolor('black')
screen.title("Snake Game")
screen.tracer(0)

# ------------------------ CONTROLS ---------------------- #
screen.listen()
screen.onkey(snake.up,"Up")
screen.onkey(snake.down,"Down")
screen.onkey(snake.left,"Left")
screen.onkey(snake.right,"Right")

# --------------------------------- SNAKE GAME ------------------------ #
game_is_on = True

while game_is_on:
    screen.update()
    time.sleep(0.1)
    snake.move()

    # Detect Collision with Food
    if snake.head.distance(food) < 15:
        food.refresh()
        snake.extend()
        scoreboard.increase_score()

    # Detect Collision with Wall
    if snake.head.xcor() > 290 or snake.head.xcor() < -290 or\
        snake.head.ycor() > 270 or snake.head.ycor() < -280:
        scoreboard.reset()
        snake.reset()
        want_continue()

    # Detect Collision with Tail
    for segment in snake.segments[1:]:
        if snake.head.distance(segment) < 10:
            scoreboard.reset()
            snake.reset()
            want_continue()

screen.exitonclick()
