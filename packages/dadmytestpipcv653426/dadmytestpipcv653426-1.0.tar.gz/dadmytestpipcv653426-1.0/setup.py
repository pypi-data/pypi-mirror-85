# -*- coding: utf-8 -*-
import setuptools

with open("README.txt", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dadmytestpipcv653426",  # 这个名字要独一无二的
    version="1.0",
    author="lzw",
    author_email="168805237@qq.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Faner227/PIPTEST",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['opencv-python>=4.2.0.34'],
    py_requires=["example_pkg"],  # 这是你存放python代码的目录
    python_requires='>=3.6',
)


#     # packages=setuptools.find_packages(),

