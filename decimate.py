#!/usr/bin/env python

import obja
import os
import numpy as np # type: ignore
import sys
import networkx as nx # type: ignore
import check_rotation
import patch_vertex
import zigzag_coloration
import utils
from graphe import get_independent_set
from getBFT_triangles import getBFT
from encoding import encoding
from compute_wn import compute_wn
import time

def save_as_obj(path, model):
    dict_ecart = dict()
    ecart = 0
    with open(path, "w") as f:
        for (vertex_index, v) in enumerate(model.vertices):
            if vertex_index not in model.deleted_vertices:
                f.write(f"v {v[0]} {v[1]} {v[2]}\n")
                dict_ecart[vertex_index] = ecart
            else :
                ecart += 1
        for (face_index, face) in enumerate(model.faces):
            if face_index not in model.deleted_faces:
                f.write(f"f {face.a+1 - dict_ecart[face.a]} {face.b+1 - dict_ecart[face.b]} {face.c+1 - dict_ecart[face.c]}\n")

class OutputDel(obja.Output):
    def delete_face(self, index, face):
        print('df {}'.format(
            self.face_mapping[index] + 1
        ),
            file=self.output
        )

    def change_color(self, index, id_color) :
        color = "1.0 1.0 1.0" if id_color == 0 else "0.0 0.0 1.0"
        print("fc {} {}".format(self.face_mapping[index] + 1, color), file=self.output)

class Decimater(obja.Model):
    """
    A simple class that decimates a 3D model stupidly.
    """
    def __init__(self):
        super().__init__()
        self.deleted_faces = set()
        self.deleted_vertices = set()
        

    def contract(self, output, obj_name, iter_max):
        """
        Decimates the model stupidly, and write the resulting obja in output.
        """
        operations = []
        vecteurs_couleurs = []
        encoded_wns = []
        encoded_colorations = []

        print('Taille faces set initial: ', len(self.faces))


        for i in range(iter_max):
            #init dict_colors
            triangle_couleur = {}
            for ind in range(len(self.faces)):
                triangle_couleur[ind] = 0

            # Get indexes to remove 
            indexes_to_delete = get_independent_set(self) 
            # Remove faces and get patches
            patchs, patches_colors, formated_faces, triangle_couleur = patch_vertex.patch_vertex(self, indexes_to_delete, operations, triangle_couleur)
            print('taille set deleted_faces: ', len(self.deleted_faces))
            print('taille deleted_vertices: ', len(self.deleted_vertices))
            
            print('Taille faces ajoutées: ', len(formated_faces))
            print('Taille faces set after adding new ones: ', len(self.faces))
            print(f"Nombre d'opérations {i} :", len(operations))


            # Build the binary vector for the coloration encoding
            new_colors = utils.flatten(patches_colors)
            faces_etape_i = [self.faces[face_ind] for face_ind in range(len(self.faces)) if face_ind not in self.deleted_faces]
            
            index_faces_etape_i = [face_ind for face_ind in range(len(self.faces)) if face_ind not in self.deleted_faces]

            ordre_faces_etape_i = getBFT(faces_etape_i)
            vecteur = ""
            for face in ordre_faces_etape_i :
                if face in formated_faces :
                    index = formated_faces.index(face)
                    vecteur += str(new_colors[index])
                else :
                    vecteur += "0"
            vecteurs_couleurs.append(vecteur)

            # Add colors operations
            for ind in range(len(self.faces)) :
                if ind in index_faces_etape_i :
                    operations.append(('couleur', ind, triangle_couleur[ind]))


            
            # Encoding
            w_n = compute_wn(self, patchs, indexes_to_delete)
            w_n = [tuple(np.round(w * 1000).astype(int)) for w in w_n]
            w_n_encoded, coloration_encoded = encoding(w_n, vecteur)

            encoded_wns.append(w_n_encoded)
            encoded_colorations.append(coloration_encoded)
            

            #raise Exception('lol')


        # Save model with the lowest resolution
        save_as_obj(f'example/{obj_name}_low.obj', self)

        # Iterate through the vertex
        for (vertex_index, vertex) in enumerate(self.vertices):

            if vertex_index not in self.deleted_vertices:

                # Iterate through the faces
                for (face_index, face) in enumerate(self.faces):

                    # Delete any face related to this vertex
                    if face_index not in self.deleted_faces:
                        if vertex_index in [face.a,face.b,face.c]:
                            self.deleted_faces.add(face_index)
                            # Add the instruction to operations stack
                            if face_index in triangle_couleur.keys() :
                                operations.append(('couleur', face_index, triangle_couleur[face_index]))
                            else :
                                operations.append(('couleur', face_index, 0))
                            operations.append(('face', face_index, face))
                            

                # Delete the vertex
                operations.append(('vertex', vertex_index, vertex))

        # To rebuild the model, run operations in reverse order
        operations.reverse()

        # Write the result in output file
        output_model = OutputDel(output)

        for (ty, index, value) in operations:
            #print(ty, index, value)
            if ty == "vertex":
                output_model.add_vertex(index, value)
            elif ty == "face":
                output_model.add_face(index, value)
            elif ty == "couleur" :
                output_model.change_color(index, value) 
            else:
                output_model.delete_face(index, value)

        original_file = f'example/{obj_name}.obj'
        low_file = f'example/{obj_name}_low.obj'
        size_low = os.path.getsize(low_file)
        encoded_data_size = sum(len(e) for e in encoded_colorations) + sum(len(e) for e in encoded_wns) + size_low
        size_original = os.path.getsize(original_file)
        #print("size of encoded data : ", encoded_data_size)
        #print("size of original obj file : ", size_original)
        #print("size of low res model :", size_low)
        compression_ratio = 100 * (1 - (encoded_data_size / size_original))
        print(f"Taux de compression basé sur encodage : {compression_ratio:.2f} %")
            
        return encoded_colorations, encoded_wns, compression_ratio

def main():
    """
    Runs the program on the model given as parameter.
    """
    if len(sys.argv) == 3:
        obj_name = sys.argv[1]
        iter_max = int(sys.argv[2])
    elif len(sys.argv) == 2:
        obj_name = sys.argv[1]
        iter_max = 5
    else :
        obj_name = 'bunny'
        iter_max = 5

    np.seterr(invalid = 'raise')
    model = Decimater()
    model.parse_file(f'example/{obj_name}.obj')

    with open(f'example/progressive__{obj_name}.obja', 'w') as output:
        model.contract(output, obj_name, iter_max)


if __name__ == '__main__':
    main()
