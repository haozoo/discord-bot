from random import seed
from random import randint
from datetime import datetime


def coder(string):
    dict = {'Q': '\%', 'W': '\^', 'E': '\~', 'R': '\|', 'T': '\[',
            'Y': '\]', 'U': '\<', 'I': '\>', 'O': '\{', 'P': '\}',
            'A': '\@', 'S': '\#', 'D': '\&', 'F': '\*', 'G': '\-',
            'H': '\+', 'J': '\=', 'K': '\(', 'L': '\)', 'Z': '\_',
            'X': '\$', 'C': '\!', 'V': '\?', 'B': '\:', 'N': '\;',
            'M': '\/',
            '1': '\,', '2': '\.',
            '%': 'Q', '^': 'W', '~': 'E', '|': 'R', '[': 'T',
            ']': 'Y', '<': 'U', '>': 'I', '{': 'O', '}': 'P',
            '@': 'A', '#': 'S', '&': 'D', '*': 'F', '-': 'G',
            '+': 'H', '=': 'J', '(': 'K', ')': 'L', '_': 'Z',
            '$': 'X', '!': 'C', '?': 'V', ':': 'B', ';': 'N',
            '/': 'M',
            ',': '1', '.': '2',
            ' ': '  '}

    string = string.upper()
    message = ''

    for letter in string:
        if letter in dict:
            message = message + dict[letter]
        else:
            message = message + letter

    return message


def hotdog():
    # Generate randome number
    seed(datetime.now())

    size = randint(8, 50)
    # Top bun
    top = '-    ' + (' ' * (size // 4)) + ('_' * (size // 2)) + '\n' + \
        '-    ' + (' ' * (size // 4 - 1)) + '(' + ' ' * (size // 2) + ')\n'
    hotdog = '-    ' + '-' * size + '\n' \
        + '-  ' + '(' + (' ' * (size // 4 + 1)) + ('~' * (size // 2)) + (' ' * (size // 4)) + '  )' + '\n' + \
        '-    ' + ('-' * size) + '\n'
    bot = '-    ' + (' ' * (size // 4 - 1)) + '(' + ('_' * (size // 2)) + ')'

    msg = 'Your hotdog is this long:\n' + '```fix\n' + top + \
        '```' + '```diff\n' + hotdog + '```' + '```fix\n' + bot + '```'

    return msg
