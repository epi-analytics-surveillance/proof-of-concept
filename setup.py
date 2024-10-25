"""Setup file for the python simsurveillance package.
"""

from setuptools import setup, find_packages


setup(
    name='simsurveillance',
    packages=find_packages(include=('simsurveillance', 'simsurveillance.*')),
    include_package_data=True,
    install_requires=[
        'matplotlib',
        'numpy',
        'pandas',
        'pints',
        'scipy',
    ],
    extras_require={
        'stan': [
            'arviz',
            'nest_asyncio',
            'stan',
        ],
        'dev': [
            'flake8',
            'coverage',
        ]
    },
)
