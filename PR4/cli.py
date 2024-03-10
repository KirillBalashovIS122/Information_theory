import argparse
from huffman_coder import CodeGenerator

def main():
    parser = argparse.ArgumentParser(description="Generate Huffman code for a text file.")
    parser.add_argument("file_path", type=str, help="Path to the text file.")
    args = parser.parse_args()

    cgen = CodeGenerator()
    cgen.gen_code(args.file_path)

if __name__ == "__main__":
    main()
