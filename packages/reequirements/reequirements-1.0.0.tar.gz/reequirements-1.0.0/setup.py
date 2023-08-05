import re
from os.path import join as join_path

import setuptools

with open(join_path("reequirements", "__init__.py"), encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setuptools.setup(
    name='reequirements',
    version=version,
    author='Zeke Marffy',
    author_email='zmarffy@yahoo.com',
    packages=setuptools.find_packages(),
    url='https://github.com/zmarffy/reequirements',
    license='MIT',
    description='library for defining and checking for the status of requirements needed for your Python project',
    python_requires='>=3.3',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
    ],
)
