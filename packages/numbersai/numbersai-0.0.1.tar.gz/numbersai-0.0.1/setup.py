import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="numbersai",
    version="0.0.1",
    description="Read numbers like AI",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/kurianbenoy/Reading_like_AI/",
    author="Kurian Benoy",
    author_email="kurian.bkk@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["nosai"],
    include_package_data=True,
    install_requires=["num2words"],
    entry_points={
        "console_scripts": [
            "numbersai=nosai.__main__:main",
        ]
    },
)
