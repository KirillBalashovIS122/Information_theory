import configparser
import logging
import numpy as np
import random

class HammingCoder:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.word_size = int(config['Settings']['word_size'])

    def code(self, data):
        blocks = [data[i:i + self.word_size] for i in range(0, len(data), self.word_size)]
        encoded_data = bytearray()

        for block in blocks:
            # Дополняем блоки, которые короче word_size, нулями до нужной длины
            if len(block) < self.word_size:
                block += b'\x00' * (self.word_size - len(block))

            encoded_block = self._hamming_encode_block(block)
            encoded_data.extend(encoded_block)

        return encoded_data

    def decode(self, data):
        blocks = [data[i:i + self.word_size + self._calculate_parity_bits(self.word_size)] for i in range(0, len(data), self.word_size + self._calculate_parity_bits(self.word_size))]
        decoded_data = bytearray()

        for block in blocks:
            decoded_block = self._hamming_decode_block(block)
            decoded_data.extend(decoded_block)

        return decoded_data

    def noise(self, data, num_errors):
        # Вносит ошибки в последовательность байт
        for _ in range(num_errors):
            error_index = random.randint(0, len(data) - 1)
            data[error_index] = 1 - data[error_index]

    def _hamming_encode_block(self, block):
        n = len(block)
        r = self._calculate_parity_bits(n)

        hamming_matrix = np.zeros((r, n + r), dtype=int)

        for i in range(n):
            hamming_matrix[:, i + 1] = list(map(int, format(i + 1, f'0{r}b')))

        for i in range(r):
            indices = [2 ** i - 1] + [j for j in range(2 ** i, n + r + 1, 2 ** (i + 1))]
            hamming_matrix[i, 0] = sum([block[j - 1] for j in indices]) % 2

        encoded_block = bytearray()
        for i in range(n + r):
            encoded_bit = sum(hamming_matrix[:, i]) % 2
            encoded_block.append(encoded_bit)

        return encoded_block

    def _hamming_decode_block(self, block):
        n = len(block)
        r = self._calculate_parity_bits(n)

        hamming_matrix = np.zeros((r, n), dtype=int)

        for i in range(n):
            hamming_matrix[:, i] = list(map(int, format(i + 1, f'0{r}b')))

        syndrome = []
        for row in hamming_matrix:
            syndrome_bit = sum([block[i] * row[i] for i in range(n)]) % 2
            syndrome.append(syndrome_bit)

        error_position = sum([syndrome[i] * 2 ** i for i in range(len(syndrome))])

        if error_position != 0:
            block[error_position - 1] = 1 - block[error_position - 1]

        decoded_block = block[:n - r]

        return decoded_block

    def _calculate_parity_bits(self, n):
        r = 0
        while 2 ** r < n + r + 1:
            r += 1
        return r

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

    # Пример использования кодирования
    original_data = b'Hello, world!'
    encoded_data = coder.code(original_data)
    print("Encoded data:", encoded_data)

    # Пример использования декодирования
    decoded_data = coder.decode(encoded_data)
    print("Decoded data:", decoded_data)

    # Пример внесения ошибок
    noisy_data = bytearray(encoded_data)
    coder.noise(noisy_data, 2)
    print("Noisy data:", noisy_data)

    # Попытка декодирования зашумленных данных
    corrected_data = coder.decode(noisy_data)
    print("Corrected data:", corrected_data)

if __name__ == "__main__":
    main()
