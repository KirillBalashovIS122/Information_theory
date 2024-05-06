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
def brute_force(ciphertext):
    decrypted_options = []

    # Генерируем все возможные варианты для каждого сдвига
    for shift in range(1, len('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')):
        decrypted_text = caesar_decrypt(ciphertext, shift)
        decrypted_options.append((shift, decrypted_text))

    # Фильтруем только тексты, похожие на русский
    with open('russian.txt', 'r', encoding='utf-8') as f:
        russian_words = set(word.strip().lower() for word in f)
    decrypted_options = [(shift, text) for shift, text in decrypted_options
                         if sum(word.lower() in russian_words for word in text.split()) / len(text.split()) > 0.5]

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
