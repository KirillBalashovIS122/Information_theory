import configparser
import logging
from hamming_coder_decoder import HammingCoder

def setup_logger():
    logger = logging.getLogger('hamming_logger')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('hamming.log')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

def main():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    logger = setup_logger()
    coder = HammingCoder(config, logger)

    print("Добро пожаловать в программу кодирования/декодирования по Хэммингу")

    while True:
        print("\nПожалуйста, выберите опцию:")
        print("1. Закодировать текст")
        print("2. Декодировать данные")
        print("3. Добавить ошибки в закодированные данные")
        print("4. Выйти из программы")

        choice = input("Введите ваш выбор: ")

        if choice == "1":
            text = input("Введите текст для кодирования: ")
            encoded_data = coder.code(text.encode('utf-8'))
            print("Закодированные данные:", encoded_data)

        elif choice == "2":
            encoded_data = input("Введите закодированные данные: ")
            decoded_data = coder.decode(bytearray.fromhex(encoded_data))
            print("Декодированные данные:", decoded_data.decode('utf-8'))

        elif choice == "3":
            encoded_data = input("Введите закодированные данные: ")
            num_errors = int(input("Введите количество ошибок для добавления: "))
            encoded_data_bytes = bytearray.fromhex(encoded_data)
            coder.noise(encoded_data_bytes, num_errors)
            print("Закодированные данные с ошибками:", encoded_data_bytes.hex())

        elif choice == "4":
            print("Завершение программы. До свидания!")
            break

        else:
            print("Неверный выбор. Пожалуйста, введите допустимую опцию.")

if __name__ == "__main__":
    main()
