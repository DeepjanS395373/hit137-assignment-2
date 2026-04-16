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
    """Encrypt one character and return its rule label."""
    if "a" <= char <= "m":
        encrypted = shift_char(char, shift1 * shift2, "a")
        return encrypted, "lower_first"

    if "n" <= char <= "z":
        encrypted = shift_char(char, -(shift1 + shift2), "a")
        return encrypted, "lower_second"

    if "A" <= char <= "M":
        encrypted = shift_char(char, -shift1, "A")
        return encrypted, "upper_first"

    if "N" <= char <= "Z":
        encrypted = shift_char(char, shift2 ** 2, "A")
        return encrypted, "upper_second"

    return char, "other"


def encrypt_text(text, shift1, shift2):
    """Encrypt full text and store rule history."""
    encrypted_chars = []
    rule_history = []

    for char in text:
        encrypted_char, rule_used = encrypt_char(char, shift1, shift2)
        encrypted_chars.append(encrypted_char)
        rule_history.append(rule_used)

    return "".join(encrypted_chars), rule_history


def decrypt_char(char, rule_used, shift1, shift2):
    """Decrypt one character using the stored rule label."""
    if rule_used == "lower_first":
        return shift_char(char, -(shift1 * shift2), "a")

    if rule_used == "lower_second":
        return shift_char(char, shift1 + shift2, "a")

    if rule_used == "upper_first":
        return shift_char(char, shift1, "A")

    if rule_used == "upper_second":
        return shift_char(char, -(shift2 ** 2), "A")

    return char


def decrypt_text(text, rule_history, shift1, shift2):
    """Decrypt full text using stored rule history."""
    decrypted_chars = []

    for index, char in enumerate(text):
        rule_used = rule_history[index]
        decrypted_chars.append(
            decrypt_char(char, rule_used, shift1, shift2)
        )

    return "".join(decrypted_chars)


def verify_text(original_text, decrypted_text):
    """Return True if decrypted text matches original text."""
    return original_text == decrypted_text


def run_q1():
    """Run the full Question 1 workflow."""
    shift1, shift2 = get_shift_values()

    raw_text = read_file(RAW_FILE)

    encrypted_text, rule_history = encrypt_text(
        raw_text,
        shift1,
        shift2,
    )
    write_file(ENCRYPTED_FILE, encrypted_text)

    decrypted_text = decrypt_text(
        encrypted_text,
        rule_history,
        shift1,
        shift2,
    )
    write_file(DECRYPTED_FILE, decrypted_text)

    if verify_text(raw_text, decrypted_text):
        print("Verification successful.")
    else:
        print("Verification failed.")


def main():
    """Run Question 1 safely."""
    try:
        run_q1()
    except FileNotFoundError:
        print("Input file not found.")
    except ValueError:
        print("Please enter valid integer values for shifts.")


if __name__ == "__main__":
    main()