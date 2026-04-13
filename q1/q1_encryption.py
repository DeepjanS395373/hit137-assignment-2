"""
HIT137 Assignment 2 - Question 1
Foundation functions
"""

RAW_FILE = "raw_text.txt"
ENCRYPTED_FILE = "encrypted_text.txt"
DECRYPTED_FILE = "decrypted_text.txt"


def get_shift_values():
    shift1 = int(input("Enter shift1: "))
    shift2 = int(input("Enter shift2: "))
    return shift1, shift2


def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def write_file(file_path, content):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)


def shift_char(char, shift, base):
    return chr((ord(char) - ord(base) + shift) % 26 + ord(base))