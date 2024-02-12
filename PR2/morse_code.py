MORSE_CODE_DICT = {
    'А': '.-',
    'Б': '-...',
    'В': '.--', 
    'Г': '--.', 
    'Д': '-..', 
    'Е': '.', 
    'Ё': '.', 
    'Ж': '...-', 
    'З': '--..', 
    'И': '..', 
    'Й': '.---', 
    'К': '-.-', 
    'Л': '.-..', 
    'М': '--', 
    'Н': '-.', 
    'О': '---', 
    'П': '.--.', 
    'Р': '.-.', 
    'С': '...', 
    'Т': '-', 
    'У': '..-', 
    'Ф': '..-.', 
    'Х': '....', 
    'Ц': '-.-.', 
    'Ч': '---.', 
    'Ш': '----', 
    'Щ': '--.-', 
    'Ъ': '--.--', 
    'Ы': '-.--', 
    'Ь': '-..-', 
    'Э': '..-..', 
    'Ю': '..--', 
    'Я': '.-.-', 
    '0': '-----', 
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', 
    '.': '.-.-.-', ',': '--..--', ';': '-.-.-.', ':': '---...', '?': '..--..', '!': '-.-.--', '-': '-....-', ' ': '\t'
}

def encode_morse(text):
    encoded_text = ''
    for char in text.upper():
        if char in MORSE_CODE_DICT:
            encoded_text += MORSE_CODE_DICT[char] + ' '
    return encoded_text

def decode_morse(morse_code):
    decoded_text = ''
    morse_code += ' '
    key_list = list(MORSE_CODE_DICT.keys())
    val_list = list(MORSE_CODE_DICT.values())
    code = ''
    for symbol in morse_code:
        if symbol != ' ':
            code += symbol
        else:
            if code in val_list:
                index = val_list.index(code)
                decoded_text += key_list[index]
                code = ''
            else:
                decoded_text += ''
    return decoded_text
