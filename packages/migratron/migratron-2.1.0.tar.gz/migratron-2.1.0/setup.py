# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

current_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(current_dir, "migratron", "VERSION"), "r") as vf:
    version = vf.read().strip()

with open(os.path.join(current_dir, "README.rst")) as readme_file:
    readme = readme_file.read()

with open(os.path.join(current_dir, "CHANGELOG.rst")) as history_file:
    history = history_file.read()


def parse_requirements_txt(filename="requirements.txt"):
    with open(os.path.join(current_dir, filename)) as requirements_file:
        requirements = requirements_file.readlines()
        # remove whitespaces
        requirements = [line.strip().replace(" ", "") for line in requirements]
        # remove all the requirements that are comments
        requirements = [line for line in requirements if not line.startswith("#")]
        # remove empty lines
        requirements = list(filter(None, requirements))
        return requirements


setup(
    name="migratron",
    version=version,
    description="Run the database migrations",
    author="Jampp",
    author_email="tech@jampp.com",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/x-rst",
    install_requires=parse_requirements_txt(),
    extras_require={
        "dev-strict": parse_requirements_txt("requirements-dev.txt"),
        "dev": [
            req.replace("==", ">=")
            for req in parse_requirements_txt("requirements-dev.txt")
        ],
    },
    entry_points={"console_scripts": {"migratron = migratron.main:main"}},
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 6 - Mature",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Database",
        "Topic :: Software Development",
    ],
    license="BSD 3-Clause",
    url="https://github.com/jampp/migratron",
    test_suite="tests",
)
