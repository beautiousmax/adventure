__author__ = 'Clara'

import unittest
import adventure_map


class TestForGreatness(unittest.TestCase):

    def test_change_direction(self):
        adventure_map.current = adventure_map.map_squares[100]
        adventure_map.change_direction("north")
        assert adventure_map.current == adventure_map.map_squares[0]
        adventure_map.change_direction("north")
        assert adventure_map.current == adventure_map.map_squares[0]

    def test_map_coolness(self):
        assert len(adventure_map.map_squares) == 10000