# pr1/huffman_tree.py

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

class HuffmanTree:
    def __init__(self, text):
        self.text = text
        self.freq_dict = self._build_freq_dict()
        self.root = self._build_tree()

    def _build_freq_dict(self):
        freq_dict = {}
        for char in self.text:
            if char in freq_dict:
                freq_dict[char] += 1
            else:
                freq_dict[char] = 1
        return freq_dict

    def _build_tree(self):
        nodes = [Node(char, freq) for char, freq in self.freq_dict.items()]

        while len(nodes) > 1:
            nodes = sorted(nodes, key=lambda x: x.freq)

            left = nodes.pop(0)
            right = nodes.pop(0)

            parent = Node(None, left.freq + right.freq)
            parent.left = left
            parent.right = right

            nodes.append(parent)

        return nodes[0]

    def _generate_codes_helper(self, node, current_code):
        if node.char:
            self.codes[node.char] = current_code
            return

        self._generate_codes_helper(node.left, current_code + '0')
        self._generate_codes_helper(node.right, current_code + '1')

    def get_codes(self):
        self.codes = {}
        self._generate_codes_helper(self.root, '')
        return self.codes
