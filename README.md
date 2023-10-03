![GitHub](https://img.shields.io/github/license/dtsong/sleeper-api-wrapper.svg?color=blue)
![GitHub issues](https://img.shields.io/github/issues/dtsong/sleeper-api-wrapper.svg?color=orange)
![PyPI](https://img.shields.io/pypi/v/sleeper-api-wrapper)
# sleeper-api-wrapper
A Python API wrapper for Sleeper Fantasy Sports, as well as tools to simplify data received. It makes all endpoints found in the Sleeper API docs: https://docs.sleeper.app/ available and turns the JSON response received into Python types for easy usage.

Ownership was transferred from @SwapnikKatkoori to @dtsong in March 2022 to continue efforts.
Original Repository: https://github.com/SwapnikKatkoori/sleeper-api-wrapper

# Table of Contents
1. [Project Roadmap](#roadmap)
2. [Installation](#install)
3. [Documentation](#documentation)
4. [Notes](#notes)
5. [Dependencies](#depends)
6. [License](#license)

<a name="roadmap"></a>
# Project Roadmap
* Establish solid CICD practices with automated testing and validation of pull requests via GitHub Actions
* Ensure libraries are up to date and secure.
* Update endpoints and logic with the current Sleeper API docs
* Investigate performance optimization (effort, implementation, etc)

Want to help? Send me a message to @dtsong

<a name="install"></a>
# Install
```
pip install sleeper-api-wrapper
```

<a name="documentation"></a>
# Documentation
There are five objects in the package that get data from the Sleeper API. Most of them are intuitive based on the [Sleeper API docs](https://docs.sleeper.com/), but full documentation for the Python objects and their methods can be found in the [`docs` folder](https://github.com/dtsong/sleeper-api-wrapper/tree/master/docs). There are some bespoke methods for transforming the data into more useful structures in addition to the methods that directly call the API.

<a name="notes"></a>
# Notes
This package is intended to be used by Python version 3.8 and higher. There might be some wacky results for previous versions.

<a name="depends"></a>
# Dependencies

[requests](https://github.com/kennethreitz/requests)
- Used for all http requests in sleeper_wrapper

[pytest](https://github.com/pytest-dev/pytest)
- Used for all testing in sleeper_wrapper

<a name="license"></a>
# License
This project is licensed under the terms of the MIT license.
