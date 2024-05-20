import json
import heapq
from collections import defaultdict
from configparser import ConfigParser, NoSectionError, NoOptionError

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
        try:
            config.read('settings.ini', encoding='utf-8')
            if 'Huffman' not in config.sections():
                config.add_section('Huffman')
            config['Huffman']['Word_Length'] = str(len(data))
            with open('settings.ini', 'w', encoding='utf-8') as configfile:
                config.write(configfile)
        except (OSError, IOError) as e:
            print(f"Ошибка при работе с файлом settings.ini: {e}")

        # Сохранение словаря кодов в JSON файл
        try:
            with open("huffman_codes.json", "w", encoding='utf-8') as file:
                json.dump(self.huffman_codes, file)
        except (OSError, IOError) as e:
            print(f"Ошибка при сохранении словаря кодов в JSON файл: {e}")

        return huffman_encoded_data

    def decode(self, encoded_data):
        """Декодирование данных методом Хаффмана.

        Args:
            encoded_data (str): Закодированные данные.

        Returns:
            str: Декодированные данные.
        """
        # Загрузка словаря кодов из JSON файла
        try:
            with open("huffman_codes.json", "r", encoding='utf-8') as file:
                self.huffman_codes = json.load(file)
        except (OSError, IOError, json.JSONDecodeError) as e:
            print(f"Ошибка при загрузке словаря кодов из JSON файла: {e}")
            return ""

        # Чтение длины слова из settings.ini
        config = ConfigParser()
        try:
            config.read('settings.ini', encoding='utf-8')
            word_length = int(config['Huffman']['Word_Length'])
        except (OSError, IOError, NoSectionError, NoOptionError, ValueError) as e:
            print(f"Ошибка при чтении длины слова из settings.ini: {e}")
            return ""

        reverse_huffman_codes = {v: k for k, v in self.huffman_codes.items()}

        decoded_data = ""
        current_code = ""
        for bit in encoded_data:
            current_code += bit
            if current_code in reverse_huffman_codes:
                decoded_data += reverse_huffman_codes[current_code]
                current_code = ""

        return decoded_data[:word_length]  # Ограничение по длине слова
