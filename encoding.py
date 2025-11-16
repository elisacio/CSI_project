from huffman import huffman_encoder
from lz_encoding import encode

def encoding(w_n, coloration):
    """
    Encode the displacments' vector and the coloration vector.

    Args:
        w_n: list of displacements.
        coloration: vector containing the traingles' colors obtained thanks to a Breadth-First Search algorithm.

    Returns:
        w_n_encoded : a list containing the encoded version of W_n using Huffman.
        coloration_encoded :  a list containing the encoded version of coloration using the LZ encoder.
    """
    w_n_encoded = huffman_encoder(w_n)
    coloration_encoded = LZ_encoder(coloration)

    return w_n_encoded, coloration_encoded

def LZ_encoder(vect):
    """
    Encode a vector using LZ.

    Args:
        list(int): a list of integers.

    Returns:
        encoded_vect : a list containing the encoded values.
    """
    encoded_vect = encode(vect) # PAS FINI, il faut gérer les types d'entrée et de sortie
    return encoded_vect