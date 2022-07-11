import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="sleeper-api-wrapper",
    version="1.0.7",
    description="A Python API wrapper for Sleeper Fantasy Football, as well as tools to simplify data recieved.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/SwapnikKatkoori/sleeper-api-wrapper",
    author="Swapnik Katkoori",
    author_email="katkoor2@msu.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["sleeper_wrapper"],
    include_package_data=True,
    install_requires=["requests>=2.22.0"]
)
