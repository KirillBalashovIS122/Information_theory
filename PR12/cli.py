import multiprocessing
import requests
import threading

def load_russian_words():
    response = requests.get('https://raw.githubusercontent.com/danakt/russian-words/master/russian.txt')
    text = response.content.decode('cp1251')
    with open('russian.txt', 'w', encoding='utf-8') as ru:
        ru.write(text)

def load_english_words():
    response = requests.get('https://raw.githubusercontent.com/dwyl/english-words/master/words.txt')
    text = response.text
    with open('english.txt', 'w', encoding='utf-8') as en:
        en.write(text)

def decrypt_with_shift(text, shift, language='russian'):
    result = ""
    for char in text:
        new_char = char
        if char.isalpha():
            if language == 'russian':
                shift_value = ord('А') if char.isupper() else ord('а')
                new_char = chr((ord(char) - shift_value - shift) % 32 + shift_value)
            elif language == 'english':
                shift_value = ord('A') if char.isupper() else ord('a')
                new_char = chr((ord(char) - shift_value - shift) % 26 + shift_value)
        result += new_char
    return result

def check_meaningful_words(text, words):
    text_words = text.split()
    meaningful_words = []
    for word in text_words:
        if word.lower() in words:
            meaningful_words.append(word)
    return meaningful_words

def decrypt_and_check(args):
    text, shift, language, words = args
    decrypted_text = decrypt_with_shift(text, shift, language)
    meaningful_words = check_meaningful_words(decrypted_text, words)
    if meaningful_words:
        return shift, decrypted_text, meaningful_words
    return None

def brute_force_decrypt(text, language, words, pool_size=4):
    shift_range = 32 if language == 'russian' else 26
    args = [(text, shift, language, words) for shift in range(shift_range)]

    if pool_size > multiprocessing.cpu_count():
        results = map(decrypt_and_check, args)
    else:
        pool = multiprocessing.Pool(processes=pool_size)
        results = pool.map(decrypt_and_check, args)
        pool.close()
        pool.join()

    return [result for result in results if result]

def display_decrypted_options(decrypted_options):
    if not decrypted_options:
        print("Не удалось найти расшифрованный текст с заданными параметрами.")
    for shift, decrypted_text, meaningful_words in decrypted_options:
        print(f"Shift: {shift}")
        print(f"Decrypted Text: {decrypted_text}")
        print(f"Meaningful Words: {', '.join(meaningful_words)}\n")

if __name__ == "__main__":
    try:
        with open('russian.txt', 'r', encoding='utf-8') as file_rus, open('english.txt', 'r', encoding='utf-8') as file_eng:
            russian_words = set(word.strip().lower() for word in file_rus.readlines())
            english_words = set(word.strip().lower() for word in file_eng.readlines())
    except FileNotFoundError:
        russian_thread = threading.Thread(target=load_russian_words)
        english_thread = threading.Thread(target=load_english_words)
        russian_thread.start()
        english_thread.start()
        russian_thread.join()
        english_thread.join()
        with open('russian.txt', 'r', encoding='utf-8') as file_rus, open('english.txt', 'r', encoding='utf-8') as file_eng:
            russian_words = set(word.strip().lower() for word in file_rus.readlines())
            english_words = set(word.strip().lower() for word in file_eng.readlines())

    while True:
        print("1) Начать работу")
        print("2) Выйти")
        choice = input("> ")

        if choice == "1":
            print("Введите зашифрованный текст: ")
            encrypted_text = input(">")
            
            print("Выберите язык для расшифровки:")
            print("1. Русский")
            print("2. Английский")
            print("3. Оба языка")
            lang_choice = input("> ")

            if lang_choice == "1":
                language = 'russian'
                words = russian_words
            elif lang_choice == "2":
                language = 'english'
                words = english_words
            elif lang_choice == "3":
                language = 'both'
                words = russian_words | english_words
            else:
                print("Некорректный выбор языка.")
                continue

            print("Введите мощность (количество процессов): ")
            try:
                pool_size = int(input("> "))
            except ValueError:
                print("Некорректное значение мощности.")
                continue

            decrypted_options = []
            if language == 'both':
                print("Расшифровка на русском языке...")
                decrypted_options.extend(brute_force_decrypt(encrypted_text, 'russian', russian_words, pool_size))
                print("Расшифровка на английском языке...")
                decrypted_options.extend(brute_force_decrypt(encrypted_text, 'english', english_words, pool_size))
            else:
                decrypted_options = brute_force_decrypt(encrypted_text, language, words, pool_size)

            display_decrypted_options(decrypted_options)
        elif choice == "2":
            break
        else:
            print("Некорректный выбор.")
