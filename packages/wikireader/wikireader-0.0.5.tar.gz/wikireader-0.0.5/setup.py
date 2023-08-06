from setuptools import setup, find_packages
from os import path, environ

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="wikireader",
    version="0.0.5",
    packages=find_packages(),
    description="Read wikipedia articles distraction free",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Marcel Kerkveld",
    url="https://github.com/mke21/wikireader",
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=[
        "PyQt5>=5.15.1",
        "PyQtWebEngine>=5.15.1",
        "wikipedia>=1.4.0"
    ],
    entry_points={
        'console_scripts': [
            'wikireader=wikireader.cli:main',
        ],
    }
)
