"""
CLI 
"""
import os
import json
import shutil
from datetime import datetime
from huffman import CodeGenerator

class CLI:
    """
    Класс CLI предоставляет простой интерфейс командной строки для работы с кодами Хаффмана.

    Атрибуты:
        generator: Объект CodeGenerator для генерации кодов Хаффмана.
    """

    def __init__(self):
        """
        Инициализация объекта CLI.
        """
        self.generator = CodeGenerator()

    def show_menu(self):
        """
        Отображает меню действий на экране.
        """
        print("Выберите действие:")
        print("1. Сгенерировать код Хаффмана для текстового файла")
        print("2. Удалить всю историю создания кодов Хаффмана")
        print("3. Выйти")

    def run(self):
        """
        Запускает основной цикл работы программы.
        """
        while True:
            self.show_menu()
            choice = input("Ваш выбор: ")

            if choice == '1':
                file_path = input("Введите путь к текстовому файлу: ")
                self.generate_huffman_code(file_path)
            elif choice == '2':
                self.delete_history()
            elif choice == '3':
                print("Выход из программы.")
                break
            else:
                print("Некорректный ввод. Пожалуйста, выберите действие из списка.")

    def generate_huffman_code(self, file_path):
        """
        Генерирует код Хаффмана для указанного текстового файла.

        Args:
            file_path (str): Путь к текстовому файлу.

        Raises:
            ImportError: Если возникает ошибка при импорте.
        """
        try:
            if os.path.exists(file_path):
                code_folder_name = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                os.makedirs(code_folder_name)

                code_file_path = os.path.join(code_folder_name, "code.json")

                code_map = self.generator.gen_code(file_path)

                with open(code_file_path, 'w', encoding='utf-8') as outfile:
                    json.dump(code_map, outfile, ensure_ascii=False, indent=4)

                print(f"Код Хаффмана успешно сгенерирован и сохранён в {code_file_path}")
            else:
                print("Указанный файл не существует.")
        except OSError as e:
            print(f"Произошла ошибка: {str(e)}")

    def delete_history(self):
        """
        Удаляет всю историю создания кодов Хаффмана.

        Raises:
            ImportError: Если возникает ошибка при импорте.
        """
        try:
            history_folders = [f for f in os.listdir('.') if os.path.isdir(f) and len(f) == 19]
            for folder in history_folders:
                shutil.rmtree(folder)
            print("История создания кодов Хаффмана успешно удалена.")
        except OSError as e:
            print(f"Произошла ошибка при удалении истории: {str(e)}")

def main():
    """
    Точка входа в программу. Создает объект CLI и запускает его основной метод run().
    """
    cli = CLI()
    cli.run()

if __name__ == "__main__":
    main()
