import json
import heapq
from collections import defaultdict
from configparser import ConfigParser

class Huffman:
    """Класс для работы с кодированием и декодированием данных методом Хаффмана."""

    def __init__(self):
        """Инициализация объекта класса."""
        self.huffman_codes = {}  # Словарь кодов Хаффмана

    def encode(self, data):
        """Кодирование данных методом Хаффмана.

        Args:
            data (str): Данные для кодирования.

        Returns:
            str: Закодированные данные.
        """
        frequency = defaultdict(int)
        for symbol in data:
            frequency[symbol] += 1

        priority_queue = [[weight, [symbol, ""]] for symbol, weight in frequency.items()]
        heapq.heapify(priority_queue)

        while len(priority_queue) > 1:
            lo = heapq.heappop(priority_queue)
            hi = heapq.heappop(priority_queue)
            for pair in lo[1:]:
                pair[1] = '0' + pair[1]
            for pair in hi[1:]:
                pair[1] = '1' + pair[1]
            heapq.heappush(priority_queue, [lo[0] + hi[0]] + lo[1:] + hi[1:])

        self.huffman_codes = dict(priority_queue[0][1:])
        huffman_encoded_data = ''.join(self.huffman_codes[symbol] for symbol in data)

        # Запись длины слова в settings.ini
        config = ConfigParser()
        config.read('settings.ini')
        if 'Huffman' not in config.sections():
            config.add_section('Huffman')
        config['Huffman']['Word_Length'] = str(len(data))
        with open('settings.ini', 'w') as configfile:
            config.write(configfile)

        # Сохранение словаря кодов в JSON файл
        with open("huffman_codes.json", "w") as file:
            json.dump(self.huffman_codes, file)

        return huffman_encoded_data

    def decode(self, encoded_data):
        """Декодирование данных методом Хаффмана.

        Args:
            encoded_data (str): Закодированные данные.

        Returns:
            str: Декодированные данные.
        """
        # Загрузка словаря кодов из JSON файла
        with open("huffman_codes.json", "r") as file:
            self.huffman_codes = json.load(file)

        # Чтение длины слова из settings.ini
        config = ConfigParser()
        config.read('settings.ini')
        word_length = int(config['Huffman']['Word_Length'])

        reverse_huffman_codes = {v: k for k, v in self.huffman_codes.items()}

        decoded_data = ""
        current_code = ""
        for bit in encoded_data:
            current_code += bit
            if current_code in reverse_huffman_codes:
                decoded_data += reverse_huffman_codes[current_code]
                current_code = ""

        return decoded_data[:word_length]  # Ограничение по длине слова
