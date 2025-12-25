"""
__main__.py for the Todo In-Memory Python Console App.
This file allows the package to be executed as a script.
"""
from .cli import TodoCLI


def main():
    """
    Main entry point for the Todo application.
    """
    app = TodoCLI()
    app.run()


if __name__ == "__main__":
    main()