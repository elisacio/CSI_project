#!/usr/bin/env python
from collections import Counter
import obja
import numpy as np # type: ignore
import sys
import networkx as nx # type: ignore
from check_rotation import mean_normals, compare_norm, normal_triangle
import unittest
import utils
import zigzag_coloration


def couple_index_face(face, deleted_index):
    result = [face.a, face.b, face.c]
    result = [ind for ind in result if ind != deleted_index]
    return result

def verifier_ferme(couples):
    couples_bis = set(utils.flatten(couples))
    compteur = Counter(utils.flatten(couples))
    return (len(couples_bis) == len(couples)) and all(valeur == 2 for valeur in compteur.values())

def ordonnement(face_vertices, faces_voisines, deleted_index):
    #print(deleted_index)
    couples = [face_vert[1:] for face_vert in face_vertices]
    #print(couples)
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

def patch_vertex(model, indices_a_supprimer, operations, sens_counterclock):
    """
    Prend en entrée les indices des vertex à supprimer, prend la liste des opérations de décimations
    Renvoie la liste des patchs ( la liste des indices dans l'ordre tel que la normale soit dans le bon sens )
    """
    patchs = set()
    retriangulated_patches = []
    patches_colors = []
    index_face = len(model.faces)
    
    for vertex_index in indices_a_supprimer:

        faces_voisines = utils.face_from_vertex(model, vertex_index)
        face_vertices = [utils.rotate_until_first([model.faces[face_ind].a, model.faces[face_ind].b, model.faces[face_ind].c], vertex_index) for face_ind in faces_voisines]
        # face_vertices_set = set(face_vertices)
        consecutive_list = ordonnement(face_vertices, faces_voisines, vertex_index)
        # print(consecutive_list)

        if len(consecutive_list) != 0:
            
            list_vertex_sorted = consecutive_list if sens_counterclock else consecutive_list[::-1]
            
            new_triangles, colors = zigzag_coloration.draw_zigzag(tuple(list_vertex_sorted))

            normals = [normal_triangle(model.vertices, triang) for triang in new_triangles]
            has_zero_vector = any(all(x == 0 for x in n) for n in normals)
            # has_same_face = any(utils.face_already_exist(model, triangle) for triangle in new_triangles)
            while has_zero_vector: # or has_same_face:
                #print('has zero normal: ', has_zero_vector)
                # print('has same face: ', has_same_face)
                # print('old list vertex sorted: ', list_vertex_sorted)
                list_vertex_sorted.append(list_vertex_sorted.pop(0))
                # print('new list vertex sorted: ', list_vertex_sorted)
                new_triangles, colors = zigzag_coloration.draw_zigzag(tuple(list_vertex_sorted))
                
                normals = [normal_triangle(model.vertices, triang) for triang in new_triangles]
                # print('normals', normals)
                has_zero_vector = any(all(x == 0 for x in v) for v in normals)
                print('has zero normal: ', has_zero_vector)
                # has_same_face = any(utils.face_already_exist(model, triangle) for triangle in new_triangles)
                # print('has same face: ', has_same_face)

            patchs.add(tuple(list_vertex_sorted))
            retriangulated_patches.append(new_triangles)
            patches_colors.append(colors)
            last_index = len(model.faces)
            initial_normal = mean_normals(model.vertices, face_vertices)

            # build operations
            i = 0
            for triangle in new_triangles:
                if not utils.face_already_exist(model, triangle):
                    f_ind = compare_norm(model.vertices, initial_normal, triangle)
                    f = obja.Face(f_ind[0], f_ind[1], f_ind[2])
                    model.faces.append(f)
                    operations.append(('del', last_index+i, f))
                    i += 1
            
            operations.extend([('face', face_ind, model.faces[face_ind]) for face_ind in faces_voisines])
            model.deleted_faces.update({face_ind for face_ind in faces_voisines})
            
            operations.append(('vertex', vertex_index, model.vertices[vertex_index]))
            model.deleted_vertices.add(vertex_index)
    
    return patchs, patches_colors, model.faces[index_face:-1]