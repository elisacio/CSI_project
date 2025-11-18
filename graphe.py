import networkx as nx
import unittest
import obja
import random


"""
This file contains the function calculating the maximum independent set of the formed graph
by the vertices of the 3D mesh and its unit tests.
"""

def get_independent_set(model):

    """
    Returns the model's maximal independent set of vertices. 
    INPUT : a Model object
    OUTPUT : a list of the graph's independent vertices
    """

    if len(model.vertices) == 0:
         print("The 3D model has no vertices ")
         return []

    G = nx.Graph()

    for (vertex_index, vertex) in enumerate(model.vertices):
        if vertex_index not in model.deleted_vertices:
            G.add_node(vertex_index)

    for (face_index, face) in enumerate(model.faces):
        if face_index not in model.deleted_faces:
            a = face.a
            b = face.b
            c = face.c
            G.add_edge(a, b)
            G.add_edge(b, c)
            G.add_edge(a, c)

    print('number of nodes: ', G.number_of_nodes())

    random.seed(2)

    stable = nx.maximal_independent_set(G)

    print('taille stable', len(stable))

    return stable

