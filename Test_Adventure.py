__author__ = 'Clara'

import unittest
import adventure_map


class TestForGreatness(unittest.TestCase):

    def test_been_here_yet(self):
        self.assertTrue(adventure_map.current.discovered_yet is True)
        adventure_map.current = adventure_map.change_direction("east")
        self.assertTrue(adventure_map.current.discovered_yet is True)

    def test_change_direction(self):
        x = adventure_map.current.location
        self.assertTrue(x in adventure_map.grid)
        adventure_map.current = adventure_map.change_direction("north")
        self.assertTrue(adventure_map.current.location == x - 10)
