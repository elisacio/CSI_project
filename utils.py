#!/usr/bin/env python

import obja
import numpy as np
import sys
import networkx as nx
import unittest

def flatten(xss):
    return [x for xs in xss for x in xs]

def shape_centroid(vertices_set):
    # Return Centroid of the 3D shape which is the mean of each value
    vert_coor = np.array([i for (_, i) in enumerate(vertices_set)])
    cent = np.sum(vert_coor, axis=0)
    cent = cent / len(vertices_set)
    return cent

def face_from_vertex(model, vertex_index) :
    liste_face = []
    for (face_index, face) in enumerate(model.faces) :
        if face_index not in model.deleted_faces:
            vertices = [face.a, face.b, face.c]
            if vertex_index in vertices :
                liste_face.append(face_index)
    return liste_face