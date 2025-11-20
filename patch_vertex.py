from collections import Counter
import obja
import numpy as np
import sys
import networkx as n 
from check_rotation import mean_normals, compare_norm, normal_triangle
import unittest
import utils
import zigzag_coloration

def verifier_ferme(couples):
    """
    Verify if list of couples is closed

    Args:
        couples: list of list of indexes (ex: [[1, 2], [2, 4]])
        
    Returns:
        True if the list is closed properly
    """
    couples_bis = set(utils.flatten(couples))
    compteur = Counter(utils.flatten(couples))
    return (len(couples_bis) == len(couples)) and all(valeur == 2 for valeur in compteur.values())

def ordonnement(face_vertices, faces_voisines):
    """
    Ordonate the vertices within a patch, according to conditions

    Args:
        face_vertices : list of list of indexes
        faces_voisines : list of faces
        
    Returns:
        consecutive_list : list of indexes
    """
    couples = [face_vert[1:] for face_vert in face_vertices]
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

def patch_vertex(model, indices_a_supprimer, operations, triangle_couleur):
    """
    Take as input the model, the list of vertices to remove, the list of operations and a dictionary of the colors of the triangle
    Return the set of the new patchs, the colors of these patchs, the formated faces and the completed dictionary

    Args:
        model : Decimater object
        indices_a_supprimer : list of index
        operations : list of operations
        triangle_couleur : dictionary between index of faces and a color (0 or 1)
        
    Returns:
        patchs : set of N-tuples
        patches_colors : list of list of colors (0 or 1)
        formated_faces : list of Faces
        triangle_couleur : dictionary between index of faces and a color (0 or 1) 
    """
    patchs = set()
    retriangulated_patches = []
    patches_colors = []
    index_face = len(model.faces)
    
    for vertex_index in indices_a_supprimer:

        faces_voisines = utils.face_from_vertex(model, vertex_index)
        face_vertices = [utils.rotate_until_first([model.faces[face_ind].a, model.faces[face_ind].b, model.faces[face_ind].c], vertex_index) for face_ind in faces_voisines]
        list_vertex_sorted = ordonnement(face_vertices, faces_voisines)

        if len(list_vertex_sorted) != 0:
            new_triangles, colors = zigzag_coloration.draw_zigzag(tuple(list_vertex_sorted))

            normals = [normal_triangle(model.vertices, triang) for triang in new_triangles]
            has_zero_vector = any(all(x == 0 for x in n) for n in normals)
            while has_zero_vector: # or has_same_face:
                list_vertex_sorted.append(list_vertex_sorted.pop(0))
                new_triangles, colors = zigzag_coloration.draw_zigzag(tuple(list_vertex_sorted))
                
                normals = [normal_triangle(model.vertices, triang) for triang in new_triangles]
                has_zero_vector = any(all(x == 0 for x in v) for v in normals)

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
                    triangle_couleur[last_index+i] = colors[i]
                    model.faces.append(f)
                    operations.append(('del', last_index+i, f))
                    i += 1
            
            for face_ind in faces_voisines :
                operations.append(('face', face_ind, model.faces[face_ind]))
                if model.faces[face_ind] in triangle_couleur.keys() :
                    operations.append(('couleur', face_ind, triangle_couleur[model.faces[face_ind]]))
            model.deleted_faces.update({face_ind for face_ind in faces_voisines})
            
            operations.append(('vertex', vertex_index, model.vertices[vertex_index]))
            model.deleted_vertices.add(vertex_index)
    
    return patchs, patches_colors, model.faces[index_face:-1], triangle_couleur