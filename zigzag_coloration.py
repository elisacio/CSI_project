from math import floor

def draw_zigzag(patch):
    """
    Draw the zizag shape in a patch and color the new triangles.

    Args:
        patch (list(int)): list of vertices that form the patch.

    Returns:
        triangles_list: a list containing the lists of vertices that form the new triangles.
        color_list: the list of the colors of the new triangles.
    """
    incr = 1
    triangles_list = []
    colors_list = []
    # Boucle for sur le nombre de faces à créer
    for i in range(len(patch)-2) :
        # Coloration
        color = 1 # Each triangle is encoded with the '1' bit except two faces

        # First triangle (encoded with the '0' bit)
        if i == 0 :
            v1 = patch[0]
            v2 = patch[1]
            v3 = patch[2]
            color = 0

        # Last triangle
        elif i + 1 == len(patch)-2 :
            v1 = patch[len(patch)-1]
            v2 = patch[0]
            v3 = patch[2]

        # Triangles between triangle n° 1 and triangle n° nb_triangles/2
        elif i < floor((len(patch)-2)/2) :
            v1 = patch[i+1]
            v2 = patch[i+2]
            v3 = patch[len(patch)-i]

        # Triangle nb_triangles/2 (encoded with the '0' bit)
        elif i == floor((len(patch)-2)/2) :
            v1 = patch[i+1]
            v2 = patch[i+2]
            v3 = patch[i+3]
            color = 0

        # Triangles between triangle n° nb_triangles/2 and the last triangle
        else : 
            v1 = patch[i+2]
            v2 = patch[i+3]
            # If the number of vertices of the patch is even
            if len(patch) % 2 == 0 :
                v3 = patch[floor(len(patch)/2)-incr]
            # If the number of vertices of the patch is odd
            else :
                v3 = patch[floor(len(patch)/2)-incr+1]
            incr += 1

        # Creation of the new triangle
        new_triangle = [v1,v2,v3]
        triangles_list.append(new_triangle)
        colors_list.append(color)

    return triangles_list, colors_list

def retriangulation(patches) :
    """
    Retriangulate and apply the coloration in all the patches.

    Args:
        patches list((list(int))): list of patches.

    Returns:
        retriangulated_patches: a list containing the list of vertices that form the new triangles for each patch.
        patches_colors: the list of the triangles'colors of the patches.
    """
    retriangulated_patches = []
    patches_colors = []
    for patch in patches:
        new_triangles, colors = draw_zigzag(patch)
        retriangulated_patches.append(new_triangles)
        patches_colors.append(colors)
    return retriangulated_patches, patches_colors






