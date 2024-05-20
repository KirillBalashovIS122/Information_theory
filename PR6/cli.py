import os
import logging
from huffman_pr6 import Huffman
from hamming_pr6 import Hamming


# Проверка наличия файла logfile.log и его создание, если не существует
if not os.path.exists("logfile.log"):
    with open("logfile.log", "w") as file:
        file.write("Log file created.\n")

# Настройка логгера
logging.basicConfig(filename='logfile.log', level=logging.INFO)

def menu():
    """Отображает главное меню и обрабатывает выбор пользователя."""
    while True:
        print("1. Кодировать")
        print("2. Декодировать")
        print("3. Выход")
        choice = input("Выберите операцию (1/2/3): ")
        huffman = Huffman()
        hamming = Hamming()
        if choice == '1':
            data = input("Введите данные для кодирования: ")
            encoded_huffman = huffman.encode(data)
            print("Закодированные данные Хаффмана:", encoded_huffman)
            encoded_hamming = hamming.encode(encoded_huffman)
            print("Закодированные данные Хэмминга:", encoded_hamming)
            # Логгирование
            logging.info("Huffman encoding: {}".format(encoded_huffman))
            logging.info("Hamming encoding: {}".format(encoded_hamming))
        elif choice == '2':
            encoded_data = input("Введите закодированные данные: ")
            decoded_hamming = hamming.decode(encoded_data)
            print("Декодированные данные Хэмминга:", decoded_hamming)
            decoded_huffman = huffman.decode(decoded_hamming)
            print("Декодированные данные Хаффмана:", decoded_huffman)
            # Логгирование
            logging.info("Hamming decoding: {}".format(decoded_hamming))
            logging.info("Huffman decoding: {}".format(decoded_huffman))
        elif choice == '3':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор операции.")

if __name__ == "__main__":
    menu()
