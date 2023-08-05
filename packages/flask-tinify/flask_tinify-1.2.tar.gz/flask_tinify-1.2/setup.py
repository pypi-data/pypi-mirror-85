import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="flask_tinify",
    version="1.2",
    description="An adaption of tinify as a flask extension",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/minecraftschurli/flask_tinify",
    author="Minecraftschurli",
    author_email="minecraftschurli@gmail.com",
    license="MIT",
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=["flask_tinify"],
    include_package_data=True,
    install_requires=["flask"],
)
