import re

def parse_judgement_result(response_text):
    pattern = r"\[\[\'?([ABC])\'?\]\]"  # Regex pattern to find [[A]], [[B]], or [[C]]
    matches = re.findall(pattern, response_text)

    if matches:
        return matches[0]  # Return the first match (A, B, or C)
    else:
        return None  # Return None if no match is found

def parse_number_score(input_str):
    pattern = r'\((\d+)\)'  # This pattern matches one or more digits inside parentheses
    matches = re.findall(pattern, input_str)

    # Assuming you want the last matching number
    if matches:
        return int(matches[-1])  # Convert the matched string to an integer

    return None  # Return None or a default value if no match is found


def parse_number_score_2(input_str):
    # First, try to match the [[X]] format
    bracket_pattern = r'\[\[(\d+)\]\]'
    matches = re.findall(bracket_pattern, input_str)
    if matches:
        return int(matches[-1])  # Return the last matched number in this format

    # Next, try to match the "X." format
    matches = re.findall(r'\b(\d+)\.\s', input_str)
    if matches:
        return int(matches[-1])

    # Return the last standalone number found
    match = re.findall(r'\b\d+\b', input_str)
    if match:
        return int(match[-1])  
