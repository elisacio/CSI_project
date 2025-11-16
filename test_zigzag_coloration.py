import unittest
from zigzag_coloration import draw_zigzag, retriangulation


class TestZigzagColoration(unittest.TestCase):

    def test_square(self):
        square = [1,2,3,4]
        results_triangles = [[1,2,3], [4,1,3]]
        results_colors = [0,1]
        new_triangles, colors = draw_zigzag(square)
        self.assertEqual(new_triangles, results_triangles, f"The zizag was not drawn properly on the square of vertices {square}.")
        self.assertEqual(colors,results_colors,f"The coloration was not done properly on the square of vertices {square}.")

    def test_pentagon(self):
        patch = [1,2,3,4,5]
        results_triangles = [[1,2,3], [3,4,5], [5,1,3]]
        results_colors = [0,0,1]
        new_triangles, colors = draw_zigzag(patch)
        self.assertEqual(new_triangles, results_triangles, f"The zizag was not drawn properly on the pentagon of vertices {patch}.")
        self.assertEqual(colors,results_colors,f"The coloration was not done properly on the pentagon of vertices {patch}.")

    def test_hexagon(self):
        patch = [1,2,3,4,5,6]
        results_triangles = [[1,2,3], [3,4,6], [4,5,6], [6,1,3]]
        results_colors = [0,1,0,1]
        new_triangles, colors = draw_zigzag(patch)
        self.assertEqual(new_triangles, results_triangles, f"The zizag was not drawn properly on the hexagon of vertices {patch}.")
        self.assertEqual(colors,results_colors,f"The coloration was not done properly on the hexagon of vertices {patch}.")

    def test_heptagon(self):
        patch = [1,2,3,4,5,6,7]
        results_triangles = [[1,2,3], [3,4,7], [4,5,6], [6,7,4], [7,1,3]]
        results_colors = [0,1,0,1,1]
        new_triangles, colors = draw_zigzag(patch)
        self.assertEqual(new_triangles, results_triangles, f"The zizag was not drawn properly on the heptagon of vertices {patch}.")
        self.assertEqual(colors,results_colors,f"The coloration was not done properly on the heptagon of vertices {patch}.")

    def test_octogon(self):
        patch = [1,2,3,4,5,6,7,8]
        results_triangles = [[1,2,3], [3,4,8], [4,5,7], [5,6,7], [7,8,4], [8,1,3]]
        results_colors = [0,1,1,0,1,1]
        new_triangles, colors = draw_zigzag(patch)
        self.assertEqual(new_triangles, results_triangles, f"The zizag was not drawn properly on the octogon of vertices {patch}.")
        self.assertEqual(colors,results_colors,f"The coloration was not done properly on the octogon of vertices {patch}.")

    def test_9gon(self):
        patch = [1,2,3,4,5,6,7,8,9]
        results_triangles = [[1,2,3], [3,4,9], [4,5,8], [5,6,7], [7,8,5], [8,9,4], [9,1,3]]
        results_colors = [0,1,1,0,1,1,1]
        new_triangles, colors = draw_zigzag(patch)
        self.assertEqual(new_triangles, results_triangles, f"The zizag was not drawn properly on the 9-gon of vertices {patch}.")
        self.assertEqual(colors,results_colors,f"The coloration was not done properly on the 9-gon of vertices {patch}.")

    def test_12gon(self):
        patch = [1,2,3,4,5,6,7,8,9,10,11,12]
        results_triangles = [[1,2,3], [3,4,12], [4,5,11], [5,6,10], [6,7,9], [7,8,9], [9,10,6], [10,11,5], [11,12,4], [12,1,3]]
        results_colors = [0,1,1,1,1,0,1,1,1,1]
        new_triangles, colors = draw_zigzag(patch)
        self.assertEqual(new_triangles, results_triangles, f"The zizag was not drawn properly on the 12-gon of vertices {patch}.")
        self.assertEqual(colors,results_colors,f"The coloration was not done properly on the 12-gon of vertices {patch}.")

    def test_15gon(self):
        patch = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        results_triangles = [[1,2,3], [3,4,15], [4,5,14], [5,6,13], [6,7,12], [7,8,11], [8,9,10], [10,11,8], [11,12,7], [12,13,6], [13,14,5], [14,15,4],[15,1,3]]
        results_colors = [0,1,1,1,1,1,0,1,1,1,1,1,1]
        new_triangles, colors = draw_zigzag(patch)
        self.assertEqual(new_triangles, results_triangles, f"The zizag was not drawn properly on the 15-gon of vertices {patch}.")
        self.assertEqual(colors,results_colors,f"The coloration was not done properly on the 15-gon of vertices {patch}.")

    def test_20gon(self):
        patch = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
        results_triangles = [[1,2,3], [3,4,20], [4,5,19], [5,6,18], [6,7,17], [7,8,16], [8,9,15], [9,10,14], [10,11,13], [11,12,13], [13,14,10], [14,15,9],[15,16,8], [16,17,7], [17,18,6],[18,19,5],[19,20,4],[20,1,3]]
        results_colors = [0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1]
        new_triangles, colors = draw_zigzag(patch)
        self.assertEqual(new_triangles, results_triangles, f"The zizag was not drawn properly on the 20-gon of vertices {patch}.")
        self.assertEqual(colors,results_colors,f"The coloration was not done properly on the 20-gon of vertices {patch}.")

class TestRetriangulation(unittest.TestCase):
    def test_retriangulation_0(self):
        patches = []
        results_patches, results_colors = retriangulation(patches)
        self.assertEqual([], results_patches, f"The retriangulation didn't work on the empty list of patches.")
        self.assertEqual([],results_colors, f"The coloration didn't work on the empty list of patches.")

    def test_retriangulation_1(self):
        patches = [[1,2,3,4,5,6]]
        results_patches, results_colors = retriangulation(patches)
        expected_retriangulation = [[[1,2,3], [3,4,6], [4,5,6], [6,1,3]]]
        expected_coloration = [[0,1,0,1]]
        self.assertEqual(results_patches, expected_retriangulation,  f"The retriangulation didn't work on the list of patches containing 1 patch.")
        self.assertEqual(results_colors, expected_coloration, f"The coloration didn't work on the list of patches containing 1 patch.")

    def test_retriangulation_2(self):
        patches = [[1,2,3,4,5,6], [7,8,9,10,11]]
        results_patches, results_colors = retriangulation(patches)
        expected_retriangulation = [[[1,2,3], [3,4,6], [4,5,6], [6,1,3]], [[7,8,9], [9,10,11], [11,7,9]]]
        expected_coloration = [[0,1,0,1], [0,0,1]]
        self.assertEqual(results_patches, expected_retriangulation, f"The retriangulation didn't work on the list of patches containing 2 patches.")
        self.assertEqual(results_colors, expected_coloration, f"The coloration didn't work on the list of patches containing 2 patches.")

    def test_retriangulation_3(self):
        patches = [[1,2,3,4,5,6], [7,8,9,10,11], [12,13,14,15,16,17]]
        results_patches, results_colors = retriangulation(patches)
        expected_retriangulation = [[[1,2,3], [3,4,6], [4,5,6], [6,1,3]], [[7,8,9], [9,10,11], [11,7,9]], [[12,13,14], [14,15,17], [15,16,17], [17,12,14]]]
        expected_coloration = [[0,1,0,1], [0,0,1], [0,1,0,1]]
        self.assertEqual(results_patches, expected_retriangulation, f"The retriangulation didn't work on the list of patches containing 3 patches.")
        self.assertEqual(results_colors, expected_coloration, f"The coloration didn't work on the list of patches containing 3 patches.")


if __name__ == '__main__':
    unittest.main()