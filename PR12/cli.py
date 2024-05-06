import multiprocessing
import requests

# Функция для загрузки русского словаря
def download_russian_dictionary():
    response = requests.get('https://raw.githubusercontent.com/danakt/russian-words/master/russian.txt')
    text = response.content.decode('cp1251')
    with open('russian.txt', 'wb') as ru:
        ru.write(text.encode('utf-8'))

# Функция для расшифровки строки с помощью шифра Цезаря
def caesar_decrypt(ciphertext, shift):
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    decrypted_text = ''
    for char in ciphertext:
        if char in alphabet:
            shifted_index = (alphabet.index(char) - shift) % len(alphabet)
            decrypted_text += alphabet[shifted_index]
        else:
            decrypted_text += char
    return decrypted_text

# Функция для поиска ключа методом брутфорса
def brute_force(ciphertext, pool_size=4):
    pool = multiprocessing.Pool(pool_size)
    decrypted_options = []

    def decrypt_with_shift(shift):
        decrypted_text = caesar_decrypt(ciphertext, shift)
        # Проверяем, является ли расшифрованный текст похожим на русский с помощью словаря
        with open('russian.txt', 'r', encoding='utf-8') as f:
            russian_words = set(word.strip().lower() for word in f)
            decrypted_words = decrypted_text.split()
            russian_word_count = sum(word.lower() in russian_words for word in decrypted_words)
            if russian_word_count / len(decrypted_words) > 0.5:
                decrypted_options.append((shift, decrypted_text))

    # Перебираем возможные сдвиги в пуле процессов
    pool.map(decrypt_with_shift, range(1, len('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')))
    pool.close()
    pool.join()

    return decrypted_options

# Основная часть программы
def main():
    # Загружаем русский словарь
    download_russian_dictionary()

    # Зашифрованный текст
    ciphertext = input("Введите зашифрованную строку: ")

    # Брутфорс атака
    options = brute_force(ciphertext)

    # Записываем варианты в файл
    with open('options.txt', 'w', encoding='utf-8') as f:
        for shift, decrypted_text in options:
            f.write(f"Ключ: {shift}, Расшифрованный текст: {decrypted_text}\n")

if __name__ == "__main__":
    main()
