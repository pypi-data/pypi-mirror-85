import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'gilgamesh',
    version = '0.100.0',
    scripts=['gilgamesh'] ,
    author = 'Leonard Pollak',
    author_email = 'leonardp@tr-host.de',
    description = ('distributed data'),
    license = 'AGPL-3.0-or-later',
    keywords = 'beta data',
    url = 'https://gitlab.com/gilgamesh-zmq/ggm',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Utilities',
        'Topic :: System :: Distributed Computing',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python :: 3.7'
    ],
    python_requires='>=3.7',
    install_requires=['pyzmq', 'aiohttp', 'blosc', 'ujson'],
    extras_require={
        'timescaledb': ['psycopg2'],
        'mqtt': ['paho-mqtt'],
    },
    packages=find_packages(exclude=['doc', 'config']),
    package_data = {
        'ggm': [
            'distfiles/*.json',
            'distfiles/*.service',
            'distfiles/*.dist',
            ],
    },
#    entry_points={
#        'console_scripts': [
#            'gilgamesh=gilgamesh:main',
#        ],
#    },
)
