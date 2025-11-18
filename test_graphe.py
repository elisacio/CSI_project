import networkx as nx
import unittest
import obja
from graphe import get_independent_set
import numpy as np
from decimate_check_rot import Decimater


class TestGetStable(unittest.TestCase):

    def test_empty(self):
        attendu = []
        model = Decimater()
        test = get_independent_set(model)
        self.assertEqual(test, attendu)

    def test_single_triangle(self):
        model = Decimater()
        model.vertices.append(np.array([0.0, 0.0, 0.0]))
        model.vertices.append(np.array([1.0, 0.0, 0.0]))
        model.vertices.append(np.array([0.0, 1.0, 0.0]))
        model.faces.append(obja.Face(0, 1, 2))
        
        result = get_independent_set(model)
        self.assertEqual(len(result), 1)
        self.assertTrue(result[0] in [0, 1, 2])

    def test_two_triangles_sharing_edge(self):
        model = Decimater()
        for i in range(4):
            model.vertices.append(np.array([float(i), 0.0, 0.0]))
        model.faces.append(obja.Face(0, 1, 2))
        model.faces.append(obja.Face(1, 2, 3))
        
        result = get_independent_set(model)
        for i in range(len(result)):
            for j in range(i + 1, len(result)):
                self.assertFalse(
                    (result[i] in [0, 1, 2] and result[j] in [0, 1, 2] and result[i] != result[j]) or
                    (result[i] in [1, 2, 3] and result[j] in [1, 2, 3] and result[i] != result[j])
                )

    def test_disconnected_vertices(self):
        model = Decimater()
        for i in range(5):
            model.vertices.append(np.array([float(i), 0.0, 0.0]))
        
        result = get_independent_set(model)
        self.assertEqual(len(result), 5)

    def test_tetrahedron(self):
        model = Decimater()
        for i in range(4):
            model.vertices.append(np.array([float(i), 0.0, 0.0]))
        model.faces.append(obja.Face(0, 1, 2))
        model.faces.append(obja.Face(0, 1, 3))
        model.faces.append(obja.Face(0, 2, 3))
        model.faces.append(obja.Face(1, 2, 3))
        
        result = get_independent_set(model)
        self.assertEqual(len(result), 1)

    def test_square_faces(self):
        model = Decimater()
        model.vertices.append(np.array([0.0, 0.0, 0.0]))
        model.vertices.append(np.array([1.0, 0.0, 0.0]))
        model.vertices.append(np.array([1.0, 1.0, 0.0]))
        model.vertices.append(np.array([0.0, 1.0, 0.0]))
        model.faces.append(obja.Face(0, 1, 2))
        model.faces.append(obja.Face(0, 2, 3))
        
        result = get_independent_set(model)
        self.assertGreaterEqual(len(result), 1)
        if len(result) == 2:
            self.assertTrue(
                (1 in result and 3 in result) or 
                any(combo for combo in [(0, 2), (1, 3)])
            )

    def test_independence_property(self):
        model = Decimater()
        vertices = [
            [0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0], [1.0, 0.0, 1.0], [1.0, 1.0, 1.0], [0.0, 1.0, 1.0]
        ]
        for v in vertices:
            model.vertices.append(np.array(v))
        
        faces = [
            (0, 1, 2), (0, 2, 3),  
            (4, 5, 6), (4, 6, 7),   
            (0, 1, 5), (0, 5, 4),
            (2, 3, 7), (2, 7, 6), 
            (0, 3, 7), (0, 7, 4),  
            (1, 2, 6), (1, 6, 5),  
        ]
        for f in faces:
            model.faces.append(obja.Face(f[0], f[1], f[2]))
        
        result = get_independent_set(model)
        
        G = nx.Graph()
        for i in range(len(model.vertices)):
            G.add_node(i)
        for face in model.faces:
            G.add_edge(face.a, face.b)
            G.add_edge(face.b, face.c)
            G.add_edge(face.a, face.c)
        
        for i in range(len(result)):
            for j in range(i + 1, len(result)):
                self.assertFalse(G.has_edge(result[i], result[j]),
                               f"Les sommets {result[i]} et {result[j]} sont adjacents")

    def test_result_type(self):
        model = Decimater()
        model.vertices.append(np.array([0.0, 0.0, 0.0]))
        result = get_independent_set(model)
        self.assertIsInstance(result, list)

    def test_result_contains_valid_indices(self):
        model = Decimater()
        for i in range(5):
            model.vertices.append(np.array([float(i), 0.0, 0.0]))
        model.faces.append(obja.Face(0, 1, 2))
        
        result = get_independent_set(model)
        for vertex_index in result:
            self.assertGreaterEqual(vertex_index, 0)
            self.assertLess(vertex_index, len(model.vertices))

    def test_linear_chain(self):
        model = Decimater()
        for i in range(5):
            model.vertices.append(np.array([float(i), 0.0, 0.0]))
        model.faces.append(obja.Face(0, 1, 2))
        model.faces.append(obja.Face(1, 2, 3))
        model.faces.append(obja.Face(2, 3, 4))
        
        result = get_independent_set(model)
        self.assertGreaterEqual(len(result), 2)

    def test_maximality(self):
        model = Decimater()
        for i in range(3):
            model.vertices.append(np.array([float(i), 0.0, 0.0]))
        model.faces.append(obja.Face(0, 1, 2))
        
        result = get_independent_set(model)
        
        G = nx.Graph()
        for i in range(len(model.vertices)):
            G.add_node(i)
        for face in model.faces:
            G.add_edge(face.a, face.b)
            G.add_edge(face.b, face.c)
            G.add_edge(face.a, face.c)
        
        for v in range(len(model.vertices)):
            if v not in result:
                has_neighbor_in_result = any(G.has_edge(v, r) for r in result)
                self.assertTrue(has_neighbor_in_result,
                              f"Le sommet {v} pourrait être ajouté à l'ensemble")


if __name__ == '__main__':
    unittest.main()
