# coding=utf-8

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='cbot',

    version="0.1.0",
    description=(
        'A chinese chat bot'

    ),
    long_description=open('README.md', 'r').read(),
    long_description_content_type="text/markdown",
    author='felix',
    author_email='felix2@foxmail.com',
    maintainer='felix',
    maintainer_email='felix2@foxmail.com',
    license='MIT License',
    packages=find_packages(),
    platforms=["ubuntu", 'windows'],
    url='https://github.com/wangyitao/cbot',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'sqlalchemy',
        'python-dateutil',
        'python-levenshtein',
        'requests',
    ]
)
