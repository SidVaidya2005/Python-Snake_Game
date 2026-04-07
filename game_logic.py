from config import (
    COMBO_WINDOW_SECONDS,
    DIFFICULTY_DELAYS,
    GRID_SIZE,
    HALF_HEIGHT,
    HALF_WIDTH,
    MAX_COMBO_MULTIPLIER,
    MIN_DELAY,
    PLAYABLE_MARGIN,
    SPEEDUP_EVERY_POINTS,
    SPEEDUP_STEP,
    BoundaryMode,
)


def playable_bounds():
    max_x = HALF_WIDTH - PLAYABLE_MARGIN
    max_y = HALF_HEIGHT - PLAYABLE_MARGIN
    return -max_x, max_x, -max_y, max_y


def snap_to_grid(value: int) -> int:
    return round(value / GRID_SIZE) * GRID_SIZE


def level_for_score(score: int) -> int:
    return 1 + (max(score, 0) // SPEEDUP_EVERY_POINTS)


def tick_delay(difficulty: str, score: int, speed_modifier: float = 0.0) -> float:
    base = DIFFICULTY_DELAYS.get(difficulty, DIFFICULTY_DELAYS["normal"])
    level_drop = (score // SPEEDUP_EVERY_POINTS) * SPEEDUP_STEP
    return max(MIN_DELAY, base - level_drop + speed_modifier)


def combo_multiplier(seconds_since_last_food: float | None) -> int:
    if seconds_since_last_food is None:
        return 1
    if seconds_since_last_food <= COMBO_WINDOW_SECONDS:
        return 2
    return 1


def normalize_combo(combo_streak: int) -> int:
    return min(MAX_COMBO_MULTIPLIER, max(1, combo_streak))


def boundary_outcome(x: float, y: float, mode: BoundaryMode):
    min_x, max_x, min_y, max_y = playable_bounds()
    if mode == BoundaryMode.WALL:
        hit_wall = x < min_x or x > max_x or y < min_y or y > max_y
        return x, y, hit_wall

    wrapped_x = x
    wrapped_y = y
    if x < min_x:
        wrapped_x = max_x
    elif x > max_x:
        wrapped_x = min_x

    if y < min_y:
        wrapped_y = max_y
    elif y > max_y:
        wrapped_y = min_y

    return wrapped_x, wrapped_y, False
