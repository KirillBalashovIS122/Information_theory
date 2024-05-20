from collections import defaultdict
from math import log2
from huffman import Huffman

def calculate_entropy(data):
    """Расчет энтропии для исходного текста."""
    frequency = defaultdict(int)
    for symbol in data:
        frequency[symbol] += 1
    total_symbols = len(data)
    entropy = -sum((freq / total_symbols) * log2(freq / total_symbols)
        for freq in frequency.values())
    return entropy

def calculate_compression_ratio(original_size, encoded_size):
    """Расчет степени сжатия."""
    return original_size / encoded_size

def encode_file(input_file, output_file):
    """Кодирование файла."""
    with open(input_file, 'r', encoding='utf-8') as file:  # Указана кодировка 'utf-8'
        data = file.read()
    huffman = Huffman()
    encoded_data = huffman.encode(data)

    with open(output_file, 'w', encoding='utf-8') as file:  
        file.write(encoded_data)
    
    bits_per_symbol = len(encoded_data) / len(data)

    return len(data), len(encoded_data), calculate_entropy(data), bits_per_symbol

def decode_file(input_file, output_file):
    """Декодирование файла."""
    with open(input_file, 'r', encoding='utf-8') as file:  
        encoded_data = file.read()

    huffman = Huffman()
    decoded_data = huffman.decode(encoded_data)

    with open(output_file, 'w', encoding='utf-8') as file:  
        file.write(decoded_data)

    return len(encoded_data), len(decoded_data)
