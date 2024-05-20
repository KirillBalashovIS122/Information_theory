import json
from datetime import datetime
import os
import re
import shutil


class Node:
    """
    Класс представляет узел дерева Хаффмана.
    """
    def __init__(self, left, right):
        """
        Инициализирует новый экземпляр класса Node.

        Параметры:
        - left: Левый дочерний узел.
        - right: Правый дочерний узел.
        """
        self.left = left
        self.right = right

    @staticmethod
    def compress_data(text, huff_codes):
        """
        Сжимает данные, используя кодирование Хаффмана.

        Аргументы:
            text (str): Входной текст для сжатия.
            huff_codes (dict): Коды Хаффмана.

        Возвращает:
            str: Сжатые данные.
        """
        compressed_data = ""
        for char in text:
            compressed_data += huff_codes[char]
        return compressed_data

    @staticmethod
    def decompress_data(compressed_data, huff_codes):
        """
        Декодирует бинарные данные с использованием кодирования Хаффмана.

        Аргументы:
            compressed_data (str): Бинарные данные для декодирования.
            huff_codes (dict): Словарь, содержащий коды Хаффмана.

        Возвращает:
            str: Раскодированные данные.
        """
        decoded_data = ""
        current_code = ""

        for bit in compressed_data:
            current_code += str(bit)
            if current_code in huff_codes.values():
                decoded_data += next(symbol for symbol, code in huff_codes.items()
                                     if code == current_code)
                current_code = ""

        return decoded_data


class HuffmanTree:
    """
    Класс представляет дерево Хаффмана для кодирования текста.
    """
    def __init__(self, text):
        """
        Инициализирует новый экземпляр класса HuffmanTree.

        Параметры:
        - text: Входной текст для кодирования Хаффмана.
        """
        self.text = text
        self.letters = set(text)
        self.frequencies = [(text.count(letter), letter) for letter in self.letters]

    def build_tree(self):
        """
        Строит дерево Хаффмана.
        """
        while len(self.frequencies) > 1:
            self.frequencies = sorted(self.frequencies, key=lambda x: x[0], reverse=True)
            first = self.frequencies.pop()
            second = self.frequencies.pop()
            freq = first[0] + second[0]
            self.frequencies.append((freq, Node(first[1], second[1])))
        return self.frequencies[0][1]

    def generate_codes(self, node, path='', code=None):
        """
        Генерирует коды Хаффмана.

        Параметры:
        - node: Текущий узел дерева.
        - path: Текущий путь кода.
        - code: Словарь для хранения кодов.

        Возвращает:
            dict: Словарь с кодами Хаффмана.
        """
        if code is None:
            code = {}
        if isinstance(node, str):
            code[node] = path
            return code
        code = self.generate_codes(node.left, path + '0', code)
        code = self.generate_codes(node.right, path + '1', code)
        return code


def delete_folders_by_pattern(base_folder, pattern):
    """
    Удаляет папки, соответствующие заданному шаблону.

    Параметры:
    - base_folder: Базовая папка, в которой будет производиться удаление.
    - pattern: Регулярное выражение для сопоставления имен папок.
    """
    try:
        for folder_name in os.listdir(base_folder):
            folder_path = os.path.join(base_folder, folder_name)
            if os.path.isdir(folder_path) and re.match(pattern, folder_name):
                shutil.rmtree(folder_path)
    except OSError as e:
        print(f"Произошла ошибка при удалении папок: {e}")


def save_codes_to_json(data):
    """
    Сохраняет коды Хаффмана и сжатый текст в JSON-файл.

    Параметры:
    - data: Данные для сохранения, включая коды Хаффмана и сжатый текст.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    target_folder = "/home/admin/teorinfo2/teorinfo2/pr5"
    delete_folders_by_pattern(target_folder, r'\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}')
    folder_path = os.path.join(target_folder, timestamp)
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, "code.json")

    try:
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False)
    except OSError as e:
        print(f"Произошла ошибка при сохранении данных в JSON: {e}")


def create_text_file(decoded_data):
    """
    Создает текстовый файл с декодированными данными в указанной директории.

    Параметры:
    - decoded_data: Декодированные текстовые данные.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%М-%S")
    target_folder = "/home/admin/teorinfo2/teorinfo2/pr5"
    delete_folders_by_pattern(target_folder, r'\d{4}-\д{2}-\д{2}-\д{2}-\д{2}-\д{2}')
    folder_path = os.path.join(target_folder, timestamp)
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, "decode.txt")
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(decoded_data)
    except OSError as e:
        print(f"Произошла ошибка при сохранении декодированного текста в файл: {e}")


def save_binary_data(source_data, file_path):
    """
    Сохраняет бинарные данные в файл.

    Аргументы:
        source_data (str): Исходные данные для сохранения.
        file_path (str): Путь к файлу для сохранения данных.
    """
    source_data = source_data + '0' * (8 - (len(source_data) % 8))
    source_data_byte = bytearray([int(source_data[i * 8:i * 8 + 8], 2)
                                  for i in range(int(len(source_data) / 8))])
    with open(file_path, 'wb') as file:
        file.write(source_data_byte)


def load_binary_data(file_path):
    """
    Загружает бинарные данные из файла.

    Аргументы:
        file_path (str): Путь к файлу для загрузки данных.

    Возвращает:
        str: Загруженные бинарные данные.
    """
    with open(file_path, 'rb') as file:
        result_data_byte = file.read()
    result_data = ''.join(['{:08b}'.format(byte) for byte in result_data_byte])
    return result_data
