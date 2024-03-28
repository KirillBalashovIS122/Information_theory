import json
from hyffman_code import HuffmanCoder

def main():
    """
    Основная функция программы, позволяющая пользователю работать с.
    """
    coder = HuffmanCoder()

    while True:
        print ("\nДобро пожаловать!")
        print("1. Закодировать текст")
        print("2. Декодировать текст")
        print("3. Вывести данные о файле")
        print("4. Удалить все созданные файлы")
        print("5. Выйти")

        choice = input("Введите ваш выбор: ")
        if choice == '1':
            encode_text(coder)
        elif choice == '2':
            decode_text(coder)
        elif choice == '3':
            print_file_data(coder)
        elif choice == '4':
            cleanup_files(coder)
        elif choice == '5':
            print("Завершение работы программы")
            break
        else:
            print("Ошибка: Неверный выбор. Пожалуйста, выберите еще раз")

def encode_text(coder):
    """
    Кодирует текст, используя код Хаффмана.
    
    Параметры:
    coder (HuffmanCoder): Экземпляр класса HuffmanCoder для работы с кодированием.
    """
    file_path = input("Введите путь к текстовому файлу: ")
    try:
        coder.load_file(file_path)
        coder.encode()
        coder.save_bin_code()
        coder.save_json()
        print("Код Хаффмана успешно сохранен")
    except json.JSONDecodeError:
        print("Ошибка: Неверный формат JSON файла с кодом Хаффмана")

def decode_text(coder):
    """
    Декодирует текст, используя код Хаффмана.
    
    Параметры:
    coder (HuffmanCoder): Экземпляр класса HuffmanCoder для работы с декодированием.
    """
    file_path = input("Введите путь к зашифрованному тексту: ")
    haf_key = input("Введите путь к коду Хаффмана: ")
    try:
        coder.bin_file_loader(file_path)
        coder.load_file(haf_key)
        coder.decode()
        print("Текст успешно расшифрован")
        coder.save_decodetxt()
        print("Файл успешно сохранен")
    except json.JSONDecodeError:
        print("Ошибка: Неверный формат JSON файла с кодом Хаффмана")

def print_file_data(coder):
    """
    Выводит данные о файле.

    Параметры:
    coder (HuffmanCoder): Экземпляр класса HuffmanCoder для работы с данными файла.
    """
    if coder.text is None:
        print("Ошибка: Не загружен текстовый файл")
    else:
        try:
            coder.print_data()
        except ImportError as e:
            print(f"Ошибка при выводе данных: {e}")

def cleanup_files(coder):
    """
    Удаляет все созданные файлы во время работы программы.

    Параметры:
    coder (HuffmanCoder): Экземпляр класса HuffmanCoder для работы с файлами.
    """
    coder.cleanup_files()
    print("Все созданные файлы удалены.")

if __name__ == '__main__':
    main()
