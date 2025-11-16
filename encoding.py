from huffman import huffman_encoder
from lz_encoding import encode

def encoding(w_n, coloration):
    """
    Encode the displacments' vector and the coloration vector.

    Args:
        w_n: list of displacements (a list of floats).
        coloration: vector containing the traingles' colors obtained thanks to a Breadth-First Search algorithm (a string containing 0s and 1s).

    Returns:
        w_n_encoded : a string containing the encoded version of W_n using Huffman.
        coloration_encoded :  a string containing the encoded version of coloration using the LZ encoder.
    """
    w_n_encoded = huffman_encoder(w_n)
    coloration_encoded = LZ_encoder(coloration)

    return w_n_encoded, coloration_encoded

def LZ_encoder(vect):
    """
    Encode a vector using LZ.

    Args:
        string: the list of bits.

    Returns:
        encoded_vect : a string of the encoded bits.
    """
    encoded_vect = encode(list(vect)) 
    return encoded_vect