# pytest-common-subject
[![pytest-common-subject PyPI version](https://badge.fury.io/py/pytest-common-subject.svg)](https://pypi.python.org/pypi/pytest-common-subject/)
[![pytest-common-subject PyPI pyversions](https://img.shields.io/pypi/pyversions/pytest-common-subject.svg)](https://pypi.python.org/pypi/pytest-common-subject/)
[![pytest-common-subject PyPI license](https://img.shields.io/pypi/l/pytest-common-subject.svg)](https://pypi.python.org/pypi/pytest-common-subject/)

**pytest-common-subject** is a "framework" for organizing tests to reduce boilerplate while writing, improve skimmability when reading, and bolster parallelization when executing the suite.

To utilize this framework, we first choose a single function that our group of tests will all call — in other words, an entry point, or a _common subject_. This function will be automatically called before each of our tests, with args and kwargs that can be customized by overriding fixtures — enabling child test classes to make HTTP requests as a different user, or to use a different cache backend, or to change the value of a monkeypatched method.

The return value of the chosen function will be passed as a fixture to each test. To reap the full benefits of the framework, create separate tests to verify different aspects of the return value. Was the response status code a 200? Did the response contain the expected data? Were the expected rows created in the database? By using separate tests for each of these aspects, we can pinpoint and correct multiple bugs at once, instead of getting sucked into a fix-test-fix cycle with its chorus of "oh, bother, not again!"
