from os.path import basename
from os.path import splitext

from setuptools import setup
from setuptools import find_packages


def _requires_from_file(filename):
    return open(filename).read().splitlines()


setup(
    name='domainchecker',
    version='1.0.3',
    author='Kento Oki',
    author_email='hrn832@protonmail.com',
    description='A python module that provides check if the domain is available, via Onamae.com Status API',
    long_description='file:README.md',
    long_description_content_type='text/markdown',
    url='https://github.com/kkent030315/onamae-domain-check',
    licence='file: LICENCE',
    python_requires='>=3.7',
    install_requires=_requires_from_file('requirements.txt'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ]
)
