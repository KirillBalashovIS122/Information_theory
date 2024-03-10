import json
import os
import heapq
from collections import Counter

class Node:
    """Class representing a node in the Huffman tree."""
    def __init__(self, symbol=None, frequency=0, left=None, right=None):
        """
        Initializes a Node object with the provided symbol, frequency, left and right child nodes.
        
        :param symbol: Symbol represented by the node.
        :param frequency: Frequency of the symbol.
        :param left: Left child node.
        :param right: Right child node.
        """
        self.symbol = symbol
        self.frequency = frequency
        self.left = left
        self.right = right

    def __lt__(self, other):
        """
        Compares the frequency of this node with another node.
        :param other: Another Node object to compare frequency with.
        :return: True if this node's frequency is less than the other node's frequency,
        :False otherwise.
        """
        return self.frequency < other.frequency

class CodeGenerator:
    """Class for generating Huffman codes."""
    def __init__(self):
        """Initializes a CodeGenerator object."""
        self._codes = {}

    def _build_huffman_tree(self, frequencies):
        """
        Builds a Huffman tree based on the symbol frequencies.
        
        :param frequencies: A dictionary containing symbol frequencies.
        :return: The root node of the Huffman tree.
        """
        heap = [Node(symbol, frequency) for symbol, frequency in frequencies.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            merged = Node(left=left, right=right, frequency=left.frequency + right.frequency)
            heapq.heappush(heap, merged)

        return heap[0]

    def _traverse_tree(self, node, code=''):
        """
        Traverses the Huffman tree to generate codes for symbols.
        
        :param node: Current node being traversed.
        :param code: The code generated so far for the path to this node.
        """
        if node.symbol is not None:
            self._codes[node.symbol] = code
            return
        self._traverse_tree(node.left, code + '0')
        self._traverse_tree(node.right, code + '1')

    def gen_code(self, file_path):
        """
        Generates Huffman codes for symbols in a file and saves them to a JSON file.
        
        :param file_path: Path to the input file.
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            frequencies = Counter(text)
            huffman_tree = self._build_huffman_tree(frequencies)
            self._traverse_tree(huffman_tree)

            folder_name = f'{file_path}-codes'
            os.makedirs(folder_name, exist_ok=True)
            output_path = os.path.join(folder_name, 'code.json')

            with open(output_path, 'w', encoding='utf-8') as json_file:
                json.dump(self._codes, json_file, ensure_ascii=False, indent=4)
