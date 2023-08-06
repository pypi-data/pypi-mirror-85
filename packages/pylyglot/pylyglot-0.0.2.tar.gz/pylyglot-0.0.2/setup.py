from setuptools import setup, find_packages
from os.path import join, dirname

__PACKAGE__='pylyglot'
__DESCRIPTION__='pylyglot is a multi programming language converter'
__VERSION__="0.0.2"

setup(
    name=__PACKAGE__,
    version=__VERSION__,
    packages=['pylyglot'],
    description=__DESCRIPTION__,
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    author="lonagi",
    author_email='lonagi22@gmail.com',
    url="https://github.com/lonagi/pylyglot",
)