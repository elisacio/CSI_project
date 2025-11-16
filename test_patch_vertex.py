#!/usr/bin/env python

import obja
import numpy as np
import sys
import networkx as nx
from check_rotation import check_rotation
import unittest
import utils
from obja import Face

from patch_vertex import patch_vertex, ordonnement, couple_index_face



class TestStringMethods(unittest.TestCase):

    def test_empty(self):
        patchs, operations = patch_vertex([], [], [], [])
        self.assertEqual(patchs, set())
        self.assertEqual(operations, [])

    def test_cube(self):
        patchs, operations = patch_vertex([1,6], [], [[2,2,2],[0,0,1],[0,1,1],[0,1,0],[0,0,0],[1,1,1],[1,1,0],[1,0,0],[1,0,1]], [Face(1,2,4),Face(2,3,4),Face(2,5,3),Face(3,5,6), Face(5,8,6), Face(6,7,8),Face(1,4,8),Face(4,7,8),Face(3,4,6),Face(4,6,7),Face(1,2,5),Face(1,5,8)])
        self.assertEqual(patchs, {(4, 7, 8, 5, 3), (5, 8, 4, 2)})
        self.assertListEqual(operations, [('face', 0, Face(1, 2, 4)), ('face', 6, Face(1, 4, 8)), ('face', 10, Face(1, 2, 5)), ('face', 11, Face(1, 5, 8)), ('vertex', 1, [0, 0, 1]), ('face', 3, Face(3, 5, 6)), ('face', 4, Face(5, 8, 6)), ('face', 5, Face(6, 7, 8)), ('face', 8, Face(3, 4, 6)), ('face', 9, Face(4, 6, 7)), ('vertex', 6, [1, 1, 0])])


if __name__ == '__main__':
    unittest.main()