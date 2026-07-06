import unittest

from sousvide.haccp import cook_safety


class HaccpTests(unittest.TestCase):
    def test_held_long_enough_passes(self):
        r = [{"t": 0, "temp_c": 55}, {"t": 90, "temp_c": 55}]
        self.assertTrue(cook_safety(r, 54.4, 90)["pass"])

    def test_too_short_fails(self):
        r = [{"t": 0, "temp_c": 55}, {"t": 30, "temp_c": 55}]
        self.assertFalse(cook_safety(r, 54.4, 90)["pass"])

    def test_dip_below_threshold_resets_the_clock(self):
        r = [{"t": 0, "temp_c": 55}, {"t": 40, "temp_c": 50}, {"t": 50, "temp_c": 55}, {"t": 80, "temp_c": 55}]
        # after the dip at t=40 the run restarts at t=50; longest contiguous hold = 30 < 90
        self.assertFalse(cook_safety(r, 54.4, 90)["pass"])

    def test_reports_held_minutes(self):
        r = [{"t": 0, "temp_c": 55}, {"t": 90, "temp_c": 55}]
        self.assertEqual(cook_safety(r, 54.4, 90)["held_minutes"], 90)


if __name__ == "__main__":
    unittest.main()
