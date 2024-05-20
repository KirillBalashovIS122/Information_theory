class Hamming:
    """Класс для кодирования и декодирования данных методом Хэмминга."""

    def encode(self, data):
        """Кодирует данные методом Хэмминга.

        Добавляет контрольные биты к входным данным для обеспечения возможности
        обнаружения и исправления одиночных ошибок.

        Args:
            data (str): Входные данные для кодирования, представленные в виде строки из битов.

        Returns:
            str: Закодированные данные, содержащие исходные и контрольные биты.
        """
        data = list(data)
        m = len(data)
        r = 0
        while 2**r < m + r + 1:
            r += 1

        hamming_code = ['0'] * (m + r)

        j = 0
        for i in range(1, len(hamming_code) + 1):
            if (i & (i - 1)) == 0:
                hamming_code[i - 1] = '0'
            else:
                hamming_code[i - 1] = data[j]
                j += 1

        for i in range(r):
            x = 2**i
            parity = 0
            for j in range(x - 1, len(hamming_code), 2 * x):
                parity ^= sum(int(bit) for bit in hamming_code[j:j + x])
            hamming_code[x - 1] = str(parity % 2)

        return ''.join(hamming_code)

    def decode(self, encoded_data):
        """Декодирует данные, закодированные методом Хэмминга.

        Проверяет наличие ошибок в закодированных данных, исправляет одиночные ошибки
        и восстанавливает исходные данные.

        Args:
            encoded_data (str): Закодированные данные, представленные в виде строки из битов.

        Returns:
            str: Декодированные данные без контрольных битов.
        """
        encoded_data = list(encoded_data)
        n = len(encoded_data)
        r = 0
        while 2**r < n + 1:
            r += 1

        error_pos = 0
        for i in range(r):
            x = 2**i
            parity = 0
            for j in range(x - 1, n, 2 * x):
                parity ^= sum(int(bit) for bit in encoded_data[j:j + x])
            if parity % 2 != 0:
                error_pos += x

        if error_pos:
            encoded_data[error_pos - 1] = '1' if encoded_data[error_pos - 1] == '0' else '0'

        decoded_data = []
        for i in range(1, n + 1):
            if (i & (i - 1)) != 0:
                decoded_data.append(encoded_data[i - 1])

        return ''.join(decoded_data)
