import numpy as np

def compute_wn(model, patchs, removed_vertices):
    """
    Compute displacement vectors w_n for each removed vertex of this iteration.
    
    Args:
        model: Decimater
        patchs: list of tuples/lists 
        removed_vertices: list of vertex indices removed 
        
    Returns:
        w_n: list of displacement vectors 
    """

    w_n = []

    for vertex_id, patch in zip(removed_vertices, patchs):

        patch_vertices = patch

        # Compute barycenter of each patch 
        coords = [model.vertices[i] for i in patch_vertices]
        vc = sum(coords) / len(coords)

        # Compute w : displacement vector
        v = model.vertices[vertex_id]
        w = v - vc

        w_n.append(w)

    return w_n
