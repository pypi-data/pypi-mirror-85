from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='courierman',
    packages=find_packages(exclude=("tests",)),
    use_scm_version=True,
    description='Courier Man - A Python interface for Postman',
    author='Cristiano W. Araujo',
    author_email='cristianowerneraraujo@gmail.com',
    url='https://github.com/cristianowa/courierman',
    download_url='https://github.com/cristianowa/courierman/archive/0.1.zip',
    keywords=['postman'],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=["requests"],
    setup_requires=["setuptools_scm"],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
