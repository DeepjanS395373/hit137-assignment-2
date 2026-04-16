"""
HIT137 Assignment 2
Question 1: file encryption and decryption
"""

RAW_FILE = "raw_text.txt"
ENCRYPTED_FILE = "encrypted_text.txt"
DECRYPTED_FILE = "decrypted_text.txt"
ALPHABET_SIZE = 26


def get_shift_values():
    """Read shift1 and shift2 from the user."""
    shift1 = int(input("Enter shift1: "))
    shift2 = int(input("Enter shift2: "))
    return shift1, shift2


def read_file(file_path):
    """Read and return all text from a file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def write_file(file_path, content):
    """Write text content to a file."""
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)


def shift_char(char, shift, base_char):
    """Shift one alphabetic character with wrap-around."""
    offset = ord(char) - ord(base_char)
    new_offset = (offset + shift) % ALPHABET_SIZE
    return chr(ord(base_char) + new_offset)


def encrypt_char(char, shift1, shift2):
    """Encrypt a single character based on assignment rules."""

    if "a" <= char <= "m":
        return shift_char(char, shift1 * shift2, "a")

    if "n" <= char <= "z":
        return shift_char(char, -(shift1 + shift2), "a")

    if "A" <= char <= "M":
        return shift_char(char, -shift1, "A")

    if "N" <= char <= "Z":
        return shift_char(char, shift2 ** 2, "A")

    return char


def encrypt_text(text, shift1, shift2):
    """Encrypt full text."""
    result = []

    for char in text:
        result.append(encrypt_char(char, shift1, shift2))

    return "".join(result)