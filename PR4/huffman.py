# huffman.py

import os
import json
from datetime import datetime
from tree import *

class CodeGenerator:
    def __init__(self):
        self._codes = {}

    def _create_output_dir(self):
        now = datetime.now()
        folder_name = now.strftime("%Y-%m-%d-%H-%M-%S")
        os.makedirs(folder_name, exist_ok=True)
        return folder_name

    def gen_code(self, input_file):
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()

        tree = HuffmanTree(text)
        self._codes = tree.get_codes()

        output_dir = self._create_output_dir()
        output_file = os.path.join(output_dir, 'code.json')

        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(self._codes, file, ensure_ascii=False, indent=4)

        print(f"Huffman code generated and saved in {output_file}")
