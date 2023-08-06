import argparse
from .main import main as program


def main():
    parser = argparse.ArgumentParser(
        description="Search Wikipedia and read the article distraction free"
    )
    arg = parser.parse_args()
    program()

