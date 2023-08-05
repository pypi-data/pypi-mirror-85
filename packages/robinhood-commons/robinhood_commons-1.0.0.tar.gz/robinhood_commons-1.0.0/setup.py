from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')


setup(
    name='robinhood_commons',
    version='1.0.0',
    description='Robinhood DayTrader Commons',
    url='https://github.com/mhowell234/robinhood_commons',
    author='mhowell234',
    author_email='mhowell234@gmail.com',

    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.8',
    ],

    package_dir={'': 'robinhood_commons'},
    packages=find_packages(where='robinhood_commons'),
    python_requires='>=3.8, <4',
)
