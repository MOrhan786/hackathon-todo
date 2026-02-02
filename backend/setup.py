from setuptools import setup, find_packages

setup(
    name="todo-backend",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlmodel",
        "python-multipart",
        "python-jose[cryptography]",
        "passlib[bcrypt]",
        "psycopg2-binary",
        "python-dotenv",
    ],
    python_requires=">=3.7",
)