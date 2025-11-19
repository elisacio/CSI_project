#!/usr/bin/env python

import obja
import numpy as np # type: ignore
import sys
import networkx as nx # type: ignore
import unittest

def flatten(xss):
    return [x for xs in xss for x in xs]

def rotate_until_first(liste, target):
    try:
        i = liste.index(target)
    except ValueError:
        return liste

    return liste[i:] + liste[:i]

'''
def shape_centroid(vertices_set):
    # Return Centroid of the 3D shape which is the mean of each value
    vert_coor = np.array([i for (_, i) in enumerate(vertices_set)])
    cent = np.sum(vert_coor, axis=0)
    cent = cent / len(vertices_set)
    return cent'''

def face_from_vertex(model, vertex_index) :
    """
    Return the faces not deleted with vertex_index as a vertex of the face
    """
    liste_face = []
    for (face_index, face) in enumerate(model.faces) :
        if face_index not in model.deleted_faces:
            vertices = [face.a, face.b, face.c]
            if vertex_index in vertices :
                liste_face.append(face_index)
    return liste_face

def equal(face, triangle):
    """
    Return True if the indexes of the triangle are the same as the indexes of the vertices of the face
    """
    return face.a in triangle and face.b in triangle and face.c in triangle

def face_already_exist(model, triangle):
    return any(equal(f, triangle) for ind,f in enumerate(model.faces) if ind not in model.deleted_faces)