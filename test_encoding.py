import unittest
from encoding import LZ_encoder, encoding
from huffman import encode_vector, decode_vector, build_huffman_tree, generate_huffman_codes
from lz_encoding import encode, decode

class TestHuffmanEncoding(unittest.TestCase):
    def  test(self):
        vect = [0.002, -0.5, 1.5, 2, -1, 0.04, 0.03, 2, -1, -1, 0.002, -0.5, 1.5, 2]
        symbols = set(vect)
        freq = {x: vect.count(x) for x in symbols}  
        freq = freq.values()
        # Build the Huffman tree
        root = build_huffman_tree(symbols, freq)
        # Generate Huffman codes
        huffman_codes = generate_huffman_codes(root)
        # Encode the vector
        encoded_vect = encode_vector(vect, huffman_codes)
        # Decode the encoded vect
        decoded_vect = decode_vector(encoded_vect, huffman_codes)
        print(f"Test Huffman: \nencoded_vect:{encoded_vect} \ndecoded_vect:{decoded_vect}")
        self.assertEqual(vect,decoded_vect)


class TestLZEncoding(unittest.TestCase):
    def  test(self):
        vect = "0000000000001000011110000000"
        encoded_vect = LZ_encoder(vect)
        decoded_vect = decode(list(encoded_vect))
        print(f"Test LZ: \nencoded_vect:{encoded_vect} \ndecoded_vect:{decoded_vect}")
        self.assertEqual(vect,decoded_vect)

class TestBothEncodings(unittest.TestCase):
    def test(self):
        w_n = [0.002, -0.5, 1.5, 2, -1, 0.04, 0.03, 2, -1, -1, -0.0007, -0.0007, -1, 0.04, 0.03, -1, 0.04, 0.03, 1.5, 2, -1]
        coloration = "0001111100000110000101110000001111"
        w_n_encoded, coloration_encoded = encoding(w_n, coloration)

        # Compute Huffman decoding
        # Get the frequency for each value
        symbols = set(w_n)
        freq = {x: w_n.count(x) for x in symbols}  
        freq = freq.values()
        # Build the Huffman tree
        root = build_huffman_tree(symbols, freq)
        # Generate Huffman codes
        huffman_codes = generate_huffman_codes(root)
        # Encode the vect with the generated huffman codes
        encoded_vect = encode_vector(w_n, huffman_codes)
        # Decode the encoded vect
        decoded_w_n = decode_vector(w_n_encoded, huffman_codes)

        # Compute LZ decoding
        decoded_coloration = decode(list(coloration_encoded))

        # Assertions
        self.assertEqual(w_n_encoded, encoded_vect)
        self.assertEqual(w_n, decoded_w_n)
        self.assertEqual(coloration, decoded_coloration)


if __name__ == '__main__':
    unittest.main()