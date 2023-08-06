# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beeline',
 'beeline.middleware',
 'beeline.middleware.awslambda',
 'beeline.middleware.bottle',
 'beeline.middleware.django',
 'beeline.middleware.flask',
 'beeline.middleware.werkzeug',
 'beeline.patch',
 'beeline.propagation']

package_data = \
{'': ['*']}

install_requires = \
['libhoney>=1.7.0', 'wrapt>=1.12.1,<2.0.0']

entry_points = \
{'console_scripts': ['tests = beeline.test_suite:run_tests']}

setup_kwargs = {
    'name': 'honeycomb-beeline',
    'version': '2.15.0',
    'description': 'Honeycomb library for easy instrumentation',
    'long_description': '# Honeycomb Beeline for Python\n\n[![Build Status](https://circleci.com/gh/honeycombio/beeline-python.svg?style=svg)](https://app.circleci.com/pipelines/github/honeycombio/beeline-python)\n\nThis package makes it easy to instrument your Python web application to send useful events to [Honeycomb](https://honeycomb.io), a service for debugging your software in production.\n\n- [Usage and Examples](https://docs.honeycomb.io/getting-data-in/beelines/beeline-python/)\n- [API Reference](https://honeycombio.github.io/beeline-python/)\n\n## Compatible with\n\nCurrently supports Django (>1.10), Flask, Bottle, and Tornado.\n\nCompatible with both Python 2.7 and Python 3.\n\n## Get in touch\n\nPlease reach out to [support@honeycomb.io](mailto:support@honeycomb.io) or ping\nus with the chat bubble on [our website](https://www.honeycomb.io) for any\nassistance. We also welcome [bug reports](https://github.com/honeycombio/beeline-python/issues).\n\n## Contributions\n\nFeatures, bug fixes and other changes to `beeline-python` are gladly accepted. Please\nopen issues or a pull request with your change. Remember to add your name to the\nCONTRIBUTORS file!\n\nIf you add a new test module, be sure and update `beeline.test_suite` to pick up the new tests.\n\nAll contributions will be released under the Apache License 2.0.\n\n## Releases\n\nYou may need to install the `bump2version` utility by running `pip install bump2version`.\n\nTo update the version number, do\n\n```\nbump2version [major|minor|patch|release|build]\n```\n\nIf you want to release the version publicly, you will need to manually create a tag `v<x.y.z>` and push it in order to\ncause CircleCI to automatically push builds to github releases and PyPI.\n',
    'author': 'Honeycomb.io',
    'author_email': 'feedback@honeycomb.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/honeycombio/beeline-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=2.7',
}


setup(**setup_kwargs)
