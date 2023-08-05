from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='localize-py',
      version='0.8.1.5',
      description='Localization simplified.',
      packages=['localize_py'],
      author_email='alexlaki1@yandex.ru',
      python_requires='>=3.6',
      zip_safe=False,
      url='https://github.com/Alex-Blade/localize-py',
      long_description=long_description,
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      long_description_content_type='text/markdown')
