from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='localize-py',
      version='0.8.1',
      description='Localization simplified.',
      packages=['localize-py'],
      author_email='alexlaki1@yandex.ru',
      zip_safe=False,
      url='https://github.com/Alex-Blade/localize-py',
      long_description=long_description,
      long_description_content_type='text/markdown')
