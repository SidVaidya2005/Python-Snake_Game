# Python Snake Game
Classic Snake game built with Python’s built-in `turtle` graphics module.

## Features
- Real-time snake movement on a 600x600 game board.
- Arrow-key controls (`Up`, `Down`, `Left`, `Right`).
- Food spawning at random positions.
- Snake growth when food is eaten.
- Score tracking with persistent high score support.
- Collision handling for walls and tail segments.

## Requirements
- Python 3
- Standard-library `turtle` module (included with most Python installations)

## How to Run
From the repository root, run:

```bash
python /home/runner/work/Python-Snake_Game/Python-Snake_Game/main.py
```

This opens a Turtle graphics window and starts the game loop.

## Controls
- `↑` Up Arrow: move up
- `↓` Down Arrow: move down
- `←` Left Arrow: move left
- `→` Right Arrow: move right

## Code Structure
- `/home/runner/work/Python-Snake_Game/Python-Snake_Game/main.py`  
  Main game loop, input binding, collision checks, and continue prompt.
- `/home/runner/work/Python-Snake_Game/Python-Snake_Game/snake.py`  
  Snake segment creation, movement, extension, reset logic, and direction guards.
- `/home/runner/work/Python-Snake_Game/Python-Snake_Game/food.py`  
  Food object and random respawn behavior.
- `/home/runner/work/Python-Snake_Game/Python-Snake_Game/scoreboard.py`  
  Score display, high-score persistence, and game-over rendering.
- `/home/runner/work/Python-Snake_Game/Python-Snake_Game/data.txt`  
  Stored high-score value.

## Gameplay Logic Overview
- The game updates in a loop (`screen.update()` + short `sleep`).
- Snake moves continuously each frame.
- On food collision:
  - Food respawns
  - Snake extends
  - Score increases
- On wall or tail collision:
  - Scoreboard resets
  - Snake resets
  - Player is prompted to continue (`yes`/`no`)

## Code Snippets

### A) Main loop + collision checks (`main.py`)
```python
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
```

### B) Snake movement (`snake.py`)
```python
def move(self):
    for seg_num in range(len(self.segments) - 1, 0, -1):
        new_x = self.segments[seg_num - 1].xcor()
        new_y = self.segments[seg_num - 1].ycor()
        self.segments[seg_num].goto(new_x,new_y)
    self.head.forward(MOVE_DISTANCE)
```

### C) Food respawn (`food.py`)
```python
def refresh(self):
    random_x = random.randint(-280,280)
    random_y = random.randint(-280,280)
    self.goto(random_x,random_y)
```

### D) High-score update on reset (`scoreboard.py`)
```python
def reset(self):
    if self.score > self.high_score:
        self.high_score = self.score
        with open('Snake Game/data.txt',mode='w') as data:
            data.write(f"{self.high_score}")

    self.score = 0
    self.update_scoreboard()
```

## Known Issues / Notes
- High-score file path in `scoreboard.py` is currently `'Snake Game/data.txt'`, while this repository stores the file at `/home/runner/work/Python-Snake_Game/Python-Snake_Game/data.txt`.
- Depending on the launch directory, high-score read/write may fail unless path handling is adjusted.
- `turtle` depends on a GUI environment; headless systems may not open the game window.

## Possible Improvements
- Fix high-score path handling using a robust path strategy (for example, paths relative to file location).
- Add restart behavior that avoids manual text input.
- Add automated tests for snake logic and score persistence.
- Add difficulty levels (speed scaling over time).
- Add a short gameplay GIF/screenshot section in the README.
