from setuptools import setup, find_packages
from uamf import __version__

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='uamf',
    version=__version__,
    description='',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Adam Konieczny',
    packages=find_packages(include=['uamf', 'uamf.*']),
    python_requires='>=3.8, <4',
    zip_safe=False,
)
