import unittest

from config import BoundaryMode
from game_logic import (
    boundary_outcome,
    combo_multiplier,
    level_for_score,
    normalize_combo,
    playable_bounds,
    tick_delay,
)


class GameLogicTests(unittest.TestCase):
    def test_level_progression(self):
        self.assertEqual(level_for_score(0), 1)
        self.assertEqual(level_for_score(5), 2)
        self.assertEqual(level_for_score(12), 3)

    def test_tick_delay_respects_minimum(self):
        self.assertGreaterEqual(tick_delay("fast", 1000), 0.045)

    def test_combo_multiplier_window(self):
        self.assertEqual(combo_multiplier(None), 1)
        self.assertEqual(combo_multiplier(1.0), 2)
        self.assertEqual(combo_multiplier(5.0), 1)

    def test_combo_normalization(self):
        self.assertEqual(normalize_combo(0), 1)
        self.assertEqual(normalize_combo(2), 2)
        self.assertEqual(normalize_combo(99), 3)

    def test_wall_boundary_hit(self):
        _, max_x, _, _ = playable_bounds()
        _, _, hit = boundary_outcome(max_x + 1, 0, BoundaryMode.WALL)
        self.assertTrue(hit)

    def test_wrap_boundary(self):
        min_x, max_x, _, _ = playable_bounds()
        x, y, hit = boundary_outcome(max_x + 1, 0, BoundaryMode.WRAP)
        self.assertFalse(hit)
        self.assertEqual(x, min_x)
        self.assertEqual(y, 0)


if __name__ == "__main__":
    unittest.main()
