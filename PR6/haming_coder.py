import configparser
import logging
import random

class HammingCoder:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def code(self, byte_sequence):
        """
        Кодирует последовательность байт кодом Хэмминга.

        Параметры:
            byte_sequence (bytearray): Последовательность байт для кодирования.

        Возвращает:
            bytearray: Закодированная последовательность байт.
        """
        # Реализация кодирования по Хэммингу
        encoded_sequence = bytearray()

        # Вычисляем количество проверочных бит
        word_size = self.config.getint('Settings', 'word_size')
        parity_bits = HammingCoder.calculate_parity_bits(word_size)

        # Создаем копию последовательности с добавлением мест для контрольных бит
        encoded_byte_sequence = bytearray(HammingCoder.insert_parity_bits
                                          (byte_sequence, parity_bits))

        # Вычисляем контрольные биты и вставляем их в последовательность
        for i in range(len(parity_bits)):
            # Вычисляем позицию контрольного бита
            position = 2 ** i - 1
            # Вычисляем значение контрольного бита
            encoded_byte_sequence[position] = HammingCoder.calculate_parity_bit(encoded_byte_sequence, position, parity_bits[i])

        return encoded_byte_sequence

    def decode(self, byte_sequence):
        """
        Декодирует последовательность байт методом Хэмминга.

        Аргументы:
            byte_sequence (bytearray): Последовательность байт для декодирования.

        Возвращает:
            tuple: Декодированная последовательность байт и статус выполнения операции.
        """
        if not byte_sequence:
            self.logger.error("Empty byte sequence provided for decoding.")
            return None, "error"

        # Расчет количества бит на проверку ошибок
        n = len(byte_sequence) * 8
        k = n.bit_length() - 1

        # Определение размера слова
        word_size = int(self.config['Hamming']['word_size'])

        # Разбиение последовательности байт на слова
        words = [byte_sequence[i:i + word_size] for i in range(0, len(byte_sequence), word_size)]

        decoded_sequence = bytearray()

        for word in words:
            # Проверка наличия ошибок и их коррекция, если это возможно
            corrected_word, error_detected = self.error_correction(word, k)
            if error_detected:
                self.logger.warning("Errors were detected and corrected in the Hamming code.")
            else:
                self.logger.info("No errors were detected in the Hamming code.")

            # Извлечение информационных битов из слова
            information_bits = self.extract_information_bits(corrected_word, k)

            # Преобразование информационных битов в байты и добавление их в раскодированную последовательность
            decoded_sequence.extend(information_bits)

        return decoded_sequence, "success"

    def noise(self, byte_sequence, num_errors):
        """
        Вносит ошибки в последовательность байт.

        Параметры:
            byte_sequence (bytearray): Последовательность байт.
            num_errors (int): Количество ошибок для внесения.

        Возвращает:
            bytearray: Последовательность байт с внесёнными ошибками.
        """
        # Вносим указанное количество ошибок случайным образом
        for _ in range(num_errors):
            position = random.randint(0, len(byte_sequence) - 1)
            byte_sequence[position] = random.randint(0, 255)
        return byte_sequence

    def error_correction(self, word, k):
        """
        Корректирует ошибки в слове методом Хэмминга.

        Аргументы:
            word (bytearray): Слово для коррекции.
            k (int): Количество бит на проверку ошибок.

        Возвращает:
            tuple: Слово после коррекции и флаг обнаружения ошибки.
        """
        # Инициализация переменных для хранения позиций ошибок и индекса бита для проверки
        error_positions = []
        parity_check_index = 1

        # Перебор битов слова, пропуская позиции проверки четности
        for i in range(1, len(word) + 1):
            # Если индекс бита равен степени двойки (позиция проверки четности), увеличиваем его
            if i == 2 ** parity_check_index:
                parity_check_index += 1
                continue

            # Вычисляем позицию бита в слове и позицию в массиве (нумерация с нуля)
            bit_position = i - 1

            # Выполняем проверку четности
            parity_sum = sum(word[j] for j in range(len(word)) if j & (bit_position + 1))
            if parity_sum % 2 != 0:
                error_positions.append(bit_position)

        # Если обнаружены ошибки, исправляем их
        if error_positions:
            self.logger.debug(f"Detected errors at positions: {error_positions}")

            # Исправляем биты с ошибками
            for position in error_positions:
                word[position] ^= 1

            self.logger.debug(f"Corrected word: {word}")
            return word, True
        else:
            return word, False

    def extract_information_bits(self, word, k):
        """
        Извлекает информационные биты из слова методом Хэмминга.

        Аргументы:
            word (bytearray): Слово для извлечения информации.
            k (int): Количество бит на проверку ошибок.

        Возвращает:
            bytearray: Информационные биты из слова.
        """
        # Формирование информационных битов, исключая биты проверки четности
        information_bits = bytearray()
        for i in range(1, len(word) + 1):
            if i not in (2 ** j for j in range(k)):
                information_bits.append(word[i - 1])

        return information_bits

    @staticmethod
    def calculate_parity_bits(word_size):
        """
        Вычисляет количество и позиции проверочных бит.

        Параметры:
            word_size (int): Размер слова.

        Возвращает:
            list: Список позиций проверочных бит.
        """
        parity_bits = []
        for i in range(word_size):
            if 2 ** i >= word_size + i + 1:
                break
            parity_bits.append(2 ** i)
        return parity_bits

    @staticmethod
    def insert_parity_bits(byte_sequence, parity_bits):
        """
        Вставляет места для проверочных бит в последовательность байт.

        Параметры:
            byte_sequence (bytearray): Последовательность байт.
            parity_bits (list): Список позиций проверочных бит.

        Возвращает:
            bytearray: Последовательность байт с местами для проверочных бит.
        """
        encoded_byte_sequence = bytearray()
        position = 0
        for i in range(len(byte_sequence) + len(parity_bits)):
            if i + 1 in parity_bits:
                encoded_byte_sequence.append(0)
            else:
                encoded_byte_sequence.append(byte_sequence[position])
                position += 1
        return encoded_byte_sequence

    @staticmethod
    def remove_parity_bits(byte_sequence, parity_bits):
        """
        Удаляет проверочные биты из последовательности байт.

        Параметры:
            byte_sequence (bytearray): Последовательность байт.
            parity_bits (list): Список позиций проверочных бит.

        Возвращает:
            bytearray: Последовательность байт без проверочных бит.
        """
        decoded_byte_sequence = bytearray()
        for i in range(len(byte_sequence)):
            if i + 1 not in parity_bits:
                decoded_byte_sequence.append(byte_sequence[i])
        return decoded_byte_sequence

    @staticmethod
    def calculate_parity_bit(byte_sequence, position, parity_bit):
        """
        Вычисляет значение проверочного бита.

        Параметры:
            byte_sequence (bytearray): Последовательность байт.
            position (int): Позиция проверочного бита.
            parity_bit (int): Номер проверочного бита.

        Возвращает:
            int: Значение проверочного бита.
        """
        # Вычисляем значение контрольного бита
        value = 0
        for i in range(len(byte_sequence)):
            if (i + 1) & position:
                value ^= byte_sequence[i]
        return value

    @staticmethod
    def correct_byte(byte_sequence, parity_bits):
        """
        Корректирует байт с помощью проверочных бит.

        Параметры:
            byte_sequence (bytearray): Последовательность байт.
            parity_bits (list): Список позиций проверочных бит.

        Возвращает:
            bytearray: Корректированный байт.
        """
        corrected_byte = bytearray()
        for i in range(len(byte_sequence)):
            if i + 1 not in parity_bits:
                corrected_byte.append(byte_sequence[i])
        return corrected_byte

def read_settings():
    """
    Читает настройки из файла конфигурации settings.ini.

    Возвращает:
        ConfigParser: Объект с настройками.
    """
    config = configparser.ConfigParser()
    config.read('settings.ini')
    return config

def setup_logger():
    """
    Настраивает логгирование.

    Возвращает:
        Logger: Объект для логгирования.
    """
    logger = logging.getLogger('HammingCoder')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

def main():
    # Читаем настройки из файла конфигурации
    config = read_settings()
    # Настраиваем логгирование
    logger = setup_logger()
    # Создаём объект кодировщика-декодировщика Хэмминга
    coder = HammingCoder(config, logger)

    # Здесь можно начать взаимодействие с пользователем, чтение входных данных и т. д.

if __name__ == "__main__":
    main()
