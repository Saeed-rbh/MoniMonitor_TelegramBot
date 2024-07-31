import re

def extract_float(input_string):
    float_pattern = r'[-+]?\d*\.\d+|\d+'
    match = re.search(float_pattern, input_string)
    if match:
        return float(match.group())
    else:
        return None