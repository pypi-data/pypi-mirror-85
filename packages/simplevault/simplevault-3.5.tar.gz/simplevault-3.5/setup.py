from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required = f.read().splitlines()

    setup(
        name="simplevault",
        version="3.5",
        url="https://gitlab.com/traxix/python/simplevault",
        packages=[".", "simplevault"],
        scripts=["simplevault/simplevault-cli"],
        install_requires=required,
        license="GPLv3",
        author="trax Omar Givernaud",
    )
