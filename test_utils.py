import unittest
import numpy as np
from utils import shape_centroid


class TestUtils(unittest.TestCase):
    
    # Add test and do exception fail for empty set on shape_centroid

    def test_shape_centroid_single_point(self):
        vertices_set = [np.array([3.0, -2.0, 5.5])]
        self.assertAlmostEqual(list(shape_centroid(vertices_set)), list(vertices_set[0]), 'Test function shape_centroid failed for single point.')
    
    def test_shape_centroid_midpoint(self):
        vertices_set = [np.array([0.0, 0.0, 0.0]), np.array([2.0, 4.0, 6.0])]
        middle = np.array([1.0, 2.0, 3.0])
        self.assertAlmostEqual(list(shape_centroid(vertices_set)), list(middle), 'Test function shape_centroid failed for midpoint.')


if __name__ == '__main__':
    unittest.main()