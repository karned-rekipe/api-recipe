# Code Coverage

This document explains how to run code coverage for the API Recipe service and how to interpret the results.

## Running Code Coverage

The API Recipe service uses [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/) to measure code coverage. This tool is already included in the project's dependencies.

### Using the Coverage Script

The easiest way to run code coverage is to use the provided script:

```bash
./run_coverage.sh
```

This script:
1. Sets up the necessary environment variables
2. Runs the tests with coverage measurement
3. Generates both terminal and XML reports

### Manual Execution

If you prefer to run the coverage manually, you need to:

1. Set up the required environment variables (see `run_coverage.sh` for the list)
2. Run the following command:

```bash
python -m pytest --cov=. --cov-report=xml --cov-report=term
```

## Understanding the Coverage Report

The coverage report shows what percentage of your code is being executed by your tests. Here's how to interpret the report:

### Terminal Report

The terminal report shows coverage statistics for each file:

```
Name                                 Stmts   Miss  Cover
--------------------------------------------------------
config/config.py                        14      0   100%
decorators/check_permission.py          32     14    56%
models/item_model.py                    19      0   100%
...
--------------------------------------------------------
TOTAL                                  553    431    22%
```

- **Stmts**: Total number of statements in the file
- **Miss**: Number of statements not covered by tests
- **Cover**: Percentage of statements covered by tests

> **Note**: The overall coverage percentage (22%) may seem low compared to what you might see without the `.coveragerc` configuration. This is because we're now excluding test files from the calculation, which typically have high coverage. This lower percentage is actually a more accurate representation of the application code coverage.

### XML Report

The XML report (`coverage.xml`) contains the same information in a format that can be consumed by other tools, such as code quality platforms or CI/CD pipelines.

## Improving Code Coverage

To improve code coverage:

1. Focus on files with low coverage percentages
2. Write tests for untested functions and methods
3. Ensure edge cases are covered in your tests

### Areas Needing Improvement

Based on the current coverage report, these areas need more test coverage:

- **Middlewares**: All middleware files have 0% coverage
  - database_middleware.py
  - licence_middleware.py
  - token_middleware.py

- **Routers**: The v1.py router has 0% coverage

- **Repositories**: The item_repository.py has 0% coverage

- **Decorators**: The log_time.py decorator has 0% coverage, and check_permission.py has only 56% coverage

- **Interfaces**: The item_interface.py has 0% coverage

- **Utils**: The path_util.py has 0% coverage

- **Main Application**: The main.py file has 0% coverage

These components represent critical parts of the application's functionality and should be prioritized for test coverage improvement.

## Generating HTML Reports

For a more detailed and interactive view of your coverage, you can generate an HTML report:

```bash
python -m pytest --cov=. --cov-report=html
```

This will create a directory called `htmlcov` with an interactive HTML report that shows exactly which lines are covered and which are not.

## Excluding Files from Coverage

The project includes a `.coveragerc` file that configures which files to exclude from the coverage report. This file is located in the root directory and contains:

```
[run]
source = .
omit =
    tests/*
    */__pycache__/*
    */site-packages/*
    .venv/*
    debug.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
    if __name__ == .__main__.:
    pass
    raise ImportError
```

This configuration:
- Excludes test files, cache files, third-party packages, virtual environment, and debug files
- Ignores common lines that typically don't need test coverage (like `__repr__` methods)

With this configuration, the coverage report focuses only on the application code that should be tested, providing a more accurate representation of test coverage.

## Continuous Integration

It's recommended to run code coverage as part of your CI/CD pipeline to track coverage over time and ensure it doesn't decrease with new changes.
