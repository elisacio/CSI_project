import obja
import numpy as np
import sys
import networkx as nx
from utils import shape_centroid

def newell(vertices_set, vertices_index_sorted):
    normal = [0.0]*3
    edges = [[vertices_index_sorted[i], vertices_index_sorted[i+1]] if i < len(vertices_index_sorted)-1 else [vertices_index_sorted[i], vertices_index_sorted[0]]  for i in range(len(vertices_index_sorted))]
    for edge in edges:
        curr = vertices_set[edge[0]]
        next = vertices_set[edge[1]]
        normal[0] += (curr[1] - next[1]) * (curr[2] + next[2])
        normal[1] += (curr[2] - next[2]) * (curr[0] + next[0])
        normal[2] += (curr[0] - next[0]) * (curr[1] + next[1])
    norm = np.linalg.norm(np.array(normal))
    normal = normal/norm
    return normal

def check_rotation(vertices_set, vertices_index_sorted, centroid_shape):
    # print('order: ', vertices_index_sorted)
    # print('centroid shape: ', centroid_shape)
    # print('polygon: ', [vertices_set[ind] for ind in vertices_index_sorted])
    centroid_poly = shape_centroid([vertices_set[ind] for ind in vertices_index_sorted])
    centers_vector = centroid_poly - centroid_shape
    normal = newell(vertices_set, vertices_index_sorted)
    # print('normal: ', normal)
    dot_prod = np.dot(normal, centers_vector)
    # print('dot_product: ', dot_prod)
    return vertices_index_sorted if dot_prod < 0 else vertices_index_sorted[::-1]


def main():
    vertices_set = [np.array([0,0,0]), np.array([1,0,0]), np.array([1,0.707,0.707]), np.array([0,0.707,0.707])]
    vertices_order = [0, 1, 2, 3]
    order = check_rotation(vertices_set, vertices_order, np.array([0, 0, 0]))
    # print(order)


if __name__ == '__main__':
    main()