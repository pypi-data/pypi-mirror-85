## texting
##### misc for string

### Functions
- has_ansi
- lange
- pad: lpad, mpad, rpad
- str_value

### Usage
```python
from texting.has_ansi import has_ansi
from texting.lange import lange
words = [
    'peace',
    '\u001B[4mwar\u001B[0m',
    '\u001b[38;2;255;255;85mtolstoy\u001b[0m',
]

for word in words:
    print(f'[{word}] [has_ansi] ({has_ansi(word)}) [lange] ({lange(word)})')
```