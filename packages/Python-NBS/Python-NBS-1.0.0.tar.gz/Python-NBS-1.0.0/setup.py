from setuptools import setup

with open("README.md", "r", encoding='utf-8') as file:
  long_description = file.read()

setup(
    name="Python-NBS",
    version="1.0.0",
    author="Kemo431",
    url="https://github.com/kemo14331/Python-NBS",
    description="A python library for loading NBS files",
    long_description = long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=["python_nbs"],
    install_requires=[],
    extras_require={
        "develop": [],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
