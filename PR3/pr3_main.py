import math
#hello

def calculate_alphabet_power(text):
    return len(set(text.lower()))

def calculate_hartley_entropy(alphabet_power):
    return math.log2(alphabet_power)

def calculate_shannon_entropy(text):
    frequencies = {}
    for char in text.lower():
        if char.isalpha():
            if char in frequencies:
                frequencies[char] += 1
            else:
                frequencies[char] = 1
    
    shannon_entropy = 0
    total_chars = len(text)
    for freq in frequencies.values():
        probability = freq / total_chars
        shannon_entropy -= probability * math.log2(probability)
    
    return shannon_entropy

def calculate_redundancy(alphabet_power, shannon_entropy):
    return 1 - (shannon_entropy / math.log2(alphabet_power))

file_name = input("Enter the file name: ")
with open(file_name, 'r') as file:
    text = file.read()

alphabet_power = calculate_alphabet_power(text)
hartley_entropy = calculate_hartley_entropy(alphabet_power)
shannon_entropy = calculate_shannon_entropy(text)
redundancy = calculate_redundancy(alphabet_power, shannon_entropy)

print(f"The power of the alphabet: {alphabet_power}")
print(f"Entropy according to Hartley: {hartley_entropy}")
print(f"Entropy according to Shannon: {shannon_entropy}")
print(f"Redundancy of the alphabet: {redundancy}")