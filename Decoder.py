def string_to_binary(s):
    return ''.join(format(ord(char), '08b') for char in s)


def binary_string_to_text(binary_string):
    n = 8
    binary_values = [binary_string[i:i + n] for i in range(0, len(binary_string), n)]
    ascii_characters = [chr(int(bv, 2)) for bv in binary_values]
    return ''.join(ascii_characters)