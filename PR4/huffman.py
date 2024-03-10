import heapq
from collections import Counter

class Node:
    """
    Представляет узел в дереве Хаффмана.

    Атрибуты:
        symbol (str): Символ, связанный с узлом.
        freq (int): Частота символа.
        left (Node): Левый дочерний узел.
        right (Node): Правый дочерний узел.
    """

    def __init__(self, symbol=None, freq=None):
        """
        Инициализирует объект Node с заданным символом и частотой.

        Args:
            symbol (str): Символ, связанный с узлом.
            freq (int): Частота символа.
        """
        self.symbol = symbol
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        """
        Сравнивает два объекта Node на основе их частот.

        Args:
            other (Node): Другой объект Node для сравнения.

        Returns:
            bool: True, если частота self меньше частоты other, иначе False.
        """
        return self.freq < other.freq

    def __eq__(self, other):
        """
        Проверяет, имеют ли два объекта Node одинаковую частоту.

        Args:
            other (Node): Другой объект Node для сравнения.

        Returns:
            bool: True, если частота self равна частоте other, иначе False.
        """
        return self.freq == other.freq

    def __ne__(self, other):
        """
        Проверяет, имеют ли два объекта Node разные частоты.

        Args:
            other (Node): Другой объект Node для сравнения.

        Returns:
            bool: True, если частота self не равна частоте other, иначе False.
        """
        return self.freq != other.freq


class CodeGenerator:
    """
    Генерирует коды Хаффмана для символов в заданном текстовом файле.
    """

    def __init__(self):
        """
        Инициализирует объект CodeGenerator.
        """

    def gen_code(self, file_path):
        """
        Генерирует коды Хаффмана для символов в заданном текстовом файле.

        Args:
            file_path (str): Путь к текстовому файлу.

        Returns:
            dict: Словарь, сопоставляющий символы их кодам Хаффмана.
        """
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
        """
        Создает словарь, сопоставляющий символы их кодам Хаффмана.

        Args:
            root (Node): Корневой узел дерева Хаффмана.
            current_code (str): Текущий генерируемый код Хаффмана.
            code_map (dict): Словарь для хранения сопоставления символов и их кодов Хаффмана.

        Returns:
            dict: Словарь, сопоставляющий символы их кодам Хаффмана.
        """
        if code_map is None:
            code_map = {}
        if root is None:
            return code_map
        if root.symbol is not None:
            code_map[root.symbol] = current_code
        code_map = self.build_code_map(root.left, current_code + '0', code_map)
        code_map = self.build_code_map(root.right, current_code + '1', code_map)
        return code_map
