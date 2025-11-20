import unittest
import numpy as np
import check_rotation


class TestCheckRotation(unittest.TestCase):

    def test_normal_triangle(self):
        vertices_set = [np.array([1, 2, 3]), np.array([4, 5, 6]), np.array([7, 8, 9.5])]
        triangle = [0, 1, 2]
        normal = check_rotation.normal_triangle(vertices_set, triangle)
        print(normal)
        self.assertTrue(np.allclose(np.array([1.5, -1.5, 0]), normal))

    def test_normal_triangle_reversed_order(self):
        vertices_set = [np.array([1, 2, 3]), np.array([4, 5, 6]), np.array([7, 8, 9.5])]
        triangle1 = [0, 1, 2]
        triangle2 = [1, 0, 2]
        normal1 = check_rotation.normal_triangle(vertices_set, triangle1)
        normal2_reversed = - check_rotation.normal_triangle(vertices_set, triangle2)
        self.assertTrue(np.allclose(normal1, normal2_reversed))

    def test_mean_normals_easy(self):
        vertices_set = [np.array([0, 0, 0]), np.array([1, 0, 0]), np.array([1, 1, 0]), np.array([0, 1, 0])]
        triangles = [[0, 1, 2], [0, 2, 3]]
        normal = check_rotation.mean_normals(vertices_set, triangles)
        self.assertTrue(np.allclose(normal, np.array([0, 0, 1])))
        self.assertTrue(np.linalg.norm(normal)==1.0)

    def test_mean_normals_non_one(self):
        vertices_set = [np.array([0, 0, 0]), np.array([7, 0, 0]), np.array([4, 3, 0]), np.array([0, 5, 0])]
        triangles = [[0, 1, 2], [0, 2, 3]]
        normal = check_rotation.mean_normals(vertices_set, triangles)
        self.assertTrue(np.linalg.norm(normal)==1.0)
        self.assertTrue(np.allclose(normal, np.array([0, 0, 1])))

    def test_mean_normals_complex(self):
        vertices_set = [np.array([1.118523, 1.143178, 7.476009]), np.array([1.131342, 1.14531 , 7.449442]), np.array([1.062269, 1.162666, 7.495965]), np.array([1.076128, 1.172289, 7.462342]), np.array([1.092419, 1.174995, 7.428558]), np.array([1.01356 , 1.181008, 7.48484 ]), np.array([1.029879, 1.192379, 7.445314])]
        triangles = [[3, 2, 0], [3, 0, 1], [3, 1, 4], [3, 5, 2], [3, 6, 5], [3, 4 ,6]]
        normal = check_rotation.mean_normals(vertices_set, triangles)
        self.assertTrue(np.linalg.norm(normal)==1.0)
        self.assertTrue(np.allclose(normal, np.array([0.36209071, 0.87203854, 0.32930093])))
    
    def test_compare_norm(self):
        initial_normal = np.array([-0.02967294, -0.79532901, -0.6054513 ])
        triangle = [0, 1, 2]
        vertices_set = [np.array([ 0.74003 , -1.365095,  8.215011]), np.array([ 0.761596, -1.349323,  8.195549]), np.array([ 0.773432, -1.372639,  8.219932])]
        order = check_rotation.compare_norm(vertices_set, initial_normal, triangle)
        self.assertTrue(np.allclose(order, triangle))

    def test_compare_norm_reverse(self):
        initial_normal = np.array([0.02967294, 0.79532901, 0.6054513 ])
        triangle = [0, 1, 2]
        vertices_set = [np.array([ 0.74003 , -1.365095,  8.215011]), np.array([ 0.761596, -1.349323,  8.195549]), np.array([ 0.773432, -1.372639,  8.219932])]
        order = check_rotation.compare_norm(vertices_set, initial_normal, triangle)
        self.assertTrue(np.allclose(order, triangle[::-1]))

if __name__ == '__main__':
    unittest.main()