# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tinymce']

package_data = \
{'': ['*'], 'tinymce': ['templates/tinymce/*']}

install_requires = \
['Django>=2.2,<3.2']

extras_require = \
{'docs': ['Sphinx>=3.3.0,<4.0.0',
          'sphinx-rtd-theme>=0.5.0,<0.6.0',
          'myst-parser>=0.12.10,<0.13.0'],
 'spellcheck': ['pyenchant>=3.1.1,<4.0.0']}

setup_kwargs = {
    'name': 'django-tinymce4-widget',
    'version': '6.1.0',
    'description': 'A Django application that provides a TinyMCE 4 editor widget without any static files',
    'long_description': '# django-tinymce4-widget\n\n<p align="center">\n  <a href="https://github.com/browniebroke/django-tinymce4-widget/actions?query=workflow%3ACI">\n    <img alt="CI Status" src="https://img.shields.io/github/workflow/status/browniebroke/django-tinymce4-widget/CI?label=CI&logo=github&style=flat-square">\n  </a>\n  <a href="https://django-tinymce4-widget.readthedocs.io">\n    <img src="https://img.shields.io/readthedocs/django-tinymce4-widget.svg?logo=read-the-docs&logoColor=fff&style=flat-square" alt="Documentation Status">\n  </a>\n  <a href="https://codecov.io/gh/browniebroke/django-tinymce4-widget">\n    <img src="https://img.shields.io/codecov/c/github/browniebroke/django-tinymce4-widget.svg?logo=codecov&logoColor=fff&style=flat-square" alt="Test coverage">\n  </a>\n</p>\n<p align="center">\n  <a href="https://python-poetry.org/">\n    <img src="https://img.shields.io/badge/packaging-poetry-299bd7?style=flat-square&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAASCAYAAABrXO8xAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAJJSURBVHgBfZLPa1NBEMe/s7tNXoxW1KJQKaUHkXhQvHgW6UHQQ09CBS/6V3hKc/AP8CqCrUcpmop3Cx48eDB4yEECjVQrlZb80CRN8t6OM/teagVxYZi38+Yz853dJbzoMV3MM8cJUcLMSUKIE8AzQ2PieZzFxEJOHMOgMQQ+dUgSAckNXhapU/NMhDSWLs1B24A8sO1xrN4NECkcAC9ASkiIJc6k5TRiUDPhnyMMdhKc+Zx19l6SgyeW76BEONY9exVQMzKExGKwwPsCzza7KGSSWRWEQhyEaDXp6ZHEr416ygbiKYOd7TEWvvcQIeusHYMJGhTwF9y7sGnSwaWyFAiyoxzqW0PM/RjghPxF2pWReAowTEXnDh0xgcLs8l2YQmOrj3N7ByiqEoH0cARs4u78WgAVkoEDIDoOi3AkcLOHU60RIg5wC4ZuTC7FaHKQm8Hq1fQuSOBvX/sodmNJSB5geaF5CPIkUeecdMxieoRO5jz9bheL6/tXjrwCyX/UYBUcjCaWHljx1xiX6z9xEjkYAzbGVnB8pvLmyXm9ep+W8CmsSHQQY77Zx1zboxAV0w7ybMhQmfqdmmw3nEp1I0Z+FGO6M8LZdoyZnuzzBdjISicKRnpxzI9fPb+0oYXsNdyi+d3h9bm9MWYHFtPeIZfLwzmFDKy1ai3p+PDls1Llz4yyFpferxjnyjJDSEy9CaCx5m2cJPerq6Xm34eTrZt3PqxYO1XOwDYZrFlH1fWnpU38Y9HRze3lj0vOujZcXKuuXm3jP+s3KbZVra7y2EAAAAAASUVORK5CYII=" alt="Poetry">\n  </a>\n  <a href="https://github.com/ambv/black">\n    <img src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square" alt="black">\n  </a>\n  <a href="https://github.com/pre-commit/pre-commit">\n    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat-square" alt="pre-commit">\n  </a>\n</p>\n<p align="center">\n  <a href="https://pypi.org/project/django-tinymce4-widget/">\n    <img src="https://img.shields.io/pypi/v/django-tinymce4-widget.svg?logo=python&logoColor=fff&style=flat-square" alt="PyPi Status">\n  </a>\n  <img src="https://img.shields.io/pypi/pyversions/django-tinymce4-widget.svg?style=flat-square&logo=python&logoColor=fff" alt="pyversions">\n  <img src="https://img.shields.io/pypi/l/django-tinymce4-widget.svg?style=flat-square" alt="license">\n</p>\n\n**django-tinymce4-widget** is a reworked fork of [django-tinymce4-lite](https://github.com/romanvm/django-tinymce4-lite). It provides a minimal [TinyMCE 4](https://www.tinymce.com/) editor widget that can be used in Django forms.\n\nThis version **does not** include any static files, it\'s using the TinyMCE from the CDN by default.\n\n**Warning**: TinyMCE 4 is incompatible with TinyMCE 3. Read [TinyMCE](https://www.tinymce.com/) docs for more information about how to configure TimyMCE 4 editor widget.\n\n## Compatibility\n\n- **Python**: 3.6-3.8\n- **Django**: 2.2-3.1\n\n## Quick Start\n\nInstall `django-tinymce4-widget`:\n\n    $ pip install django-tinymce4-widget\n\nAdd `tinymce` to `INSTALLED_APPS` in `settings.py` for your Django project:\n\n```python\nINSTALLED_APPS = (\n    ...\n    \'tinymce\',\n)\n```\n\nAdd `tinymce.urls` to `urls.py` for your project:\n\n```python\nurlpatterns = [\n    ...\n    url(r\'^tinymce/\', include(\'tinymce.urls\')),\n    ...\n]\n```\n\nIn your code:\n\n```python\nfrom django.db import models\nfrom tinymce import HTMLField\n\nclass MyModel(models.Model):\n    ...\n    content = HTMLField(\'Content\')\n```\n\nIn Django Admin the widget is used automatically for all models that have `HTMLField` fields. If you are using TinyMCE 4 in your website forms, add `form.media` variable into your templates:\n\n```django\n<!DOCTYPE html>\n<html>\n<head>\n  ...\n  {{ form.media }}\n</head>\n<body>\n...\n</body>\n</html>\n```\n\n## Documentation\n\nThe full documentation is available at <http://django-tinymce4-widget.readthedocs.io>\n',
    'author': 'Bruno Alla',
    'author_email': 'alla.brunoo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/browniebroke/django-tinymce4-widget',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
