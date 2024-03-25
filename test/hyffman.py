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
            with open(file_path, 'r') as json_file:
                self.json = json.load(json_file)
            print(f"Загруженные коды Хаффмана из файла: {self.json}")
        else:
            self.file_path = file_path
            with open(file_path, 'r') as file:
                self.text = file.read()
            print(f"Загруженный файл: {self.text}")
    
    def bin_file_loader(self, file_path):
            with open(file_path, 'rb') as file:
                result_data_byte = file.read()
                self.bin = ''.join(['{:0>8}'.format(str(bin(item))[2:]) for item in result_data_byte])
                print(f"Закодированный двоичный код: {self.bin}")

    def encode(self):
        if self.text is None:
            print("Файл не загружен!")
            return

        letters = set(self.text)
        frequences = []
        for letter in letters:
            frequences.append((self.text.count(letter), letter))

        while len(frequences) > 1:  
            frequences = sorted(frequences, key=lambda x: x[0], reverse=True)
            first = frequences.pop()
            second = frequences.pop()
            freq = first[0] + second[0]
            frequences.append((freq, HuffmanCoder(first[1], second[1])))

        self.walk(frequences[0][1])
        print("Текст закодирован")

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

        current_code = ""
        for bit in self.bin:
            current_code += bit
            for char, code in self.json.items():
                if code == current_code:
                    self.decoded_text += char
                    current_code = ''
                    break
        print(self.decoded_text)   
                     
    def save_decodetxt(self):
        with open('decode_code.txt', 'w') as file:
            file.write(self.decoded_text)

    def save_bin_code(self):
        
        encoded_text = ''.join(self.code[char] for char in self.text)

        encoded_text = encoded_text + '0'*(8-(len(encoded_text)%8))
        source_data_byte = bytearray([int(encoded_text[i*8:i*8+8],2) for i in range(int(len(encoded_text)/8))])
        with open('result', 'wb') as file:
            file.write(source_data_byte)
            
    def save_json(self):
        with open(os.path.join('code.json'), 'w') as file:
            json.dump(self.code, file)
        print("Файл сохранён")

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
        encode_file_size = os.path.getsize("result")
        print(f"Размер закодированного файла: {encode_file_size} байт")

        entropy = self.shannon_entropy(self.text)
        print(f"Энтропия исходного текстового файла: {entropy}")

        avg_bits_per_symbol = encode_file_size * 8 / len(self.text)
        print(f"Среднее количество бит на символ в закодированном файле: {avg_bits_per_symbol}")

        compression_ratio = file_size / encode_file_size
        print(f"Степень сжатия: {compression_ratio}")