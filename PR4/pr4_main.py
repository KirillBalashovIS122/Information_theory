import os
import json
from datetime import datetime

class Node:
    """Класс для представления узла в дереве Хаффмана."""
    def __init__(self, left, right):
        """
        Инициализация узла Хаффмана.

        :param left: Левый потомок узла.
        :param right: Правый потомок узла.
        """
        self.left = left
        self.right = right

class CodeGenerator:
    """Класс для генерации кода Хаффмана."""
    def __init__(self):
        """Инициализация генератора кода Хаффмана."""
        pass

    def generate_huffman_code(self, text):
        """
        Генерация кода Хаффмана для переданного текста.

        :param text: Текст для кодирования.
        :return: Словарь с кодами Хаффмана.
        """
        letters = set(text)
        frequences = [(text.count(letter), letter) for letter in letters]

        while len(frequences) > 1:
            frequences = sorted(frequences, key=lambda x: x[0], reverse=True)
            first = frequences.pop()
            second = frequences.pop()
            freq = first[0] + second[0]
            frequences.append((freq, Node(first[1], second[1])))

        code = {letter: '' for letter in letters}

        def walk(node, path=''):
            """Рекурсивная функция для обхода дерева и создания кодов."""
            if isinstance(node, str):
                code[node] = path
                return
            walk(node.left, path + '0')
            walk(node.right, path + '1')

        walk(frequences[0][1])
        return code

    def save_to_json(self, code, output_dir):
        """
        Сохранение кода Хаффмана в JSON файл.

        :param code: Сгенерированный код Хаффмана.
        :param output_dir: Папка для сохранения файла.
        """
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'code.json')
        
        with open(output_path, 'w', encoding='utf-8') as output_file:
            json.dump(code, output_file, ensure_ascii=False, indent=4)

        print(f"Код Хаффмана успешно сгенерирован и сохранен в {output_path}")

if __name__ == "__main__":
    cgen = CodeGenerator()
    
    while True:
        file_path = input('Введите путь к файлу с текстом для кодирования (или введите "exit" для завершения): ')
        if file_path.lower() == 'exit':
            break
        try:
            with open(file_path, 'r', encoding='UTF-8') as file:
                text_to_encode = file.read()
        except FileNotFoundError:
            print("Ошибка: Файл не найден.")
            continue
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            continue

        output_dir = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        huffman_code = cgen.generate_huffman_code(text_to_encode)
        cgen.save_to_json(huffman_code, output_dir)
