# rf-se-dtl-selectors-plugin

[![Build Status](https://travis-ci.org/kangasta/rf-se-dtl-selectors-plugin.svg?branch=main)](https://travis-ci.org/kangasta/rf-se-dtl-selectors-plugin)

[DOM testing library](https://testing-library.com/) inspired selectors for Robot Framework [SeleniumLibrary](https://robotframework.org/SeleniumLibrary/).

## Installation

To install this plugin from [PyPI](https://pypi.org/project/rf-se-dtl-selectors-plugin/), run:

```bash
pip install rf-se-dtl-selectors-plugin
```

## Usage

In order to use selector provided by this plugin, load `SeleniumLibrary` with `TestingLibrarySelectorsPlugin` in the plugin array:

```robot
*** Settings ***
Library         SeleniumLibrary    plugins=TestingLibrarySelectorsPlugin
```

The plugin provides `label`, `testid`, `text`, and `title` selectors. See [acceptance_tests](./acceptance_tests) directory for usage examples.

## Testing

Check and automatically fix formatting with:

```bash
pycodestyle TestingLibrarySelectorsPlugin
autopep8 -aaar --in-place TestingLibrarySelectorsPlugin
```

Run static analysis with:

```bash
pylint -E --enable=invalid-name,unused-import,useless-object-inheritance TestingLibrarySelectorsPlugin
```

Run acceptance tests in Docker container:

```bash
# Build image
docker build . -t atest

# Run tests
docker run --rm atest

# Run tests and get test output to ./out
docker run -v $(pwd)/out:/out --rm atest -d /out -L TRACE:INFO
```
