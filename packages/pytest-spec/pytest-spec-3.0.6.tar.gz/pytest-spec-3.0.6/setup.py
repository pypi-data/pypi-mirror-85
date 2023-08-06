# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_spec', 'test', 'test.test_formats', 'test.test_results']

package_data = \
{'': ['*']}

install_requires = \
['six']

entry_points = \
{'pytest11': ['pytest_spec = pytest_spec.plugin']}

setup_kwargs = {
    'name': 'pytest-spec',
    'version': '3.0.6',
    'description': 'pytest plugin to display test execution output like a SPECIFICATION',
    'long_description': 'pytest-spec\n===========\npytest plugin to display test execution output like a SPECIFICATION.\n\n\nAvailable features\n==================\n* Format output to look like specification.\n* Group tests by classes and files\n* Failed, passed and skipped are marked and colored.\n* Remove test\\_ and underscores for every test.\n* Supports function based, class based test.\n* Supports describe like tests.\n\n\nOutput example\n==============\n\n.. image:: https://github.com/pchomik/pytest-spec/raw/master/docs/output.png\n\n\nConfiguration\n=============\n\n``spec_header_format``\n----------------------\n\nYou can configure the format of the test headers by specifying a `format string <https://docs.python.org/2/library/string.html#format-string-syntax>`_ in your `ini-file <http://doc.pytest.org/en/latest/customize.html#inifiles>`_:\n\n::\n\n    [pytest]\n    spec_header_format = {module_path}:\n\nIn addition to the ``{path}`` and ``{class_name}`` replacement fields, there is also ``{test_case}`` that holds a more human readable name.\n\n``spec_test_format``\n--------------------\n\nYou can configure the format of the test results by specifying a `format string <https://docs.python.org/2/library/string.html#format-string-syntax>`_ in your `ini-file <http://doc.pytest.org/en/latest/customize.html#inifiles>`_:\n\n::\n\n    [pytest]\n    spec_test_format = {result} {name}\n\n``spec_success_indicator``\n--------------------------\n\nYou can configure the indicator displayed when test passed.\n\n::\n\n    [pytest]\n    spec_success_indicator = ✓\n\n``spec_failure_indicator``\n--------------------------\n\nYou can configure the indicator displated when test failed.\n\n::\n\n    [pytest]\n    spec_failure_indicator = ✗\n\n``spec_skipped_indicator``\n--------------------------\n\nYou can configure the indicator displated when test is skipped.\n\n::\n\n    [pytest]\n    spec_skipped_indicator = ?\n\n``spec_indent``\n---------------\n\n::\n\n    [pytest]\n    spec_indent = "   "\n\nContinuous Integration\n======================\n.. image:: https://github.com/pchomik/pytest-spec/workflows/test/badge.svg\n     :target: https://github.com/pchomik/pytest-spec/actions\n\nDownload\n========\nAll versions of library are available on official `pypi server <https://pypi.org/project/pytest-spec/#history>`_.\n\nInstall\n=======\n::\n\n    pip install pytest-spec\n\nContribution\n============\nPlease feel free to present your idea by code example (pull request) or reported issues.\n\nContributors\n============\n* @0x64746b\n* @lucasmarshall\n* @amcgregor\n* @jhermann\n* @frenzymadness\n* @chrischambers\n* @maxalbert\n* @jayvdb\n\nLicense\n=======\npytest-spec - pytest plugin to display test execution output like a SPECIFICATION.\n\nCopyright (C) 2014-2019 Pawel Chomicki\n\nThis program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.\n',
    'author': 'Pawel Chomicki',
    'author_email': 'pawel.chomicki@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pchomik/pytest-spec',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
