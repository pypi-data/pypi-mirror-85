# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['texting',
 'texting.bracket',
 'texting.chars',
 'texting.enum',
 'texting.enum.brackets',
 'texting.enum.quotes',
 'texting.enum.regexes',
 'texting.enum.regexes.strings',
 'texting.fold',
 'texting.has_ansi',
 'texting.indexing',
 'texting.lange',
 'texting.lines',
 'texting.pad',
 'texting.phrasing',
 'texting.ripper',
 'texting.str_util',
 'texting.str_value',
 'texting.tap']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'texting',
    'version': '0.0.12',
    'description': 'misc for string',
    'long_description': "## texting\n##### misc for string\n\n### Functions\n- has_ansi\n- lange\n- pad: lpad, mpad, rpad\n- str_value\n\n### Usage\n```python\nfrom texting.has_ansi import has_ansi\nfrom texting.lange import lange\nwords = [\n    'peace',\n    '\\u001B[4mwar\\u001B[0m',\n    '\\u001b[38;2;255;255;85mtolstoy\\u001b[0m',\n]\n\nfor word in words:\n    print(f'[{word}] [has_ansi] ({has_ansi(word)}) [lange] ({lange(word)})')\n```",
    'author': 'Hoyeung Wong',
    'author_email': 'hoyeungw@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pydget/texting.git',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
