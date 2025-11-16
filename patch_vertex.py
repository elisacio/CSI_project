#!/usr/bin/env python

import obja
import numpy as np
import sys
import networkx as nx
from check_rotation import check_rotation
import unittest
import utils

def couple_index_face(face, deleted_index):
    result = [face.a, face.b, face.c]
    result = [ind for ind in result if ind != deleted_index]
    return result

def ordonnement(faces, faces_voisines, deleted_index):
    # print(faces_voisines)
    couples = [couple_index_face(faces[face_ind], deleted_index) for face_ind in faces_voisines]
    # print(couples)
    # print(verifier_ferme(couples))
    if not verifier_ferme(couples) or len(couples) <= 2 or len(faces_voisines) <= 4 :
        return []
    start = couples[0][1]
    consecutive_list = couples[0]
    couples = couples[1:]
    while len(couples) > 1:
        couple = [i for i in couples if start in i][0]
        couples.remove(couple)
        start = couple[0] if couple[0] != start else couple[1]
        consecutive_list.append(start)
    return consecutive_list

def verifier_ferme(couples):
    couples_bis = set(utils.flatten(couples))
    return len(couples_bis) == len(couples)

def patch_vertex(model, indices_a_supprimer):
    """
    Prend en entrée les indices des vertex à supprimer, prend la liste des opérations de décimations
    Renvoie la liste des patchs ( la liste des indices dans l'ordre tel que la normale soit dans le bon sens )
    """
    patchs = set()
    operation = []
    centroid_shape = utils.shape_centroid(model.vertices)
    """
    for (vertex_index, vertex) in enumerate(model.vertices):
        if vertex_index in indices_a_supprimer :"""
    for vertex_index in indices_a_supprimer:
        faces_voisines = utils.face_from_vertex(model, vertex_index)
        consecutive_list = ordonnement(model.faces, faces_voisines, vertex_index)
        if len(consecutive_list) != 0:
            # print(consecutive_list)
            list_vertex_sorted = check_rotation(model.vertices, consecutive_list, centroid_shape)
            patchs.add(tuple(list_vertex_sorted))
            operation = operation + [('face', face_ind, model.faces[face_ind]) for face_ind in faces_voisines]
            model.deleted_faces.update({face_ind for face_ind in faces_voisines})
            # remove faces_voisines from faces !!!!! à mettre dans une variable
            operation.append(('vertex', vertex_index, model.vertices[vertex_index]))
            model.deleted_vertices.add(vertex_index)
            # remove vertex_index from vertices !!!!! à mettre dans une variable
    # remove les faces et vertex des set vertices and faces
    return patchs, operation#, deleted_faces, deleted_vertices