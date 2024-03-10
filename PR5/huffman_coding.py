import heapq
import json
import math

class HuffmanNode:
    def __init__(self, char, frequency):
        self.char = char
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency

def build_huffman_tree(frequency_table):
    heap = [HuffmanNode(char, freq) for char, freq in frequency_table.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        left_child = heapq.heappop(heap)
        right_child = heapq.heappop(heap)
        merged_node = HuffmanNode(None, left_child.frequency + right_child.frequency)
        merged_node.left = left_child
        merged_node.right = right_child
        heapq.heappush(heap, merged_node)

    return heap[0]

def build_encoding_table(node, prefix="", encoding_table=None):
    if encoding_table is None:
        encoding_table = {}
        
    if node.char is not None:
        encoding_table[node.char] = prefix
    else:
        build_encoding_table(node.left, prefix + "0", encoding_table)
        build_encoding_table(node.right, prefix + "1", encoding_table)
    
    return encoding_table

def encode_text(text, encoding_table):
    encoded_text = ""
    for char in text:
        encoded_text += encoding_table[char]
    return encoded_text

def decode_text(encoded_text, root):
    decoded_text = ""
    current_node = root
    for bit in encoded_text:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.char is not None:
            decoded_text += current_node.char
            current_node = root

    return decoded_text

def calculate_entropy(frequency_table):
    total_chars = sum(frequency_table.values())
    entropy = 0.0
    for freq in frequency_table.values():
        probability = freq / total_chars
        entropy -= probability * math.log2(probability)
    return entropy

def calculate_compression_ratio(original_size, compressed_size):
    return original_size / compressed_size
