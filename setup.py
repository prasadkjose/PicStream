""" setup.py """

from setuptools import setup

setup(
    name="PicStream",
    version="0.1.0",
    packages=["pic_stream"],
    setup_requires=[
        "pylint",
        "pydantic",
        "pydantic-settings",
        "flask",
        "requests",
        "ngrok",
    ],
    install_requires=[
        "pylint",
        "pydantic",
        "pydantic-settings",
        "flask",
        "requests",
        "ngrok",
    ],
    entry_points={"console_scripts": ["picstr = pic_stream.__main__:main"]},
)
