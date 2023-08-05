# Tests

The Python files in this directory contain a range of unit tests. These are functions
(recognized by their name, which start in `test_`) which verify that all `unitlib`
features work as expected, and so ensure that code updates don't introduce any
regressions.

These tests are [run automatically](../.github/workflows/CI.yml) 
on every push of code to GitHub, on a range of different Python versions and OS's.


## How to run tests locally

1. Install your local version of the `unitlib` package, by running,
   in the project root dir:
   ```
   pip install -e .
   ```
2. Install the testing requirements:
   ```
   pip install -r tests/requirements.txt
   ```
3. Finally, run
   ```
   pytest
   ```
