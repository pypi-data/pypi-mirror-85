import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def load_requirements():
    contents = read("requirements.txt")
    return [line.strip() for line in contents.splitlines()]


CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Topic :: Software Development :: Documentation",
    "Topic :: Software Development :: Version Control :: Git",
    "Topic :: Documentation",
    "Topic :: Documentation :: Sphinx",
]

KEYWORDS = "documentation git pre-commit"

setup(
    name="reslate",
    use_scm_version={"write_to": "reslate/version.py"},
    author="Samuel Rowlinson",
    author_email="sjrowlinson@virginmedia.com",
    description=(
        "A command-line tool to generate and update Sphinx-based API documentation pages."
    ),
    url="https://gitlab.com/sjrowlinson/reslate",
    license="GPL",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=load_requirements(),
    setup_requires=["setuptools_scm"],
    python_requires=">=3.6",
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
    project_urls={"Source": "https://gitlab.com/sjrowlinson/reslate",},
    package_data={"reslate": ["templates/templates/*.rst",]},
    include_package_data=True,
    entry_points={"console_scripts": ["reslate = reslate.__main__:main"]},
)
