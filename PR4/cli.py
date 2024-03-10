import os
import shutil
from datetime import datetime
from huffman import CodeGenerator

class CLI:
    def __init__(self):
        self.generator = CodeGenerator()

    def show_menu(self):
        print("Выберите действие:")
        print("1. Сгенерировать код Хаффмана для текстового файла")
        print("2. Удалить всю историю создания кодов Хаффмана")
        print("3. Выйти")

    def run(self):
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
        try:
            if os.path.exists(file_path):
                code_folder_name = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                os.makedirs(code_folder_name)

                code_file_path = os.path.join(code_folder_name, "code.json")

                self.generator.gen_code(file_path, code_file_path)

                print(f"Код Хаффмана успешно сгенерирован и сохранён в {code_file_path}")
            else:
                print("Указанный файл не существует.")
        except Exception as e:
            print(f"Произошла ошибка: {str(e)}")

    def delete_history(self):
        try:
            history_folders = [f for f in os.listdir('.') if os.path.isdir(f) and len(f) == 19]
            for folder in history_folders:
                shutil.rmtree(folder)
            print("История создания кодов Хаффмана успешно удалена.")
        except Exception as e:
            print(f"Произошла ошибка при удалении истории: {str(e)}")

def main():
    cli = CLI()
    cli.run()

if __name__ == "__main__":
    main()
