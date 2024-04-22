"""
caesar_cipher.py - программа для симметричного шифрования и расшифрования текста
с помощью шифра Цезаря.

Функции:
    - caesar_cipher(text, key, n): Функция для шифрования и расшифрования текста 
        с использованием шифра Цезаря.
    - encrypt_decrypt_worker(input_queue, output_queue): Функция для работы с потоком,
        которая принимает текст, ключ, мощность алфавита и действие (шифрование или
        расшифрование) из очереди, выполняет шифрование или расшифрование и помещает
        результат в выходную очередь.
"""

def caesar_cipher(text, key, n):
    """
    Шифрует или расшифровывает текст с использованием шифра Цезаря.

    Аргументы:
        text (str): Исходный текст для шифрования или расшифрования.
        key (int): Ключ шифра, определяющий сдвиг символов в алфавите.
        n (int): Мощность алфавита, количество символов, используемых для шифрования.

    Возвращает:
        str: Зашифрованный или расшифрованный текст.
    """
    result = ""
    for char in text:
        if char.isalpha():
            shift = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - shift + key) % n + shift)
        else:
            result += char
    return result

def encrypt_decrypt_worker(input_queue, output_queue):
    """
    Функция для работы с потоком, которая принимает текст, ключ, мощность алфавита и 
    действие (шифрование или расшифрование) из очереди, выполняет шифрование или 
    расшифрование и помещает результат в выходную очередь.

    Аргументы:
        input_queue (queue.Queue): Очередь входных данных, содержащая текст, ключ, 
            мощность алфавита и действие (шифрование или расшифрование).
        output_queue (queue.Queue): Очередь для вывода результата шифрования или 
            расшифрования.
    """
    while True:
        text, key, n, action = input_queue.get()
        if action == "encrypt":
            result = caesar_cipher(text, key, n)
        elif action == "decrypt":
            result = caesar_cipher(text, -key, n)
        output_queue.put(result)
        input_queue.task_done()
