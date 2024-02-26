# main.py

from huffman import CodeGenerator

def main():
    cgen = CodeGenerator()

    while True:
        print("Choose an option:")
        print("1. Generate Huffman code")
        print("2. Delete all Huffman code history")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            file_path = input("Enter the path to the input file: ")
            cgen.gen_code(file_path)
        elif choice == "2":
            # Add code to delete all history
            pass
        elif choice == "3":
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
