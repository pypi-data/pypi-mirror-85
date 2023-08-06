from setuptools import setup, find_packages

setup(
    name="wikireader",
    version="0.0.1",
    packages=find_packages(),
    description="Read wikipedia articles distraction free",
    author="Marcel Kerkveld",
    url="https://github.com/mke21/wikireader",
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
