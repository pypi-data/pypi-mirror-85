from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.txt'), encoding='utf-8') as f:
    long_description = f.read()
setup(
    name='TOPSIS_SUKRITI_401803026',
    version='0.0.4',
    description='TOPSIS evaluator for given data. Enter all arguments as strings',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Sukriti Sharma',
    author_email='ssharma_bemba18@thapar.edu',
    license='MIT',
    url='https://pypi.org/project/TOPSIS-SUKRITI-401803026/0.0.1/',
    classifiers=classifiers,
    keywords='calculator',
    packages=find_packages(),
    install_requires=['pandas']
)