import sys
from huffman_coding import HuffmanCoder
from haming_coder import HammingCoder, read_settings, setup_logger

def print_menu():
    print("Выберите действие:")
    print("1. Кодировать текст Хаффманом")
    print("2. Кодировать последовательность байт Хэммингом")
    print("3. Декодировать последовательность байт Хэмминга")
    print("4. Внести ошибки в последовательность байт Хэмминга")
    print("5. Выход")
    print("Спасибо за использование программы")

def huffman_encode():
    file_path = input("Введите путь к файлу для кодирования: ")
    huffman_coder = HuffmanCoder()
    huffman_coder.load_file(file_path)
    huffman_coder.encode()
    huffman_coder.save_bin_code()
    print("Текст успешно закодирован Хаффманом.")

def hamming_code():
    file_path = input("Введите путь к файлу для кодирования: ")
    hamming_coder = HammingCoder(read_settings(), setup_logger())
    with open(file_path, 'rb') as file:
        byte_sequence = bytearray(file.read())
    encoded_sequence = hamming_coder.code(byte_sequence)
    with open("encoded_hamming.txt", "wb") as encoded_file:
        encoded_file.write(encoded_sequence)
    print("Последовательность байт успешно закодирована Хэммингом и сохранена в файле encoded_hamming.txt.")


    file_path = input("Введите путь к файлу для кодирования: ")
    hamming_coder = HammingCoder(read_settings(), setup_logger())
    with open(file_path, 'rb') as file:
        byte_sequence = bytearray(file.read())
    encoded_sequence = hamming_coder.code(byte_sequence)
    with open("encoded_hamming.txt", "w") as encoded_file:
        encoded_file.write(encoded_sequence.decode())
    print("Последовательность байт успешно закодирована Хэммингом и сохранена в файле encoded_hamming.txt.")

def hamming_decode():
    file_path = input("Введите путь к файлу для декодирования: ")
    hamming_coder = HammingCoder(read_settings(), setup_logger())
    with open(file_path, 'rb') as file:
        byte_sequence = bytearray(file.read())
    decoded_sequence, status = hamming_coder.decode(byte_sequence)
    if status == "success":
        with open("decoded_hamming.txt", "w") as decoded_file:
            decoded_file.write(decoded_sequence.decode())
        print("Последовательность байт успешно декодирована Хэммингом и сохранена в файле decoded_hamming.txt.")
    elif status == "error":
        print("Произошла ошибка при декодировании. Пожалуйста, проверьте входные данные.")

def add_errors():
    file_path = input("Введите путь к файлу для добавления ошибок: ")
    num_errors = int(input("Введите количество ошибок для добавления: "))
    hamming_coder = HammingCoder(read_settings(), setup_logger())
    with open(file_path, 'rb') as file:
        byte_sequence = bytearray(file.read())
    corrupted_sequence = hamming_coder.noise(byte_sequence, num_errors)
    print(f"В последовательность байт успешно добавлено {num_errors} ошибок.")

def main():
    while True:
        print_menu()
        choice = input("Введите номер действия: ")
        if choice == '1':
            huffman_encode()
        elif choice == '2':
            hamming_code()
        elif choice == '3':
            hamming_decode()
        elif choice == '4':
            add_errors()
        elif choice == '5':
            print("Выход из программы.")
            sys.exit()
        else:
            print("Некорректный выбор. Попробуйте еще раз.")

if __name__ == "__main__":
    main()
