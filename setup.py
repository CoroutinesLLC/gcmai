from setuptools import setup

setup(
    name="gcmai",
    version="0.1",
    py_modules=["main"],
    install_requires=[
        # TODO: set the version
        "inquirer",
    ],
    entry_points={
        "console_scripts": [
            "gcmai = main:main",
        ],
    },
)
