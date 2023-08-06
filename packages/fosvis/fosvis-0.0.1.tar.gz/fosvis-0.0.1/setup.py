import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="fosvis",
    version="0.0.1",
    description="A tool for visualizing fosmid DNA sequences.",
    long_description=README,
    long_description_content_type="text/markdown",
    # url="https://github.com/realpython/reader",
    author="Tylo Roberts",
    author_email="tylojroberts@gmail.com",
    license="MIT",
    # classifiers=[
    #     "License :: OSI Approved :: MIT License",
    #     "Programming Language :: Python :: 3",
    #     "Programming Language :: Python :: 3.7",
    # ],
    packages=["fosvis"],
    include_package_data=True,
    # install_requires=["feedparser", "html2text"],
    # entry_points={
    #     "console_scripts": [
    #         "realpython=reader.__main__:main",
    #     ]
    # },
)
