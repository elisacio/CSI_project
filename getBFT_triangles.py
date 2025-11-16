import networkx as nx

def getIdFace(faces, side, id_origin):
    """
    Take as input the faces, two id of vertex and the id of a face
    Return the face containing the same vertices except one
    """
    for i in range(len(faces)) :
        face = faces[i]
        sides = [(face.a, face.b), (face.b, face.a), (face.b, face.c), (face.c, face.b), (face.c, face.a),(face.a, face.c)]
        if side in sides and i != id_origin :
            return i

def getEdges(faces, dual_vertices):
    """
    Take as input the faces and vertices of a mesh
    Return the new edges of the dual graph
    """
    dual_edges = []
    for i in range(len(faces)) :
        face = faces[i]
        sides = [(face.a, face.b), (face.b, face.c), (face.c, face.a)]
        
        id_1 = getIdFace(faces, sides[0], i)
        id_2 = getIdFace(faces, sides[1], i)
        id_3 = getIdFace(faces, sides[2], i)
        if id_1 != None : 
            dual_edges.append((i,id_1))
        if id_2 != None : 
            dual_edges.append((i,id_2))
        if id_3 != None : 
            dual_edges.append((i,id_3))

    return dual_edges

def getBFT(faces):
    """
    Take as input the faces of a mesh
    Return the breadth first traversal of the triangles
    """
    dual_vertices = [i for i in range(len(faces))]
    dual_edges = getEdges(faces, dual_vertices)

    G = nx.Graph()
    G.add_nodes_from(dual_vertices)
    G.add_edges_from(dual_edges)
    G = G.to_undirected()

    dict_successors = dict(nx.bfs_successors(G, source=0))
    keys = dict_successors.keys()

    order_triangle = []
    nexts = [0]
    while len(order_triangle) != len(faces) :
        order_triangle.append(faces[nexts[0]])
        if nexts[0] in keys :
            for ind in dict_successors[nexts[0]] :
                nexts.append(ind)
        del nexts[0]

    return order_triangle
