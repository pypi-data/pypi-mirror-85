# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['termynal']

package_data = \
{'': ['*'], 'termynal': ['assets/*']}

install_requires = \
['markdown']

extras_require = \
{'mkdocs': ['mkdocs']}

entry_points = \
{'markdown.extensions': ['termynal = termynal.markdown:TermynalExtension'],
 'mkdocs.plugins': ['termynal = termynal.plugin:TermynalPlugin']}

setup_kwargs = {
    'name': 'termynal',
    'version': '0.2.0',
    'description': '',
    'long_description': '# Termynal\n\n<!-- termynal -->\n\n```\n$ pip install termynal\n---> 100%\nInstalled\n```\n\n## Usage\n\nUse `<!-- termynal -->` before code block\n\n````\n<!-- termynal -->\n\n```\n// code\n```\n````\n\nor `console` in code block\n\n````\n```console\n// code\n```\n````\n\nThanks [ines](https://github.com/ines/termynal)\n',
    'author': 'Danil Akhtarov',
    'author_email': 'daxartio@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/termynal',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
