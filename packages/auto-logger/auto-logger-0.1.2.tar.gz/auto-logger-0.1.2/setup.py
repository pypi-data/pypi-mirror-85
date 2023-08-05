# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['auto_logger']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'auto-logger',
    'version': '0.1.2',
    'description': 'Automatically add function call logs and method call logs for Python code.',
    'long_description': '# Auto-logger\n\n![CI](https://github.com/duyixian1234/auto-logger/workflows/CI/badge.svg?branch=master)\n\nAutomatically add function call logs and method call logs for Python code.\n\n## Install\n\n```bash\npip install -U auto-logger\n```\n\n## Use\n\n```python\nimport logging\nfrom dataclasses import dataclass\n\nfrom auto_logger import Config, MethodLoggerMeta, logFuncCall,formatJson\n\nlogging.basicConfig(level=logging.INFO)\n\n\n@logFuncCall\ndef add(a: int, b: int):\n    return a + b\n\n\nadd(1, 2) # INFO:auto_logger:CALL FUCNTION <add> WITH ARGS (1, 2) KWARGS {} RETURNS  3\nadd(a=1, b=2) # INFO:auto_logger:CALL FUCNTION <add> WITH ARGS () KWARGS {\'a\': 1, \'b\': 2} RETURNS  3\n\n\n@dataclass\nclass A(metaclass=MethodLoggerMeta):\n    a: int = 0\n\n    def add(self, n: int):\n        self.a += 1\n\n    def abs(self):\n        return abs(self.a)\n\nA().add(1)  # INFO:auto_logger:CALL METHOD <add> OF A(a=0) WITH ARGS (1,) KWARGS {} RETURNS  None\n\n\nConfig.format = formatJson\nA().add(1) # INFO:auto_logger:{"args": [1], "kwargs": {}, "ret": null, "method": "add", "object": "A(a=0)"}\n\nConfig.ignoreMethods[A] = {\'abs\'}\nA().abs() # Log nothing\n```\n',
    'author': 'duyixian',
    'author_email': 'duyixian1234@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/duyixian1234/auto-logger',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
