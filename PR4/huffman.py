import json
import heapq
from collections import Counter

class Node:
    def __init__(self, symbol=None, freq=None):
        self.symbol = symbol
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

    def __eq__(self, other):
        return self.freq == other.freq

    def __ne__(self, other):
        return self.freq != other.freq


class CodeGenerator:
    def __init__(self):
        pass

    def gen_code(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()

            frequencies = Counter(text)
            heap = [Node(symbol, freq) for symbol, freq in frequencies.items()]
            heapq.heapify(heap)

            while len(heap) > 1:
                left = heapq.heappop(heap)
                right = heapq.heappop(heap)
                merged = Node(freq=left.freq + right.freq)
                merged.left = left
                merged.right = right
                heapq.heappush(heap, merged)

            code_map = self.build_code_map(heap[0])

            return code_map
        except Exception as e:
            raise e

    def build_code_map(self, root, current_code='', code_map=None):
        if code_map is None:
            code_map = {}
        if root is None:
            return code_map
        if root.symbol is not None:
            code_map[root.symbol] = current_code
        code_map = self.build_code_map(root.left, current_code + '0', code_map)
        code_map = self.build_code_map(root.right, current_code + '1', code_map)
        return code_map
