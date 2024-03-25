from hyffman import HuffmanCoder

def main():
    """
    Главная функция программы.

    Выводит меню выбора операций с текстом

    В зависимости от выбора пользователя выполняет соответствующую операцию.

    """
    coder = HuffmanCoder()

    while True:
        print("\n1. Закодировать текст")
        print("2. Декодировать текст")
        print("3. Вывести данные о файле")
        print("4. Выйти")

        choice = input("Введите ваш выбор: ")
        if choice == '1':
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
            except IOError as e:
                print(f"Ошибка при загрузке файла или кодировании текста: {e}")
        elif choice == '2':
            file_path = input("Введите путь к зашифрованному тексту: ")
            huffman_key_path = input("Введите путь к коду Хаффмана: ")
            try:
                coder.bin_file_loader(file_path)
                coder.load_file(huffman_key_path)
                coder.decode()
                print("Текст успешно расшифрован")
                coder.save_decodetxt()
                print("Файл успешно сохранен")
            except FileNotFoundError:
                print("Ошибка: Файл не найден. Проверьте путь к файлу")
            except IOError as e:
                print(f"Ошибка при декодировании файла: {e}")
        elif choice == '3':
            try:
                coder.print_data()
            except FileNotFoundError:
                print("Ошибка: Файл не найден. Проверьте путь к файлу")
        elif choice == '4':
            print("Завершение работы программы")
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте еще раз")

if __name__ == '__main__':
    main()
