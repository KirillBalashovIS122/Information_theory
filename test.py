import math

def calculate_alphabet_size(input_text):
    """
    Вычисляет размер алфавита в тексте.
    """
    return len(set(char for char in input_text.lower() if char.isalpha()))

def calculate_hartley_entropy(alphabet_size):
    """
    Вычисляет энтропию по Хартли для заданного размера алфавита.
    """
    return math.log2(alphabet_size)

def calculate_shannon_entropy(input_text):
    """
    Вычисляет энтропию по Шеннону для заданного текста.
    """
    char_chance = {}
    for char in input_text.lower():
        if char.isalpha():
            if char in char_chance:
                char_chance[char] += 1
            else:
                char_chance[char] = 1

    shannon_entropy = 0
    total_char_count = sum(char_chance.values())
    for freq in char_chance.values():
        chance = freq / total_char_count
        shannon_entropy -= chance * math.log2(chance)

    return shannon_entropy

def calculate_redundancy(alphabet_size, shannon_entropy):
    """
    Вычисляет избыточность текста на основе размера алфавита и энтропии по Шеннону.
    """
    return 1 - (shannon_entropy / math.log2(alphabet_size))

def main():
    """
    Основная функция для вычисления и вывода мощности алфавита, энтропии по Хартли, энтропии по Шеннону и избыточности текста.
    """
    file_path = input("Введите путь к файлу: ")
    with open(file_path, 'r', encoding='utf-8') as file:  # Добавлен encoding для корректной работы с текстами в разных кодировках
        text_content = file.read()

    alphabet_size = calculate_alphabet_size(text_content)
    if alphabet_size == 0:
        print("Текст не содержит буквенных символов.")
        return

    hartley_entropy = calculate_hartley_entropy(alphabet_size)
    shannon_entropy = calculate_shannon_entropy(text_content)
    redundancy = calculate_redundancy(alphabet_size, shannon_entropy)

    print(f"Мощность алфавита: {alphabet_size}")
    print(f"Энтропия по Хартли: {hartley_entropy}")
    print(f"Энтропия по Шеннону: {shannon_entropy}")
    print(f"Избыточность алфавита: {redundancy}")

if __name__ == "__main__":
    main()
