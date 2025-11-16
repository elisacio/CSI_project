#!/usr/bin/env python

import obja
import numpy as np
import sys
import networkx as nx
from check_rotation import check_rotation
import unittest
import utils
import zigzag_coloration

def couple_index_face(face, deleted_index):
    result = [face.a, face.b, face.c]
    result = [ind for ind in result if ind != deleted_index]
    return result

def ordonnement(faces, faces_voisines, deleted_index):
    couples = [couple_index_face(faces[face_ind], deleted_index) for face_ind in faces_voisines]
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

def patch_vertex(model, indices_a_supprimer, operations):
    """
    Prend en entrée les indices des vertex à supprimer, prend la liste des opérations de décimations
    Renvoie la liste des patchs ( la liste des indices dans l'ordre tel que la normale soit dans le bon sens )
    """
    patchs = set()
    retriangulated_patches = []
    patches_colors = []
    centroid_shape = utils.shape_centroid(model.vertices)
    index_face = len(model.faces)
    
    """
    for (vertex_index, vertex) in enumerate(model.vertices):
        if vertex_index in indices_a_supprimer :"""
    for vertex_index in indices_a_supprimer:

        faces_voisines = utils.face_from_vertex(model, vertex_index)
        consecutive_list = ordonnement(model.faces, faces_voisines, vertex_index)

        if len(consecutive_list) != 0:
            
            list_vertex_sorted = check_rotation(model.vertices, consecutive_list, centroid_shape)
            patchs.add(tuple(list_vertex_sorted))

            new_triangles, colors = zigzag_coloration.draw_zigzag(tuple(list_vertex_sorted))
            retriangulated_patches.append(new_triangles)
            patches_colors.append(colors)
            
            last_index = len(model.faces)
            formated_faces_patch = [obja.Face(f[0], f[1], f[2]) for f in new_triangles]
            model.faces.extend(formated_faces_patch)

            # build operations
            for i in range(len(formated_faces_patch)):
                operations.append(('del', last_index+i, formated_faces_patch[i]))
            
            operations.extend([('face', face_ind, model.faces[face_ind]) for face_ind in faces_voisines])
            model.deleted_faces.update({face_ind for face_ind in faces_voisines})
            
            operations.append(('vertex', vertex_index, model.vertices[vertex_index]))
            model.deleted_vertices.add(vertex_index)
    
    return patchs, patches_colors, model.faces[index_face:-1]