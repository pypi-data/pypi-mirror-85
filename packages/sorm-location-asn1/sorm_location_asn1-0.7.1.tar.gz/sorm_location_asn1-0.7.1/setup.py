from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='sorm_location_asn1',
    version='0.7.1',
    packages=find_packages(exclude=["tests", "tst.py"]),
    install_requires=['pyderasn>=8.1'],
    author='chabErch',
    author_email='chabErch@yandex.ru',
    description='Asn.1 representation for sorm645 location field',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/chabErch/sorm_location_asn1',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Russian',
        'Programming Language :: Python :: 3'
    ]
)
