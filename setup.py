from setuptools import setup

setup(
    name="gcmai",
    version="0.1",
    py_modules=["main"],  # This is the name of the Python file (without the .py extension)
    entry_points={
        'console_scripts': [
            'gcmai = main:main',  # 'gcmai' is the command, 'main:main' is the module and function
        ],
    },
)

