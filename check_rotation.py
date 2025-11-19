import obja
import numpy as np # type: ignore
import sys
import networkx as nx # type: ignore

def normal_triangle(vertices, face_vert):
    """
    Compute the normal of a triangle based on the set of vertices and the index of the triangle.
    Return the normal.
    """
    coor = [vertices[i] for i in face_vert]
    N = np.cross(coor[1] - coor[0], coor[2] - coor[0])
    return N

def mean_normals(vertices, faces_vertices):
    """
    Compute the mean normal of a list of triangles.
    Return the mean normal.
    """
    normals = [normal_triangle(vertices, f_vert) for f_vert in faces_vertices]
    mean = np.mean(normals, axis=0)
    mean_norm = mean/np.linalg.norm(mean)
    return mean_norm

def compare_norm(vertices, initial_normal, face_vert):
    """
    Compare the normal of a triangle to the initial normal
    and change the order of the triangle if the normals are oriented the same way.
    Return the vertices of the triangle in order.
    """
    normal_face = normal_triangle(vertices, face_vert)
    normal_face_norm = normal_face/np.linalg.norm(normal_face)
    dot_prod = np.dot(normal_face_norm, initial_normal)
    return face_vert if dot_prod >=0 else face_vert[::-1]

def main():
    return 0


if __name__ == '__main__':
    main()