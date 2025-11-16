import unittest
from huffman import encode_vector, decode_vector, build_huffman_tree, generate_huffman_codes
from lz_encoding import encode, decode

class TestHuffmanEncoding(unittest.TestCase):
    def  test1(self):
        vect = [0.3, 1, 5, -4, 8, 36, -10, -0.6, 36, -10, -0.6, 10, -0.6, 0.3, 1, 5, -4, 8, 36, -10, 1, 1, 1]
        symbols = set(vect)
        freq = {x: vect.count(x) for x in symbols}  
        freq = freq.values()
        # Build the Huffman tree
        root = build_huffman_tree(symbols, freq)
        # Generate Huffman codes
        huffman_codes = generate_huffman_codes(root)
        encoded_vect = encode_vector(vect, huffman_codes)
        decoded_vect = decode_vector(encoded_vect, huffman_codes)
        print(f"Test Huffman: \nencoded_vect:{encoded_vect} \ndecoded_vect:{decoded_vect}")
        self.assertEqual(vect,decoded_vect," ")


class TestLZEncoding(unittest.TestCase):
    def  test1(self):
        vect = "0000000000001000011110000000"
        encoded_vect = encode(list(vect))
        decoded_vect = decode(list(encoded_vect))
        print(f"Test LZ: \nencoded_vect:{encoded_vect} \ndecoded_vect:{decoded_vect}")
        self.assertEqual(vect,decoded_vect," ")

if __name__ == '__main__':
    unittest.main()