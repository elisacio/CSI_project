# Python program for Huffman Coding
# inspired by https://www.geeksforgeeks.org/dsa/huffman-coding-in-python/
import heapq

class Node:
    def __init__(self, symbol=None, frequency=None):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency

def build_huffman_tree(symbols, freq):
    # Create a priority queue of nodes
    priority_queue = [Node(char, f) for char, f in zip(symbols, freq)]
    heapq.heapify(priority_queue)

    # Build the Huffman tree
    while len(priority_queue) > 1:
        left_child = heapq.heappop(priority_queue)
        right_child = heapq.heappop(priority_queue)
        merged_node = Node(frequency=left_child.frequency + right_child.frequency)
        merged_node.left = left_child
        merged_node.right = right_child
        heapq.heappush(priority_queue, merged_node)

    return priority_queue[0]

def generate_huffman_codes(node, code="", huffman_codes={}):
    if node is not None:
        if node.symbol is not None:
            huffman_codes[node.symbol] = code
        generate_huffman_codes(node.left, code + "0", huffman_codes)
        generate_huffman_codes(node.right, code + "1", huffman_codes)
    return huffman_codes

def encode_vector(vect, huffman_codes):
    encoded_vect = ""
    for symbol in vect:
        encoded_vect = encoded_vect + huffman_codes[symbol]
    return encoded_vect

def decode_vector(encoded_vect, huffman_codes):
    current_code = ''
    decoded_vect = []
    # Invert the codes dictionary to get the reverse mapping
    inv_huffman_codes = {v: k for k, v in huffman_codes.items()}
    for bit in encoded_vect:
        current_code += bit
        if current_code in inv_huffman_codes:
            decoded_vect.append(inv_huffman_codes[current_code])
            current_code = ''
    return decoded_vect

def huffman_encoder(vect):
    """
    Encode a vector using Huffman.

    Args:
        list(floats): a list of floats.

    Returns:
        encoded_vect : a string containing the encoded values.
    """
    # Get the frequency for each value
    symbols = set(vect)
    freq = {x: vect.count(x) for x in symbols}  
    freq = freq.values()
    # Build the Huffman tree
    root = build_huffman_tree(symbols, freq)
    # Generate Huffman codes
    huffman_codes = generate_huffman_codes(root)
    # Encode the vect with the generated huffman codes
    encoded_vect = encode_vector(vect, huffman_codes)
    return encoded_vect

def huffman_encoder_with_codes(vect):
    """
    Encode a vector using Huffman and returns the codes for the decoding.

    Args:
        list(floats): a list of floats.

    Returns:
        encoded_vect : a string containing the encoded values.
        huffman_codes : the codes for decoding
    """
    # Get the frequency for each value
    symbols = set(vect)
    freq = {x: vect.count(x) for x in symbols}  
    freq = freq.values()
    # Build the Huffman tree
    root = build_huffman_tree(symbols, freq)
    # Generate Huffman codes
    huffman_codes = generate_huffman_codes(root)
    # Encode the vect with the generated huffman codes
    encoded_vect = encode_vector(vect, huffman_codes)
    return encoded_vect, huffman_codes
