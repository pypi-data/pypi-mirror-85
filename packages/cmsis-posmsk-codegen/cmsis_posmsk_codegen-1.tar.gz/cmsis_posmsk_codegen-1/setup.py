from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='cmsis_posmsk_codegen',
    version='1',
    description='small utility to generate Pos and Msk definitions for registers, particularly for CMSIS projects',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/metebalci/cmsis_posmsk_codegen',
    author='Mete Balci',
    author_email='metebalci@gmail.com',
    license='GPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Utilities',
    'Programming Language :: Python :: 3.6',
    ],

    keywords='cmsis register pos msk',
    py_modules=['cmsis_posmsk_codegen'],
    install_requires=['pyyaml==5.3.1'],

    entry_points={
        'console_scripts': [
            'cmsis_posmsk_codegen=cmsis_posmsk_codegen:main',
        ],
    },
)
