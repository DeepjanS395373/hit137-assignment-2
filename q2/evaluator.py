"""
HIT137 Assignment 2
Question 2: arithmetic expression evaluator
"""

INPUT_FILE = "sample_input.txt"
OUTPUT_FILE = "output.txt"


def make_token(token_type, value=None):
    """Create a token dictionary."""
    return {"type": token_type, "value": value}


def make_number_node(value):
    """Create a number tree node."""
    return {"kind": "num", "value": value}


def make_unary_node(operator, child):
    """Create a unary tree node."""
    return {"kind": "unary", "operator": operator, "child": child}


def make_binary_node(operator, left, right):
    """Create a binary tree node."""
    return {
        "kind": "binary",
        "operator": operator,
        "left": left,
        "right": right,
    }


def read_input_file(file_path):
    """Read all lines from a file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.readlines()


def write_output_file(file_path, content):
    """Write text content to a file."""
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)


def parse_number(number_text):
    """Convert number text into int or float."""
    if "." in number_text:
        return float(number_text)

    return int(number_text)


def is_number_char(char):
    """Return True for digit or decimal point."""
    return char.isdigit() or char == "."


def is_implicit_multiplication_needed(prev_token, next_token):
    """Return True if implicit multiplication is needed."""
    if prev_token is None:
        return False

    left_ok = prev_token["type"] in ("NUM", "RPAREN")
    right_ok = next_token["type"] in ("NUM", "LPAREN")

    return left_ok and right_ok


def read_number(expression, start_index):
    """Read an integer or decimal number from expression."""
    index = start_index
    decimal_count = 0

    while index < len(expression) and is_number_char(expression[index]):
        if expression[index] == ".":
            decimal_count += 1

        if decimal_count > 1:
            raise ValueError("Invalid decimal number")

        index += 1

    number_text = expression[start_index:index]

    if number_text == ".":
        raise ValueError("Invalid decimal number")

    if number_text.startswith(".") or number_text.endswith("."):
        raise ValueError("Invalid decimal number")

    return parse_number(number_text), index


def tokenize(expression):
    """Convert expression text into tokens."""
    tokens = []
    index = 0
    previous_token = None

    while index < len(expression):
        char = expression[index]

        if char in (" ", "\t", "\n"):
            index += 1
            continue

        if char.isdigit() or char == ".":
            value, index = read_number(expression, index)
            token = make_token("NUM", value)

            if is_implicit_multiplication_needed(previous_token, token):
                tokens.append(make_token("OP", "*"))

            tokens.append(token)
            previous_token = token
            continue

        if char in "+-*/":
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

        raise ValueError("Invalid character")

    tokens.append(make_token("END"))
    return tokens


def parse(tokens):
    """Parse tokens using recursive descent."""
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

        while (
            current_token()["type"] == "OP"
            and current_token()["value"] in ("+", "-")
        ):
            operator = current_token()["value"]
            eat("OP")
            right = parse_term()
            node = make_binary_node(operator, node, right)

        return node

    def parse_term():
        node = parse_factor()

        while (
            current_token()["type"] == "OP"
            and current_token()["value"] in ("*", "/")
        ):
            operator = current_token()["value"]
            eat("OP")
            right = parse_factor()
            node = make_binary_node(operator, node, right)

        return node

    def parse_factor():
        token = current_token()

        if token["type"] == "OP" and token["value"] == "-":
            eat("OP")
            child = parse_factor()
            return make_unary_node("neg", child)

        if token["type"] == "OP" and token["value"] == "+":
            raise ValueError("Unary plus is not supported")

        if token["type"] == "NUM":
            eat("NUM")
            return make_number_node(token["value"])

        if token["type"] == "LPAREN":
            eat("LPAREN")
            node = parse_expression()
            eat("RPAREN")
            return node

        raise ValueError("Invalid expression")

    tree = parse_expression()

    if current_token()["type"] != "END":
        raise ValueError("Unexpected trailing input")

    return tree


def format_number(value):
    """Format numbers without unnecessary decimal places."""
    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))

        text = f"{value:.4f}"
        return text.rstrip("0").rstrip(".")

    return str(value)


def format_tokens(tokens):
    """Format tokens as required."""
    parts = []

    for token in tokens:
        token_type = token["type"]
        token_value = token["value"]

        if token_type == "NUM":
            parts.append(f"[NUM:{format_number(token_value)}]")
        elif token_type == "OP":
            parts.append(f"[OP:{token_value}]")
        elif token_type == "LPAREN":
            parts.append(f"[LPAREN:{token_value}]")
        elif token_type == "RPAREN":
            parts.append(f"[RPAREN:{token_value}]")
        elif token_type == "END":
            parts.append("[END]")

    return " ".join(parts)


def format_tree(node):
    """Format an expression tree in prefix style."""
    if node["kind"] == "num":
        return format_number(node["value"])

    if node["kind"] == "unary":
        child_text = format_tree(node["child"])
        return f"({node['operator']} {child_text})"

    left_text = format_tree(node["left"])
    right_text = format_tree(node["right"])
    return f"({node['operator']} {left_text} {right_text})"


def evaluate_tree(node):
    """Evaluate an expression tree."""
    if node["kind"] == "num":
        return node["value"]

    if node["kind"] == "unary":
        child_value = evaluate_tree(node["child"])
        return -child_value

    left_value = evaluate_tree(node["left"])
    right_value = evaluate_tree(node["right"])
    operator = node["operator"]

    if operator == "+":
        return left_value + right_value

    if operator == "-":
        return left_value - right_value

    if operator == "*":
        return left_value * right_value

    if operator == "/":
        if right_value == 0:
            raise ZeroDivisionError("Division by zero")
        return left_value / right_value

    raise ValueError("Invalid operator")


def format_result(value):
    """Format result to maximum four decimal places."""
    return format_number(value)


def process_expression(expression):
    """Process one expression."""
    stripped = expression.strip()

    try:
        tokens = tokenize(stripped)
        tree = parse(tokens)
        tree_text = format_tree(tree)
        token_text = format_tokens(tokens)

        try:
            result_value = evaluate_tree(tree)
            result_text = format_result(result_value)
        except ZeroDivisionError:
            result_text = "ERROR"

        return {
            "input": stripped,
            "tree": tree_text,
            "tokens": token_text,
            "result": result_text,
        }

    except ValueError:
        return {
            "input": stripped,
            "tree": "ERROR",
            "tokens": "ERROR",
            "result": "ERROR",
        }


def build_output_block(result):
    """Build one formatted output block."""
    return "\n".join(
        [
            f"Input: {result['input']}",
            f"Tree: {result['tree']}",
            f"Tokens: {result['tokens']}",
            f"Result: {result['result']}",
        ]
    )


def evaluate_file(input_path: str) -> list[dict]:
    """Evaluate expressions from input file and return results."""
    lines = read_input_file(input_path)
    results = []

    for line in lines:
        if line.strip():
            results.append(process_expression(line))

    return results


def main():
    """Run Question 2."""
    results = evaluate_file(INPUT_FILE)
    blocks = []

    for result in results:
        blocks.append(build_output_block(result))

    write_output_file(OUTPUT_FILE, "\n\n".join(blocks))
    print("Output written successfully.")


if __name__ == "__main__":
    main()