"""
HIT137 Assignment 2
Question 2: expression evaluator
"""

INPUT_FILE = "sample_input.txt"
OUTPUT_FILE = "output.txt"


def make_token(token_type, value=None):
    """Create one token as a dictionary."""
    return {
        "type": token_type,
        "value": value,
    }


def make_number_node(value):
    """Create a number node."""
    return {
        "kind": "num",
        "value": value,
    }


def make_unary_node(operator, child):
    """Create a unary operator node."""
    return {
        "kind": "unary",
        "operator": operator,
        "child": child,
    }


def make_binary_node(operator, left, right):
    """Create a binary operator node."""
    return {
        "kind": "binary",
        "operator": operator,
        "left": left,
        "right": right,
    }


def read_input_file(file_path):
    """Read all lines from an input file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.readlines()


def write_output_file(file_path, content):
    """Write final output text to a file."""
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)


def is_implicit_multiplication_needed(prev_token, next_token):
    """Return True if implicit multiplication should be inserted."""
    if prev_token is None:
        return False

    prev_type = prev_token["type"]
    next_type = next_token["type"]

    left_ok = prev_type in ("NUM", "RPAREN")
    right_ok = next_type in ("NUM", "LPAREN")

    return left_ok and right_ok


def tokenize(expression):
    """Convert one expression string into tokens."""
    tokens = []
    index = 0
    length = len(expression)
    previous_token = None

    while index < length:
        char = expression[index]

        if char in (" ", "\t", "\n"):
            index += 1
            continue

        if char.isdigit():
            start_index = index

            while index < length and expression[index].isdigit():
                index += 1

            value = int(expression[start_index:index])
            token = make_token("NUM", value)

            if is_implicit_multiplication_needed(previous_token, token):
                tokens.append(make_token("OP", "*"))

            tokens.append(token)
            previous_token = token
            continue

        if char in ("+", "-", "*", "/"):
            token = make_token("OP", char)
            tokens.append(token)
            previous_token = token
            index += 1
            continue

        if char == "(":
            token = make_token("LPAREN", char)

            if is_implicit_multiplication_needed(previous_token, token):
                tokens.append(make_token("OP", "*"))

            tokens.append(token)
            previous_token = token
            index += 1
            continue

        if char == ")":
            token = make_token("RPAREN", char)
            tokens.append(token)
            previous_token = token
            index += 1
            continue

        raise ValueError("Invalid character found.")

    tokens.append(make_token("END"))
    return tokens


def format_tokens(tokens):
    """Format tokens exactly as required."""
    parts = []

    for token in tokens:
        token_type = token["type"]
        token_value = token["value"]

        if token_type == "NUM":
            parts.append(f"[NUM:{token_value}]")
        elif token_type == "OP":
            parts.append(f"[OP:{token_value}]")
        elif token_type == "LPAREN":
            parts.append(f"[LPAREN:{token_value}]")
        elif token_type == "RPAREN":
            parts.append(f"[RPAREN:{token_value}]")
        elif token_type == "END":
            parts.append("[END]")

    return " ".join(parts)


def parse(tokens):
    """Parse tokens into an expression tree."""
    position = {"index": 0}

    def current_token():
        return tokens[position["index"]]

    def eat(expected_type=None, expected_value=None):
        token = current_token()

        if expected_type and token["type"] != expected_type:
            raise ValueError("Unexpected token type")

        if expected_value and token["value"] != expected_value:
            raise ValueError("Unexpected token value")

        position["index"] += 1
        return token

    def parse_expression():
        node = parse_term()

        while True:
            token = current_token()

            if token["type"] == "OP" and token["value"] in ("+", "-"):
                operator = token["value"]
                eat("OP")
                right = parse_term()
                node = make_binary_node(operator, node, right)
            else:
                break

        return node

    def parse_term():
        node = parse_factor()

        while True:
            token = current_token()

            if token["type"] == "OP" and token["value"] in ("*", "/"):
                operator = token["value"]
                eat("OP")
                right = parse_factor()
                node = make_binary_node(operator, node, right)
            else:
                break

        return node

    def parse_factor():
        token = current_token()

        # Unary minus
        if token["type"] == "OP" and token["value"] == "-":
            eat("OP")
            child = parse_factor()
            return make_unary_node("neg", child)

        # Unary plus → ERROR
        if token["type"] == "OP" and token["value"] == "+":
            raise ValueError("Unary plus not allowed")

        # Number
        if token["type"] == "NUM":
            eat("NUM")
            return make_number_node(token["value"])

        # Parentheses
        if token["type"] == "LPAREN":
            eat("LPAREN")
            node = parse_expression()
            eat("RPAREN")
            return node

        raise ValueError("Invalid expression")

    tree = parse_expression()

    if current_token()["type"] != "END":
        raise ValueError("Unexpected trailing tokens")

    return tree
