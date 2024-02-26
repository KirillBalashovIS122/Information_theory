from morse_code import *

def main():
    while True:
        print("Choose an action:")
        print("1. Encoding of text in Morse code.")
        print("2. Decoding text from Morse code.")
        print("3. Exit.")

        choice = input("Enter the action number: ")

        if choice == "1":
            text = input("Enter the text to be encoded: ")
            encoded_text = encode_morse(text)
            print(f"Encoded text: {encoded_text}")
            

        elif choice == "2":
            morse_code = input("Enter the Morse code to decode: ")
            decoded_text = decode_morse(morse_code)
            print(f"Decoded text: {decoded_text}")
            

        elif choice == "3":
            break

        else:
            print("Incorrect input!")
            break

if __name__ == '__main__':
    main()
