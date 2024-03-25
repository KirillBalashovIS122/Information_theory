from hyffman import HuffmanCoder

def main():
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
            except Exception as e:
                print(f"Ошибка при загрузке файла или кодировании текста: {e}")
        elif choice == '2':
            file_path = input("Введите путь к зашифрованному тексту: ")
            Haf_key = input("Введите путь к коду Хаффмана: ")             
            try:
                coder.bin_file_loader(file_path)
                coder.load_file(Haf_key)               
                coder.decode()
                print("Текст успешно расшифрован")                         
                coder.save_decodetxt()
                print("Файл успешно сохранен")
            except FileNotFoundError:
                print("Ошибка: Файл не найден. Проверьте путь к файлу")
            except Exception as e:
                print(f"Ошибка при декодировании файла: {e}")
        elif choice == '3':
            try:
                coder.print_data()
            except Exception as e:
                print(f"Ошибка при выводе данных: {e}")
        elif choice == '4':
            print("Завершение работы программы")
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте еще раз")

if __name__ == '__main__':
    main()