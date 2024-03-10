import argparse
import json
import os
from huffman_coding import build_huffman_tree, build_encoding_table, encode_text, decode_text, calculate_entropy, calculate_compression_ratio

def read_frequency_table(encoding_file):
    with open(encoding_file, 'r') as f:
        frequency_table = json.load(f)
    return frequency_table

def write_encoded_text(output_file, encoded_text):
    with open(output_file, 'wb') as f:
        f.write(bytes(int(encoded_text[i:i+8], 2) for i in range(0, len(encoded_text), 8)))

def main():
    parser = argparse.ArgumentParser(description="Unicode to Huffman Coding and vice versa")
    parser.add_argument("input_file", help="Input file (Unicode or encoded)")
    parser.add_argument("output_file", help="Output file")
    parser.add_argument("--encoding_file", help="Huffman encoding JSON file")
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file
    encoding_file = args.encoding_file

    # Чтение текста из входного файла
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    # Определение режима работы программы (кодирование или декодирование)
    if encoding_file:
        # Декодирование из кода Хаффмана
        frequency_table = read_frequency_table(encoding_file)
        root = build_huffman_tree(frequency_table)
        decoded_text = decode_text(text, root)
        output_text = decoded_text
    else:
        # Кодирование в код Хаффмана
        frequency_table = {char: text.count(char) for char in set(text)}
        root = build_huffman_tree(frequency_table)
        encoding_table = build_encoding_table(root)
        encoded_text = encode_text(text, encoding_table)
        output_text = encoded_text
        # Сохраняем таблицу частот в JSON файл
        with open(output_file + ".json", 'w') as f:
            json.dump(frequency_table, f)

    # Запись результата в выходной файл
    if encoding_file:
        write_encoded_text(output_file, output_text)
    else:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output_text)

    # Вычисление размеров файлов и степени сжатия
    original_size = os.path.getsize(input_file)
    compressed_size = os.path.getsize(output_file)
    entropy = calculate_entropy(frequency_table)
    compression_ratio = calculate_compression_ratio(original_size, compressed_size)

    # Вывод информации в CLI
    print("Original File Size:", original_size, "bytes")
    print("Compressed File Size:", compressed_size, "bytes")
    print("Entropy:", entropy)
    print("Average Bits per Symbol in Compressed File:", compressed_size * 8 / len(text))
    print("Compression Ratio:", compression_ratio)

if __name__ == "__main__":
    main()
