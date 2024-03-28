import json
from hyffman_code import HuffmanCoder

def main():
    """
    Основная функция программы, управляющая взаимодействием с пользователем.
    """
    coder = HuffmanCoder()

    while True:
        print("\n1. Закодировать текст")
        print("2. Декодировать текст")
        print("3. Вывести данные о файле")
        print("4. Выйти")

        choice = input("Введите ваш выбор: ")
        if choice == '1':
            encode_text(coder)
        elif choice == '2':
            decode_text(coder)
        elif choice == '3':
            print_file_data(coder)
        elif choice == '4':
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
        print("Текст успешно закодирован")
        coder.save_bin_code()
        coder.save_json()
        print("Код Хаффмана успешно сохранен")
    except FileNotFoundError:
        print("Ошибка: Файл не найден. Проверьте путь к файлу")
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
    except FileNotFoundError:
        print("Ошибка: Файл не найден. Проверьте путь к файлу")
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

if __name__ == '__main__':
    main()
