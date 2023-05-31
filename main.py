import json
from tkinter import filedialog
import re

def is_python_code_valid(python_code):
    try:
        compile(python_code, "<string>", "exec")
        return True
    except SyntaxError:
        return False


def convert_python_to_javascript(python_code):
    # Define the dictionary to map Python keywords to JavaScript equivalents
    keyword_dict = {
        'and': '&&',
        'or': '||',
        'not': '!',
        'True': 'true',
        'False': 'false',
        'None': 'null',
        'if': 'if',
        'else': 'else',
        'elif': 'else if',
        'while': 'while',
        'for': 'for',
        'in': 'of',
        'range': 'Array.from({length:',
        'len': '.length',
        'def': 'function',
        'return': 'return',
        'print': 'console.log',
        'input': 'prompt',
        'float': 'parseFloat',
        'int': 'parseInt'
    }

    # Use regular expressions to find and replace Python keywords with their JavaScript equivalents
    for python_keyword, js_keyword in keyword_dict.items():
        python_code = re.sub(r'\b{}\b'.format(python_keyword), js_keyword, python_code)

    # Replace '=' with 'var'
    python_code = re.sub(r'(\b\w+\b)\s*=\s*', 'var \\1 = ', python_code)

    # Replace Python-style string formatting with JavaScript-style string formatting
    python_code = re.sub(r'(\{.*?\})', '{$1}', python_code)
    python_code = re.sub(r'%\((.*?)\)[sd]', '{$1}', python_code)

    # Add semicolons at the end of statements if they don't already exist
    python_code = re.sub(r'([^;])\n', '\\1;\n', python_code)

    # Convert Python for loop to JavaScript
    python_code = re.sub(r'for\s+(\w+)\s+in\s+Array\.from\(\{length:\s+(\d+)\}\)', r'for (var \1 = 0; \1 < \2; \1++) {', python_code)

    # Convert Python if statements to JavaScript
    python_code = re.sub(r'if\s+(.*?)\s*:', r'if (\1) {', python_code)
    python_code = re.sub(r'else\s*:', r'} else {', python_code)
    python_code = re.sub(r'elif\s+(.*?)\s*:', r'} else if (\1) {', python_code)

    # Convert Python while loop to JavaScript
    python_code = re.sub(r'while\s+(.*?)\s*:', r'while (\1) {', python_code)

    # Fix indentation
    lines = python_code.splitlines()
    new_lines = []
    indent_level = 0
    for line in lines:
        if line.strip():
            line = '    ' * indent_level + line.strip()
            new_lines.append(line)
            if line.endswith('{'):
                indent_level += 1
            elif line.endswith('}'):
                indent_level -= 1
    javascript_code = '\n'.join(new_lines)

    return javascript_code


# input_path = input('Enter input path: ')
input_path = filedialog.askopenfile(title="SELECIONE O ARQUIVO DE ENTRADA")
input_path = input_path.name

# output_file_path = input("Enter output path: ")
output_file_path = "output.js"

with open(input_path, 'r') as f:
    python_code = f.read()

if not is_python_code_valid(python_code):
    print('PYTHON CODE NOT COMPILABLE, EXITING...')
    exit(1)

# Convert the Python code to JavaScript
javascript_code = convert_python_to_javascript(python_code)

# clear output file
with open(output_file_path, 'w') as f:
    f.write('')

# Print the formatted JavaScript code
formatted_code = re.sub(r';{2,}', ';', javascript_code)
formatted_code = formatted_code[0:] + ';}'
lines = formatted_code.split(';')
for line in lines:
    if line:
        print('    ' + line.strip())
        with open(output_file_path, 'a') as f:
            f.write('    ' + line.strip() + '\n')
