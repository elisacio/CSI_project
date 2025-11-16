import unittest
import numpy as np # pyright: ignore[reportMissingImports]
from check_rotation import newell, check_rotation


class TestCheckRotation(unittest.TestCase):

    def test_newell_basic_triangle(self):
        poly = [np.array([0.0, 0.0, 0.0]), np.array([2.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0])]
        order = [0, 1, 2]
        n = newell(poly, order)
        real_normal = np.array([0.0, 0.0, 1.0])
        self.assertTrue(np.allclose(n, real_normal))

    def test_newell_basic_triangle_reversed(self):
        poly = [np.array([0.0, 0.0, 0.0]), np.array([2.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0])]
        order1 = [0, 1, 2]
        order2 = [1, 2, 0]
        n1 = list(newell(poly, order1))
        n2 = list(newell(poly, order2))
        self.assertTrue(np.allclose(n1, n2))
    
    def test_newell_square(self):
        poly = [np.array([0,0,0]), np.array([1,0,0]), np.array([1,0.707,0.707]), np.array([0,0.707,0.707])]
        order = [2, 3, 0, 1]
        n = newell(poly, order)
        self.assertTrue(np.allclose(n, np.array([0.0, -0.70710678, 0.70710678])))
    
    # Test give more vertices than necessary
    def test_newell_too_much(self):
        poly = [np.array([2.0, 1.0, 3.0]), np.array([0,0,0]), np.array([1,0,0]), np.array([3.0, 4.6, 9.8]), np.array([1,0.707,0.707]), np.array([0,0.707,0.707]), np.array([3.8, 9.4, 20.3])]
        order = [4, 5, 1, 2]
        n = newell(poly, order)
        self.assertTrue(np.allclose(n, np.array([0.0, -0.70710678, 0.70710678])))

    def test_newell_poly(self):
        poly = [np.array([-0.04109151,  0.034006  , -0.01199754]), np.array([-0.03519913,  0.03383521, -0.02050829]), np.array([-0.03158981,  0.03559233, -0.01920415]), np.array([-0.03340734,  0.03757704, -0.01615819]), np.array([-0.0380666 ,  0.0385186 , -0.00730796]), np.array([-0.0396703 ,  0.036174  , -0.00733977])]
        order =   [0, 1, 2, 3, 4, 5]
        n = newell(poly, order)
        self.assertTrue(np.allclose(n, np.array([0.54319425, -0.74662997,  0.38403607])))

    def test_check_rotation_poly_reverse(self):
        poly = [np.array([-0.04109151,  0.034006  , -0.01199754]), np.array([-0.03519913,  0.03383521, -0.02050829]), np.array([-0.03158981,  0.03559233, -0.01920415]), np.array([-0.03340734,  0.03757704, -0.01615819]), np.array([-0.0380666 ,  0.0385186 , -0.00730796]), np.array([-0.0396703 ,  0.036174  , -0.00733977])]
        order =   [0, 1, 2, 3, 4, 5]
        centroid_shape = np.array([-0.02803571, 0.09421553, 0.00904955])
        order_final = check_rotation(poly, order, centroid_shape)
        self.assertTrue(np.allclose(order, order_final[::-1]))

    def test_check_rotation_square_normal(self):
        '''order:  [1516, 2126, 2093, 2129]
        centroid shape:  [-0.02803571  0.09421553  0.00904955]
        polygon:  [array([-0.03922792,  0.09918463, -0.02191272]), array([-0.03320232,  0.1057832 , -0.02064759]), array([-0.03798766,  0.10751453, -0.01997576]), array([-0.04177183,  0.10396706, -0.02083294])]
        normal:  [ 0.02777339 -0.23032234  0.97271798]
        dot_product:  -0.03163380941082107'''
        poly = [np.array([-0.03922792,  0.09918463, -0.02191272]), np.array([-0.03320232,  0.1057832 , -0.02064759]), np.array([-0.03798766,  0.10751453, -0.01997576]), np.array([-0.04177183,  0.10396706, -0.02083294])]
        order = [0, 1, 2, 3]
        centroid_shape = np.array([-0.02803571, 0.09421553, 0.00904955])
        order_final = check_rotation(poly, order, centroid_shape)
        self.assertTrue(np.allclose(order, order_final))

if __name__ == '__main__':
    unittest.main()