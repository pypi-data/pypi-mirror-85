# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['typestring_parser']

package_data = \
{'': ['*']}

install_requires = \
['pyparsing>=2.4.7,<3.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.6.1,<2.0.0'],
 ':python_version < "3.9"': ['typing-extensions>=3.7.4.3,<4.0.0.0']}

setup_kwargs = {
    'name': 'typestring-parser',
    'version': '0.1',
    'description': 'Parse type strings into typing instances',
    'long_description': "typestring parser\n=================\n\n|PyPI| |Python Version| |License|\n\n|Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/typestring-parser.svg\n   :target: https://pypi.org/project/typestring-parser/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/typestring-parser\n   :target: https://pypi.org/project/typestring-parser\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/typestring-parser\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Tests| image:: https://github.com/Dominik1123/typestring-parser/workflows/Tests/badge.svg\n   :target: https://github.com/Dominik1123/typestring-parser/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/Dominik1123/typestring-parser/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/Dominik1123/typestring-parser\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nInstallation\n------------\n\nYou can install ``typestring-parser`` via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install typestring-parser\n\n\nUsage\n-----\n\nUse the ``parse`` function to convert type strings into `typing`_ instances:\n\n.. code:: python\n\n   >>> from typestring_parser import parse\n   >>>\n   >>> parse('int')\n   <class 'int'>\n   >>> parse('int or str')\n   typing.Union[int, str]\n   >>> parse('list of str or str')\n   typing.Union[typing.List[str], str]\n   >>> parse('list of (int, str)')\n   typing.List[typing.Tuple[int, str]]\n\n\n.. _PyPI: https://pypi.org/\n.. _pip: https://pip.pypa.io/\n.. _typing: https://docs.python.org/3/library/typing.html\n",
    'author': 'Dominik1123',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Dominik1123/typestring-parser',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.9,<4.0.0',
}


setup(**setup_kwargs)
