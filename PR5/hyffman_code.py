import os
import json
import math

class HuffmanCoder:
    """
    Класс для выполнения кодирования Хаффмана для текстовых файлов.

    Атрибуты:
        left (HuffmanCoder): Левый дочерний узел в дереве Хаффмана.
        right (HuffmanCoder): Правый дочерний узел в дереве Хаффмана.
        code (dict): Словарь для хранения кодов Хаффмана для символов.
        json (dict): Словарь для сериализации кодов Хаффмана.
        bin (str): Бинарное представление закодированного текста.
        text (str): Текст, загруженный из файла.
        decoded_text (str): Раскодированный текст.
        file_path (str): Путь к загруженному файлу.
    """

    def __init__(self, left=None, right=None):
        """
        Инициализирует объект HuffmanCoder с необязательными левым и правым дочерними узлами.

        Параметры:
            left (HuffmanCoder): Левый дочерний узел.
            right (HuffmanCoder): Правый дочерний узел.
        """
        self.left = left
        self.right = right
        self.code = {}
        self.json = {}
        self.bin = None
        self.text = None
        self.decoded_text = ""
        self.file_path = None

    def load_file(self, file_path):
        """
        Загружает файл по указанному пути.

        Аргументы:
            file_path (str): Путь к файлу.
        """
        if file_path.endswith('.json'):
            with open(file_path, 'r', encoding='utf-8') as file:
                self.text = file.read()
        else:
            self.file_path = file_path
            with open(file_path, 'r', encoding='utf-8') as file:
                self.text = file.read()

    def bin_file_loader(self, file_path):
        """
        Загружает бинарный файл и конвертирует его в строку битов.

        Аргументы:
            file_path (str): Путь к бинарному файлу.
        """
        with open(file_path, 'rb') as file:
            result_data_byte = file.read()
            self.bin = ''.join([f'{item:08b}' for item in result_data_byte])

    def encode(self):
        """
        Кодирует текст, используя алгоритм Хаффмана.
        """
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
        self.save_json()  # Сохраняем коды Хаффмана в формате JSON

    def walk(self, node, path=''):
        """
        Рекурсивно обходит дерево Хаффмана для генерации кодов.

        Аргументы:
            node (HuffmanCoder): Текущий узел.
            path (str): Путь к текущему узлу.
        """
        if isinstance(node, str):
            self.code[node] = path
            return
        self.walk(node.left, path + '0')
        self.walk(node.right, path + '1')

    def decode(self):
        """
        Декодирует бинарное представление текста.
        """
        if self.bin is None:
            print("Файл не загружен!")
            return

        # Загружаем коды Хаффмана из файла JSON
        with open(os.path.join(os.path.dirname(__file__), 'code.json'),
                  'r', encoding='utf-8') as file:
            self.json = json.load(file)

        current_code = ""
        for bit in self.bin:
            current_code += bit
            for char, code in self.json.items():
                if code == current_code:
                    self.decoded_text += char
                    current_code = ''  # Сбрасываем текущий код
                    break

        # Проверяем, были ли добавлены дополнительные нули в конец текста
        if current_code:
            # Если остались непрочитанные биты, добавляем недостающие символы, если это возможно
            for char, code in self.json.items():
                if code.startswith(current_code):
                    self.decoded_text += char
                    break

    def save_decodetxt(self):
        """
        Сохраняет раскодированный текст в файле 'decode_code.txt'.
        """
        with open(os.path.join(os.path.dirname(__file__),
                               'decode_code.txt'), 'w', encoding='utf-8') as file:
            file.write(self.decoded_text)

    def save_bin_code(self):
        """
        Сохраняет закодированный текст в двоичном формате в файле 'result'.
        """
        encoded_text = ''.join(self.code[char] for char in self.text)
        padding_length = 8 - (len(encoded_text) % 8)
        encoded_text += '0' * padding_length
        source_data_byte = bytes([int(encoded_text[i:i + 8], 2)
                                  for i in range(0, len(encoded_text), 8)])
        with open(os.path.join(os.path.dirname(__file__), 'result'), 'wb') as file:
            file.write(source_data_byte)


    def save_json(self):
        """
        Сохраняет коды Хаффмана в формате JSON в файле 'code.json'.
        """
        formatted_codes = {char: code for char, code in self.code.items()}
        with open(os.path.join(os.path.dirname(__file__),
        'code.json'), 'w', encoding='utf-8') as file:
            json.dump(formatted_codes, file, ensure_ascii=False, indent=4)

    def shannon_entropy(self, text):
        """
        Вычисляет энтропию Шеннона для текста.

        Аргументы:
            text (str): Текст для расчета энтропии.

        Возвращает:
            float: Значение энтропии.
        """
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
        """
        Выводит информацию о данных (исходном тексте, коде, энтропии и т. д.).
        """
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
        """
        Удаляет файлы, созданные во время работы программы.
        """
        files_to_delete = ['decode_code.txt', 'result', 'code.json']
        for file in files_to_delete:
            file_path = os.path.join(os.path.dirname(__file__), file)
            if os.path.exists(file_path):
                os.remove(file_path)
