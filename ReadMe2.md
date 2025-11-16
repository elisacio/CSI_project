## Code advancement

### File decimate_ordonnancement.py (Badr, Damien, Helia)

### File check_rotation.py (Helia)
- Code for checking if the patch is in the right order (normal is inward)
- Principal function is check_rotation.
- args: full set of vertices, list of indexes of patch vertices in order (one next to the other), centroïd of the 3D object
- returns: list of patch vertices in the correct order.

### File zigzag_coloration.py (Elisa)
- Code for drawing the zigzag shape and for coloring triangles within a patch
- args : list(int) the list of vertices of the patch
- returns : the list of the new triangles and the list of the colors that encode the new triangles
- Tested with unit tests in file test_zigzag_coloration.py

### File encoding.py (Elisa)
- Code for encoding the displacements and the mesh's coloration
- args: w_n the list of the displacements and coloration the list of the triangles colors
- returns: the encoded vectors

### Files huffman.py and lz_encoder.py (Elisa)
- Code for encoding with huffman and lz_encoder

### File test_encoding.py (Elisa)
- Code for testing the huffman and LZ encoders

## File patch_vertex.py (Damien)
- Code for determining which patches need to be created and theirs associated operations ( delete a face, delete a vertex ) 
- args : list(int) list of the vertices to delete, list(operations) list of all the operations, list(3d points) list of all vertices, list(Face) list of all faces
- returns : the list of the new patches and the updated list of operations
- Tested with unit tests in file test_patch_vertex.py

## Login credentials
- username : group3
- pwd : toto
