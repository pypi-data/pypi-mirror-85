from setuptools import setup


def get_version():
    version = {}
    with open("chgksuite/version.py") as f:
        exec(f.read(), version)
    return version["__version__"]


long_description = """**chgksuite** is an utility that helps chgk editors.

[Chgk](https://en.wikipedia.org/wiki/What%3F_Where%3F_When%3F) (short for Chto? Gde? Kogda?) is a popular russian quiz.

Project home on gitlab: https://gitlab.com/peczony/chgksuite

Documentation (in Russian): https://peczony.gitbook.io/chgksuite
"""


setup(
    name="chgksuite",
    version=get_version(),
    author="Alexander Pecheny",
    author_email="peczony@gmail.com",
    description="A package for chgk automation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/peczony/chgksuite",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["chgksuite"],
    package_data={
        "chgksuite": [
            "resources/*.json",
            "resources/*.docx",
            "resources/*.pptx",
            "resources/*.toml",
            "resources/*.tex",
            "resources/*.sty",
        ]
    },
    entry_points={"console_scripts": ["chgksuite = chgksuite.__main__:main"]},
    install_requires=[
        "beautifulsoup4",
        "chardet",
        "html2text",
        "parse",
        "PyDocX",
        "pyimgur",
        "python-docx",
        "python-pptx",
        "requests",
        "Pillow",
        "ply",
        "dateparser",
        "pyperclip",
        "toml"
    ]
)
