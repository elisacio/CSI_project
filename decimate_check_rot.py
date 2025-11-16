#!/usr/bin/env python

import obja
import os
import numpy as np
import sys
import networkx as nx
import check_rotation
import patch_vertex
import zigzag_coloration
import utils
from graphe import get_independent_set
from getBFT_triangles import getBFT
from encoding import encoding, encode
from compute_wn import compute_wn

def save_as_obj(path, vertices, faces):
    with open(path, "w") as f:
        for v in vertices:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")
        for face in faces:
            f.write(f"f {face.a+1} {face.b+1} {face.c+1}\n")

class OutputDel(obja.Output):
    def delete_face(self, index, face):
        print('df {}'.format(
            self.face_mapping[index] + 1
        ),
            file=self.output
        )

class Decimater(obja.Model):
    """
    A simple class that decimates a 3D model stupidly.
    """
    def __init__(self):
        super().__init__()
        self.deleted_faces = set()
        self.deleted_vertices = set()
        

    def contract(self, output):
        """
        Decimates the model stupidly, and write the resulting obja in output.
        """
        operations = []
        vecteurs_couleurs = []
        encoded_wns = []
        encoded_colorations = []

        print('Taille faces set initial: ', len(self.faces))

        for i in range(5):
            # partie networkx de badr, on a les indices des sommets à supprimer
            indices_a_supprimer = get_independent_set(self) # resultat de badr
            # Enlever les faces et ressortir les patchs
            patchs, operation = patch_vertex.patch_vertex(self, indices_a_supprimer)
            print('taille set deleted_faces: ', len(self.deleted_faces))
            print('taille deleted_vertices: ', len(self.deleted_vertices))
            retriangulated_patches, patches_colors = zigzag_coloration.retriangulation(patchs)

            # add new faces (retriangulated_patches) to self.faces
            new_faces = utils.flatten(retriangulated_patches)
            last_index = len(self.faces)
            formated_faces = [obja.Face(f[0], f[1], f[2]) for f in new_faces]
            self.faces.extend(formated_faces)
            print('Taille faces set after adding new ones: ', len(self.faces))

            #construction du vecteur de 0 et de 1
            new_colors = utils.flatten(patches_colors)
            #faces_etape_i = list(set(self.faces) - self.deleted_faces)
            faces_etape_i = [self.faces[face_ind] for face_ind in range(len(self.faces)) if face_ind not in self.deleted_faces]
            print(f"Nombre de faces étape {i} :", len(faces_etape_i))
            ordre_faces_etape_i = getBFT(faces_etape_i)
            vecteur = ""
            for face in ordre_faces_etape_i :
                if face in formated_faces :
                    index = formated_faces.index(face)
                    vecteur += str(new_colors[index])
                else :
                    vecteur += "0"
            #print(vecteur)
            vecteurs_couleurs.append(vecteur)

            # Encodage 
            w_n = compute_wn(self, patchs, indices_a_supprimer)
            w_n = [tuple(np.round(w * 1000).astype(int)) for w in w_n]
            w_n_encoded, coloration_encoded = encoding(w_n, vecteur)

            encoded_wns.append(w_n_encoded)
            encoded_colorations.append(coloration_encoded)

            # add new faces to operations ('delete', face_index, face)
            for i in range(len(formated_faces)):
                operations.append(('del', last_index+i, formated_faces[i]))

            # ajout operation in operations
            operations = operations + operation

        # Enregistrement du modèle avec le plus bas niveau de détail
        save_as_obj("model_low.obj", self.vertices, self.faces)

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
                            operations.append(('face', face_index, face))

                # Delete the vertex
                operations.append(('vertex', vertex_index, vertex))

        # To rebuild the model, run operations in reverse order
        operations.reverse()

        # Write the result in output file
        output_model = OutputDel(output, random_color=True)

        for (ty, index, value) in operations:
            if ty == "vertex":
                output_model.add_vertex(index, value)
            elif ty == "face":
                output_model.add_face(index, value)   
            else:
                output_model.delete_face(index, value)

        original_file = "example/suzanne.obj"

        encoded_data_size = sum(len(e) for e in encoded_colorations) + sum(len(e) for e in encoded_wns)
        size_original = os.path.getsize(original_file)
        compression_ratio = 100 * (1 - encoded_data_size / size_original)
        print(f"Taux de compression basé sur encodage : {compression_ratio:.2f} %")
            
        return encoded_colorations, encoded_wns

def main():
    """
    Runs the program on the model given as parameter.
    """
    np.seterr(invalid = 'raise')
    model = Decimater()
    model.parse_file('example/suzanne.obj')

    with open('example/suzanne_prolonge.obja', 'w') as output:
        model.contract(output)


if __name__ == '__main__':
    main()
