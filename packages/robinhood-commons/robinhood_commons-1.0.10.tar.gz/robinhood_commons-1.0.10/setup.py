from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')


setup(
    name='robinhood_commons',
    version='1.0.10',
    description='Robinhood DayTrader Commons',
    url='https://github.com/mhowell234/robinhood_commons',
    author='mhowell234',
    author_email='mhowell234@gmail.com',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.8',
    ],

    packages=find_packages(),
    requires=['pyotp', 'requests', 'robin_stocks'],
    install_requires=[
          'pyotp',
          'requests',
          'robin_stocks',
    ],
    python_requires='>=3.8, <4',
)
