try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'rafiki',
    'description': 'Library to read/write raf format used in League of Legends',
    'long_description': '''Python API for reading and writing to a raf format used
        by RIOT's game League of Legends.
        ''',
    'license': 'MIT',
    'classifiers': [
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    'author': 'Tom Najdek',
    'url': 'https://github.com/tnajdek/rafiki',
    'author_email': 'tom@doppnet.com',
    'version': '0.3.0',
    'packages': ['rafiki'],
    'install_requires': ['future']
}

setup(**config)
