import pathlib
from setuptools import *

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE/"README.md").read_text()

setup(
      name='cpp_code_style_formatter',
      version='1.0.3',
      entry_points={
        "console_scripts": ['cpp_code_style_formatter = cpp_code_style_formatter.__main__:main']
      },
      description='Formatter cam format cpp code(cpp_code_style_formatter --format -f <path to file>)',
      long_description=README,
      long_description_content_type="text/markdown",
      packages=['cpp_code_style_formatter'],
      author="Stanislav Dzundza",
      author_email='stas.dzundza@gmail.com',
)