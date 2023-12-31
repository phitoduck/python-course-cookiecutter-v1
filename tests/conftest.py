"""
Register pytest plugins, fixtures, and hooks to be used during test execution.

Docs: https://stackoverflow.com/questions/34466027/in-pytest-what-is-the-use-of-conftest-py-files
"""

pytest_plugins = [
    "tests.fixtures.virtualenv",
    "tests.fixtures.project",
]
