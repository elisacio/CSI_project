import unittest
import numpy as np
import utils
from decimate import Decimater
import obja


class TestUtils(unittest.TestCase):
    
    def test_flatten_empty(self):
        liste = []
        self.assertTrue(utils.flatten(liste)==[])

    def test_flatten_integers(self):
        liste = [[2, 3, 8], [20, 65, 3], [40, 10, 5]]
        flatten_liste = utils.flatten(liste)
        expected = [2, 3, 8, 20, 65, 3, 40, 10, 5]
        self.assertTrue(all(flatten_liste[i] == expected[i] for i in range(len(expected))))

    def test_flatten_float(self):
        liste = [[40.9, 3.60, 9.37], [0.0, 3.6], [40.74, 10.14, 15.67]]
        flatten_liste = utils.flatten(liste)
        expected = [40.9, 3.60, 9.37, 0.0, 3.6, 40.74, 10.14, 15.67]
        self.assertTrue(all(flatten_liste[i] == expected[i] for i in range(len(expected))))

    def test_flatten_string(self):
        liste = [["40", "complex"], ["cent", "dix", "cinq"]]
        flatten_liste = utils.flatten(liste)
        expected = ["40", "complex", "cent", "dix", "cinq"]
        self.assertTrue(all(flatten_liste[i] == expected[i] for i in range(len(expected))))

    def test_rotate_till_first_empty(self):
        liste = []
        target = 0
        expected = []
        rotated = utils.rotate_until_first(liste, target)
        self.assertTrue(liste == expected)

    def test_rotate_till_first_easy(self):
        liste = [3, 2, 0, 5]
        target = 0
        expected = [0, 5, 3, 2]
        rotated = utils.rotate_until_first(liste, target)
        self.assertTrue(all(rotated[i] == expected[i] for i in range(len(expected))))

    def test_rotate_till_first_wrong(self):
        liste = [3, 2, 0, 5]
        target = 10
        expected = [3, 2, 0, 5]
        rotated = utils.rotate_until_first(liste, target)
        self.assertTrue(all(rotated[i] == expected[i] for i in range(len(expected))))

    def test_face_from_vertex_empty(self):
        expected = []
        model = Decimater()
        vertex_index = 10
        face = utils.face_from_vertex(model, vertex_index)
        self.assertTrue(face == expected)

    def test_single_triangle(self):
        model = Decimater()
        model.vertices.append(np.array([0.0, 0.0, 0.0]))
        model.vertices.append(np.array([1.0, 0.0, 0.0]))
        model.vertices.append(np.array([0.0, 1.0, 0.0]))
        model.faces.append(obja.Face(0, 1, 2))
        
        vertex_index = 2
        face = utils.face_from_vertex(model, vertex_index)
        expected = [0]
        self.assertTrue(face == expected)

    def test_single_multiple_triangles(self):
        model = Decimater()
        vertices = [np.array([2.0, 0.0, 0.0]), np.array([2.0, 3.0, 0.75]), np.array([0.0, 3.0, 0.0]), np.array([0.0, 0.0, 1.25]), np.array([1.36, 1.89, 0.0])]
        model.vertices.extend(vertices)
        faces = [obja.Face(0, 1, 4), obja.Face(1, 2, 4), obja.Face(0, 4, 3), obja.Face(4, 2, 3)]
        model.faces.extend(faces)
        
        vertex_index = 4
        vertex_faces = utils.face_from_vertex(model, vertex_index)
        expected = [0, 1, 2, 3]
        self.assertTrue(all(vertex_faces[i] == expected[i] for i in range(len(vertex_faces))))

    def test_single_multiple_triangles_bis(self):
        model = Decimater()
        vertices = [np.array([2.0, 0.0, 0.0]), np.array([2.0, 3.0, 0.75]), np.array([0.0, 3.0, 0.0]), np.array([0.0, 0.0, 1.25]), np.array([1.36, 1.89, 0.0])]
        model.vertices.extend(vertices)
        faces = [obja.Face(0, 1, 4), obja.Face(1, 2, 4), obja.Face(0, 4, 3), obja.Face(4, 2, 3)]
        model.faces.extend(faces)
        
        vertex_index = 2
        vertex_faces = utils.face_from_vertex(model, vertex_index)
        expected = [1, 3]
        self.assertTrue(all(vertex_faces[i] == expected[i] for i in range(len(vertex_faces))))

    def test_equal_easy(self):
        face = obja.Face(3, 10, 0)
        triangle = [3, 10, 0]
        self.assertTrue(utils.equal(face, triangle))

    def test_equal_complex(self):
        face = obja.Face(56, 30, 4)
        triangle = [4, 30, 56]
        self.assertTrue(utils.equal(face, triangle))

    def test_equal_wrong(self):
        face = obja.Face(56, 30, 4)
        triangle = [4, 10, 56]
        self.assertFalse(utils.equal(face, triangle))

    def test_equal_bis(self):
        face = obja.Face(56, 30, 4)
        triangle = [6, 10, 20]
        self.assertFalse(utils.equal(face, triangle))
    
    def test_face_already_exist_empty(self):
        model = Decimater()
        triangle = [1, 4, 2]
        self.assertFalse(utils.face_already_exist(model, triangle))

    def test_face_already_exist_complex(self):
        model = Decimater()
        vertices = [np.array([2.0, 0.0, 0.0]), np.array([2.0, 3.0, 0.75]), np.array([0.0, 3.0, 0.0]), np.array([0.0, 0.0, 1.25]), np.array([1.36, 1.89, 0.0])]
        model.vertices.extend(vertices)
        faces = [obja.Face(0, 1, 4), obja.Face(1, 2, 4), obja.Face(0, 4, 3), obja.Face(4, 2, 3)]
        model.faces.extend(faces)

        triangle = [1, 4, 2]
        self.assertTrue(utils.face_already_exist(model, triangle))

    def test_face_already_exist_complex_wrong(self):
        model = Decimater()
        vertices = [np.array([2.0, 0.0, 0.0]), np.array([2.0, 3.0, 0.75]), np.array([0.0, 3.0, 0.0]), np.array([0.0, 0.0, 1.25]), np.array([1.36, 1.89, 0.0])]
        model.vertices.extend(vertices)
        faces = [obja.Face(0, 1, 4), obja.Face(1, 2, 4), obja.Face(0, 4, 3), obja.Face(4, 2, 3)]
        model.faces.extend(faces)

        triangle = [3, 2, 0]
        self.assertFalse(utils.face_already_exist(model, triangle))

    def test_face_already_exist_deleted(self):
        model = Decimater()
        vertices = [np.array([2.0, 0.0, 0.0]), np.array([2.0, 3.0, 0.75]), np.array([0.0, 3.0, 0.0]), np.array([0.0, 0.0, 1.25]), np.array([1.36, 1.89, 0.0])]
        model.vertices.extend(vertices)
        faces = [obja.Face(0, 1, 4), obja.Face(1, 2, 4), obja.Face(0, 4, 3), obja.Face(4, 2, 3)]
        model.faces.extend(faces)
        model.deleted_faces.add(0) 
        model.deleted_faces.add(3)

        triangle = [2, 1, 4]
        self.assertTrue(utils.face_already_exist(model, triangle))
    
    def test_face_already_exist_deleted_wrong(self):
        model = Decimater()
        vertices = [np.array([2.0, 0.0, 0.0]), np.array([2.0, 3.0, 0.75]), np.array([0.0, 3.0, 0.0]), np.array([0.0, 0.0, 1.25]), np.array([1.36, 1.89, 0.0])]
        model.vertices.extend(vertices)
        faces = [obja.Face(0, 1, 4), obja.Face(1, 2, 4), obja.Face(0, 4, 3), obja.Face(4, 2, 3)]
        model.faces.extend(faces)
        model.deleted_faces.add(0) 
        model.deleted_faces.add(3)

        triangle = [4, 1, 0]
        self.assertFalse(utils.face_already_exist(model, triangle))

    '''
    def test_shape_centroid_single_point(self):
        vertices_set = [np.array([3.0, -2.0, 5.5])]
        self.assertAlmostEqual(list(shape_centroid(vertices_set)), list(vertices_set[0]), 'Test function shape_centroid failed for single point.')
    
    def test_shape_centroid_midpoint(self):
        vertices_set = [np.array([0.0, 0.0, 0.0]), np.array([2.0, 4.0, 6.0])]
        middle = np.array([1.0, 2.0, 3.0])
        self.assertAlmostEqual(list(shape_centroid(vertices_set)), list(middle), 'Test function shape_centroid failed for midpoint.')
    '''

if __name__ == '__main__':
    unittest.main()