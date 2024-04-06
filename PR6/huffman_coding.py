import os
import json
import math

class HuffmanCoder:
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right
        self.code = {}
        self.json = {}
        self.bin = None
        self.text = None
        self.decoded_text = ""
        self.file_path = None

    def load_file(self, file_path):
        if file_path.endswith('.json'):
            with open(file_path, 'r', encoding='utf-8') as file:
                self.text = file.read()
        else:
            self.file_path = file_path
            with open(file_path, 'r', encoding='utf-8') as file:
                self.text = file.read()

    def bin_file_loader(self, file_path):
        with open(file_path, 'rb') as file:
            result_data_byte = file.read()
            self.bin = ''.join([f'{item:08b}' for item in result_data_byte])

    def encode(self):
        if self.text is None:
            print("Файл не загружен!")
            return

        letters = set(self.text)
        frequencies = []
        for letter in letters:
            frequencies.append((self.text.count(letter), letter))

        while len(frequencies) > 1:
            frequencies = sorted(frequencies, key=lambda x: x[0], reverse=True)
            first = frequencies.pop()
            second = frequencies.pop()
            freq = first[0] + second[0]
            frequencies.append((freq, HuffmanCoder(first[1], second[1])))

        self.walk(frequencies[0][1])
        self.save_json()

    def walk(self, node, path=''):
        if isinstance(node, str):
            self.code[node] = path
            return
        self.walk(node.left, path + '0')
        self.walk(node.right, path + '1')

    def decode(self):
        if self.bin is None:
            print("Файл не загружен!")
            return

        with open(os.path.join(os.path.dirname(__file__), 'code.json'),
                  'r', encoding='utf-8') as file:
            self.json = json.load(file)

        current_code = ""
        for bit in self.bin:
            current_code += bit
            for char, code in self.json.items():
                if code == current_code:
                    self.decoded_text += char
                    current_code = ''
                    break

        if current_code:
            for char, code in self.json.items():
                if code.startswith(current_code):
                    self.decoded_text += char
                    break

    def save_decodetxt(self):
        with open(os.path.join(os.path.dirname(__file__),
                               'decode_code.txt'), 'w', encoding='utf-8') as file:
            file.write(self.decoded_text)

    def save_bin_code(self):
        """
        Сохраняет закодированный текст в двоичном формате в файле с расширением .bin.
        """
        encoded_text = ''.join(self.code[char] for char in self.text)
        padding_length = 8 - (len(encoded_text) % 8)
        encoded_text += '0' * padding_length
        source_data_byte = bytes([int(encoded_text[i:i + 8], 2)
                                for i in range(0, len(encoded_text), 8)])
        with open(os.path.join(os.path.dirname(__file__), 'result.bin'), 'wb') as file:
            file.write(source_data_byte)



    def save_json(self):
        formatted_codes = {char: code for char, code in self.code.items()}
        with open(os.path.join(os.path.dirname(__file__),
        'code.json'), 'w', encoding='utf-8') as file:
            json.dump(formatted_codes, file, ensure_ascii=False, indent=4)

    def shannon_entropy(self, text):
        frequency_dict = {}
        for char in text.lower():
            if char.isalpha():
                frequency_dict[char] = frequency_dict.get(char, 0) + 1

        shannon_ent = 0
        total_chars = sum(frequency_dict.values())
        for char, frequency in frequency_dict.items():
            probability = frequency / total_chars
            shannon_ent -= probability * math.log2(probability)

        return shannon_ent

    def print_data(self):
        if self.text is None:
            print("Файл не загружен!.")
            return
        print("Исходный текст:")
        print(self.text)
        file_size = os.path.getsize(self.file_path)
        print(f"Размер исходного файла: {file_size} байт")

        print("Закодированный текст:")
        print(self.bin)
        encode_file_size = os.path.getsize(os.path.join(os.path.dirname(__file__), 'result'))
        print(f"Размер закодированного файла: {encode_file_size} байт")

        entropy = self.shannon_entropy(self.text)
        print(f"Энтропия исходного текстового файла: {entropy}")

        avg_bits_per_symbol = encode_file_size * 8 / len(self.text)
        print(f"Среднее количество бит на символ в закодированном файле: {avg_bits_per_symbol}")

        compression_ratio = file_size / encode_file_size
        print(f"Степень сжатия: {compression_ratio}")

    def cleanup_files(self):
        files_to_delete = ['decode_code.txt', 'result', 'code.json']
        for file in files_to_delete:
            file_path = os.path.join(os.path.dirname(__file__), file)
            if os.path.exists(file_path):
                os.remove(file_path)
