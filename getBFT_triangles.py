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
def getBFT(faces):

    dual_vertices = [i for i in range(len(faces))]
    dual_edges = getEdges(faces, dual_vertices)

    G = nx.Graph()
    G.add_nodes_from(dual_vertices)
    G.add_edges_from(dual_edges)
    G = G.to_undirected()

    if len(faces) == 0:
        return []

    if 0 not in G.nodes:
        return faces[:]   
    
    dict_successors = dict(nx.bfs_successors(G, source=0))
    keys = dict_successors.keys()

    order_triangle = []
    nexts = [0]
    visited = set()  

    while len(order_triangle) != len(faces):

        if len(nexts) == 0:
            for i in range(len(faces)):
                if i not in visited:
                    nexts.append(i)
                    break

        current = nexts[0]
        del nexts[0]

        if current < 0 or current >= len(faces):
            continue

        if current in visited:
            continue
        visited.add(current)

        order_triangle.append(faces[current])

        if current in keys:
            for ind in dict_successors[current]:
                if ind not in visited:
                    nexts.append(ind)

    return order_triangle

