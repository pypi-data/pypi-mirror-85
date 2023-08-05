# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['print_dict']

package_data = \
{'': ['*']}

install_requires = \
['yapf>=0.30.0,<0.31.0']

entry_points = \
{'console_scripts': ['print-dict = print_dict.cli:cli']}

setup_kwargs = {
    'name': 'print-dict',
    'version': '0.1.14',
    'description': '',
    'long_description': '\n# print-dict\n\n## Motivation\n\nApparently, pretty-printing nested python dictionaries with values such as classes and functions (where you can\'t use `json.dumps`) is\nnot as straightforward as you would think.\n\nSee: https://stackoverflow.com/questions/3229419/how-to-pretty-print-nested-dictionaries\n\nThis library tries to make it a little bit easier.\n\n## Install\n\n```\n$ pip install -U print-dict\n```\n\n## Usage\n\n```python\nfrom print_dict import pd\npd({\'key\': \'value\'})\n\n# Or\n\nfrom print_dict import print_dict\nprint_dict({\'key\': \'value\'})\n```\n\n## Example 1\n\nCode:\n\n```python\nfrom print_dict import pd\n\ndict1 = {\n    \'key\': \'value\'\n}\n\npd(dict1)\n```\n\nOutput:\n\n```\n{\n    \'key\': \'value\'\n}\n```\n\n## Example 2\n\nCode:\n\n```python\nfrom print_dict import pd\n\n\nclass Object1:\n    pass\n\n\nclass Object2:\n\n    def __repr__(self):\n        return "<Object2 info>"\n\n\ndef custom_method():\n    pass\n\n\nobject1 = Object1()\n\ndata = {\n    "one": "value-one",\n    "two": "value-two",\n    "three": "value-three",\n    "four": {\n        \'1\': \'1\', \'2\': \'2\', \'3\': [1, 2, 3, 4, 5], \'4\': {\n            \'method\': custom_method,\n            \'tuple\': (1, 2),\n            \'unicode\': u\'\\u2713\',\n            \'ten\': \'value-ten\',\n            \'eleven\': \'value-eleven\',\n            \'3\': [1, 2, 3, 4]\n        }\n    },\n    "object1": object1,\n    "object2": Object2(),\n    "class": Object1\n\n}\n\npd(data)\n\n```\n\nOutput:\n\n```\n\n{\n    \'one\': \'value-one\',\n    \'two\': \'value-two\',\n    \'three\': \'value-three\',\n    \'four\': {\n        \'1\': \'1\',\n        \'2\': \'2\',\n        \'3\': [1, 2, 3, 4, 5],\n        \'4\': {\n            \'method\': <function custom_method at 0x7ff6ecd03e18>,\n            \'tuple\': (1, 2),\n            \'unicode\': \'✓\',\n            \'ten\': \'value-ten\',\n            \'eleven\': \'value-eleven\',\n            \'3\': [1, 2, 3, 4]\n        }\n    },\n    \'object1\': <__main__.Object1 object at 0x7ff6ecc588d0>,\n    \'object2\': <Object2 info>,\n    \'class\': <class \'__main__.Object1\'>\n}\n\n\n```\n\n',
    'author': 'Eyal Levin',
    'author_email': 'eyalev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
