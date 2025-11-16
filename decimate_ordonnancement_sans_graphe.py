#!/usr/bin/env python

import obja
import numpy as np
import sys
import networkx as nx
import check_rotation
import patch_vertex
import utils
from graphe import get_independent_set


class Decimater(obja.Model):
    """
    A simple class that decimates a 3D model stupidly.
    """
    def __init__(self):
        super().__init__()
        self.deleted_faces = set()
        self.deleted_vertices = set()

    def patch_vertex(self, indices_a_supprimer, operations):
        patchs = set()
        for (vertex_index, vertex) in enumerate(self.vertices[:15]):
            if vertex_index in indices_a_supprimer:
                faces_voisines = utils.face_from_vertex(self.faces, vertex_index)
                list_vertex_sorted = patch_vertex.ordonnement(self.faces, faces_voisines, vertex_index)
                patchs.add(tuple(list_vertex_sorted))
                operations_to_add = [('face', face_ind, self.faces[face_ind]) for face_ind in faces_voisines]
                operations = operations + operations_to_add
                self.deleted_faces.add({(face_ind, self.faces[face_ind]) for face_ind in faces_voisines})
                operations.append(('vertex', vertex_index, self.vertices[vertex_index]))
                self.deleted_vertices.add((vertex_index, tuple(vertex)))
        return patchs, operations
        

    def contract(self, output):
        """
        Decimates the model stupidly, and write the resulting obja in output.
        """
        operations = []

        # Calculate the centroid of the shape (helps with the normal)
        centroid_shape = check_rotation.shape_centroid(self.vertices)
        print(self.vertices)
        
        # partie networkx de badr, on a les indices des sommets à supprimer
        indices_a_supprimer = get_independent_set(self) # resultat de badr

        # Enlever les faces et ressortir les patchs
        patchs, operations = self.patch_vertex(indices_a_supprimer, operations)

        for (vertex_index, vertex) in enumerate(self.vertices):
            operations.append(('ev', vertex_index, vertex + 0.25))

        # Iterate through the vertex
        for (vertex_index, vertex) in enumerate(self.vertices):

            # Iterate through the faces
            for (face_index, face) in enumerate(self.faces):

                # Delete any face related to this vertex
                if face_index not in self.deleted_faces:
                    if vertex_index in [face.a,face.b,face.c]:
                        self.deleted_faces.add(face_index)
                        # Add the instruction to operations stack
                        operations.append(('face', face_index, face))

            # Delete the vertex
            operations.append(('vertex', vertex_index, vertex))

        # To rebuild the model, run operations in reverse order
        operations.reverse()

        # Write the result in output file
        output_model = obja.Output(output, random_color=True)

        for (ty, index, value) in operations:
            if ty == "vertex":
                output_model.add_vertex(index, value)
            elif ty == "face":
                output_model.add_face(index, value)   
            else:
                output_model.edit_vertex(index, value)

def main():
    """
    Runs the program on the model given as parameter.
    """
    np.seterr(invalid = 'raise')
    model = Decimater()
    model.parse_file('example/bunny.obj')

    with open('example/bunny.obja', 'w') as output:
        model.contract(output)


if __name__ == '__main__':
    main()
