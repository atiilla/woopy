from setuptools import setup, find_packages

setup(
    name="woopy",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "python-dotenv",
        "docker",
        "docker-compose",
        "psutil",
        "flask",
        "flask-restful",
        "flask_swagger_ui"
        "python-dotenv",
        "requests",
        "typer",
        "kivy",
        "kivymd",
        "pyyaml",
        "openai",
        "deepl",
        "autopep8",
        "python-digitalocean", 
        "python-terraform"
    ],
    entry_points={
        "console_scripts": [
            "woopy = cli.cli:app",
        ]
    },
)
