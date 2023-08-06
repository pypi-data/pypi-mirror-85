# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mithrandir']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['lint = scripts:lint',
                     'test = scripts:test',
                     'test_box = scripts:test_box']}

setup_kwargs = {
    'name': 'mithrandir',
    'version': '1.4.1',
    'description': '',
    'long_description': '---\ndescription: Reasoning the logic flow with Magic\n---\n\n# Mithrandir\n\n## Installation\n\nAs much simple as it could be, use `pip` , `pipenv` or `poetry` :\n\n```\n$ pip install mithrandir\n```\n\n{% hint style="info" %}\nRemember to check out the latest version available\n{% endhint %}\n\nOnce you have **Mithrandir** in your presence, let him be your guide...\n\n{% code title="$ python" %}\n```python\n>> from mithrandir import Monad, Op, MonadSignature as Sig\n>> magic = Monad(1) | Op.MAP(lambda x: x + 1)\n>> print("magic = ", magic)\n... "magic = Monad<async_mode=False>[2]"\n>> # Give me your blessing...\n>> print("blessed-value = ", magic.unwrap())\n... "blessed-value = 2"\n```\n{% endcode %}\n\nFor more advanced tutorials and examples, check out the next parts of the document\n\n',
    'author': 'vutr',
    'author_email': 'me@vutr.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
