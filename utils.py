import obja
import numpy as np
import sys
import networkx as nx
import unittest

def flatten(liste):
    """
    Flatten a list of lists

    Args:
        liste: list of lists
        
    Returns:
        flattened liste
    
    """
    return [x for xs in liste for x in xs]

def rotate_until_first(liste, target):
    """
    Rotate the list until the target is the first element and keep the original order.
    
    Args:
        liste: list of integers
        target: integer to be put in first place
        
    Returns:
        list rotated with target as the first element
    
    """
    try:
        i = liste.index(target)
    except ValueError:
        return liste

    return liste[i:] + liste[:i]

def face_from_vertex(model, vertex_index) :
    """
    Return the faces not deleted with vertex_index as a vertex of the face

    Args:
        model: Decimate model
        vertex_index: index of the vertex to extract its faces
        
    Returns:
        liste_face: list of faces' indexes with vertex_index as a vertex
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
    
    Args:
        face: Face (obja)
        triangle: list of index of the triangle
        
    Returns:
        True if indexes of vertices in triangle are the same as in face
    """
    return face.a in triangle and face.b in triangle and face.c in triangle

def face_already_exist(model, triangle):
    """
    Return True if the triangle already exists in the model

    Args:
        model: Decimate model
        triangle: list of index of the triangle
        
    Returns:
        True if any non deleted face of the model have the same vertices as the triangle 
    """
    return any(equal(f, triangle) for ind,f in enumerate(model.faces) if ind not in model.deleted_faces)