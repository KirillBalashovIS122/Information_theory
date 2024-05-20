import os
import logging
from huffman_pr6 import Huffman
from hamming_pr6 import Hamming

if not os.path.exists("logfile.log"):
    with open("logfile.log", "w", encoding='utf-8') as file:
        file.write("Log file created.\n")

logging.basicConfig(filename='logfile.log',
                    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def menu():
    """Отображает главное меню и обрабатывает выбор пользователя."""
    while True:
        print("1. Кодировать")
        print("2. Декодировать")
        print("3. Выход")
        choice = input("Выберите операцию: ")
        huffman = Huffman()
        hamming = Hamming()
        if choice == '1':
            data = input("Введите данные для кодирования: ")
            encoded_huffman = huffman.encode(data)
            print("Закодированные данные Хаффмана:", encoded_huffman)
            encoded_hamming = hamming.encode(encoded_huffman)
            print("Закодированные данные Хэмминга:", encoded_hamming)
            logging.info("Huffman encoding: %s", encoded_huffman)
            logging.info("Hamming encoding: %s", encoded_hamming)
        elif choice == '2':
            encoded_data = input("Введите закодированные данные: ")
            decoded_hamming = hamming.decode(encoded_data)
            print("Декодированные данные Хэмминга:", decoded_hamming)
            decoded_huffman = huffman.decode(decoded_hamming)
            print("Декодированные данные Хаффмана:", decoded_huffman)
            logging.info("Hamming decoding: %s", decoded_hamming)
            logging.info("Huffman decoding: %s", decoded_huffman)
        elif choice == '3':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор операции.")

if __name__ == "__main__":
    menu()
